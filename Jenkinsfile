pipeline {
    agent any

    environment {
        GCP_PROJECT = 'mlops-new-475914'
        IMAGE_NAME = 'hotel-reservation-prediction'
        REGION = 'us-central1'
        REPO_PATH = 'hotel-images'
    }

    stages {

        stage('Clone Repo') {
            steps {
                checkout scmGit(branches: [[name: '*/main']],
                                userRemoteConfigs: [[credentialsId: 'github_token',
                                url: 'https://github.com/Pratikshk16/Hotel-Reservation-Prediction-with-MLFlow-Jenkins-and-GCP-Deployment.git']])
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        echo "Building Docker image..."
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

                        IMAGE_TAG=$(date +%Y%m%d%H%M%S)
                        docker build --platform=linux/amd64 -t ${REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPO_PATH}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker push ${REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPO_PATH}/${IMAGE_NAME}:${IMAGE_TAG}
                        echo $IMAGE_TAG > image_tag.txt
                    '''
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        echo "Deploying to Cloud Run..."
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        IMAGE_TAG=$(cat image_tag.txt)
                        gcloud run deploy ${IMAGE_NAME} \
                            --image ${REGION}-docker.pkg.dev/${GCP_PROJECT}/${REPO_PATH}/${IMAGE_NAME}:${IMAGE_TAG} \
                            --platform managed \
                            --region ${REGION} \
                            --allow-unauthenticated \
                            --port 8080 \
                            --quiet
                    '''
                }
            }
        }
    }
}
