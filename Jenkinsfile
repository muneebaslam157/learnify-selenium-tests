pipeline {
    agent any

    environment {
        APP_REPO_URL      = 'https://github.com/muneebaslam157/Learnify-Skillup.git'
        APP_IMAGE_NAME    = 'learnify-skillup-image'
        APP_CONTAINER_NAME = 'learnify-skillup-app'
        APP_PORT          = '5173'

        // Internal URL used by Selenium tests (inside EC2)
        APP_URL           = "http://localhost:${APP_PORT}"

        // Public URL that sir will open from browser
        EC2_PUBLIC_URL    = 'http://13.233.96.170:5173/'
    }

    stages {

        stage('Checkout Tests Repo') {
            steps {
                echo 'Checking out Selenium tests (this repo)...'
                checkout scm
            }
        }

        stage('Checkout App Repo') {
            steps {
                echo 'Cloning Learnify app repo...'
                sh """
                    rm -rf app
                    git clone ${APP_REPO_URL} app
                """
            }
        }

        stage('Build App Docker Image') {
            steps {
                dir('app') {
                    echo 'Building Docker image for Learnify app...'
                    sh "docker build -t ${APP_IMAGE_NAME} ."
                }
            }
        }

        stage('Run App Container') {
            steps {
                echo 'Starting app container...'
                sh """
                    docker rm -f ${APP_CONTAINER_NAME} || true
                    docker run -d --name ${APP_CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${APP_IMAGE_NAME}
                    echo "Waiting for app to start..."
                    sleep 25
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests against ${APP_URL}..."
                sh """
                    python3 -m pip install --user -r requirements.txt
                    export APP_URL=${APP_URL}
                    python3 -m unittest -v tests.test_learnify
                """
            }
        }
    }

    post {

        always {
            echo "Pipeline finished (container left running so EC2 URL is reachable)."
        }

        success {
            echo "All tests passed. Sending success email..."

            emailext(
    to: 'muneebaslam497@gmail.com muneebaslam157@gmail.com qasimalik@gmail.com',
    subject: "Learnify CI Pipeline Result (#${env.BUILD_NUMBER})",
    body: """
Hello Sir,

The Learnify CI pipeline ran successfully on Jenkins (EC2).

Tests Repository: https://github.com/muneebaslam157/learnify-selenium-tests
Branch: ${env.GIT_BRANCH}
Build: #${env.BUILD_NUMBER}
Status: ${currentBuild.currentResult}

All 10 Selenium smoke tests passed against the Dockerized Learnify app 
running on http://13.233.96.170:5173/

Console Output:
${env.BUILD_URL}console

Regards,
Muneeb Aslam
FA22-BCS-077
"""
)

        }

        failure {
            echo "Some tests FAILED. Email notification (if desired) can be sent here."
        }
    }
}




