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
        stage('Building and pushing docker image to Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script{
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                    
                            gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

                            docker build --platform=linux/amd64 -t us-central1-docker.pkg.dev/${GCP_PROJECT}/hotel-images/hotel-reservation-prediction:latest .
                            export DOCKER_CLIENT_TIMEOUT=300
                            export COMPOSE_HTTP_TIMEOUT=300


                            docker push us-central1-docker.pkg.dev/${GCP_PROJECT}/hotel-images/hotel-reservation-prediction:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to google cloud run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script{
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                    
                            gcloud run deploy hotel-reservation-prediction \
                            --image us-central1-docker.pkg.dev/${GCP_PROJECT}/hotel-images/hotel-reservation-prediction:latest \
                            --platform managed \
                            --region us-central1 \
                            --allow-unauthenticated \
                            --quiet
                        '''
                    }
                }
            }
        }

    }
}