pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'mlops-new-475914'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }
    
    stages {
        stage('Cloning Github Repo to Jenkins') {
            steps {
                script{
                    echo 'Cloning...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/Pratikshk16/Hotel-Reservation-Prediction-with-MLFlow-Jenkins-and-GCP-Deployment.git']])

                }
            }
        }
        stage('Setting up Virtual Environment and Installing Dependencies') {
            steps {
                script{
                    echo 'Setting up Virtual Environment and Installing Dependencies'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate

                        pip install --upgrade pip
                        pip install -e .
                        '''
                }
            }
        }
        stage('Building and pushing docker image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script{
                        echo 'Building and pushing docker image to GCR............'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:latest .

                            docker build --platform=linux/amd64 -t gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:latest .
                        '''
                    }
                }
            }
        }
    }
}