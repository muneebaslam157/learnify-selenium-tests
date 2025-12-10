pipeline {
    agent any

    environment {
        APP_REPO_URL       = 'https://github.com/muneebaslam157/Learnify-Skillup.git'
        APP_CONTAINER_NAME = 'learnify-skillup-app'
        APP_IMAGE_NAME     = 'learnify-skillup-image'
        APP_PORT           = '5173'
        APP_URL            = "http://localhost:${APP_PORT}"
    }

    stages {
        stage('Checkout Tests Repo') {
            steps {
                echo "Checking out Selenium tests (this repo)..."
                checkout scm
            }
        }

        stage('Checkout App Repo') {
            steps {
                echo "Cloning Learnify app repo..."
                sh '''
                  rm -rf app || true
                  git clone ${APP_REPO_URL} app
                '''
            }
        }

        stage('Build App Docker Image') {
            steps {
                dir('app') {
                    echo "Building Docker image for Learnify app..."
                    sh "docker build -t ${APP_IMAGE_NAME} ."
                }
            }
        }

        stage('Run App Container') {
            steps {
                echo "Starting app container..."
                sh '''
                  docker rm -f ${APP_CONTAINER_NAME} || true

                  docker run -d --name ${APP_CONTAINER_NAME} -p ${APP_PORT}:5173 ${APP_IMAGE_NAME}

                  echo "Waiting for app to start..."
                  sleep 25
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests against ${APP_URL}..."
                sh '''
                  pip install --user -r requirements.txt || pip install -r requirements.txt

                  export APP_URL=${APP_URL}

                  python -m unittest -v tests.test_learnify
                '''
            }
        }
    }

    post {
        always {
            echo "Cleaning up app container..."
            sh 'docker rm -f ${APP_CONTAINER_NAME} || true'
        }

        success {
            echo "All tests passed. (Email to sir will be configured here.)"
        }

        failure {
            echo "Some tests FAILED. (Email to sir will be configured here.)"
        }
    }
}
