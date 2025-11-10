pipeline{
    agent any
    
    stages {
        stage('Cloning Github Repo to Jenkins') {
            steps {
                script{
                    echo 'Cloning...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/Pratikshk16/Hotel-Reservation-Prediction-with-MLFlow-Jenkins-and-GCP-Deployment.git']])

                }
            }
        }
    }
}