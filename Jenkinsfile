pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
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
    }
}