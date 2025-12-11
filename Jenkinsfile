pipeline {
    agent any

    environment {
        // Repos
        TESTS_REPO = 'https://github.com/muneebaslam157/learnify-selenium-tests.git'
        APP_REPO   = 'https://github.com/muneebaslam157/Learnify-Skillup.git'

        // App URLs
        APP_INTERNAL_URL = 'http://localhost:5173'          // used INSIDE EC2 for tests
        APP_PUBLIC_URL   = 'http://13.233.96.170:5173'      // shown in email to sir

        // Docker
        APP_IMAGE   = 'learnify-skillup-image'
        APP_CONTAINER = 'learnify-skillup-app'
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
                  git clone ${APP_REPO} app
                """
            }
        }

        stage('Build App Docker Image') {
            steps {
                dir('app') {
                    echo 'Building Docker image for Learnify app...'
                    sh "docker build -t ${APP_IMAGE} ."
                }
            }
        }

        stage('Run App Container') {
            steps {
                echo 'Starting app container...'
                sh """
                  docker rm -f ${APP_CONTAINER} || true
                  docker run -d --name ${APP_CONTAINER} -p 5173:5173 ${APP_IMAGE}
                  echo 'Waiting for app to start...'
                  sleep 25
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests against ${APP_INTERNAL_URL}..."
                sh """
                  python3 -m pip install --user -r requirements.txt
                  export APP_URL=${APP_INTERNAL_URL}
                  python3 -m unittest -v tests.test_learnify
                """
            }
        }
    }

    post {
        always {
            echo "Cleaning up app container..."
            sh "docker rm -f ${APP_CONTAINER} || true"
        }

        success {
            echo "All tests passed. Sending success email..."
            emailext(
                subject: "Learnify CI - SUCCESS (Build #${env.BUILD_NUMBER})",
                to: "muneebaslam497@gmail.com muneebaslam157@gmail.com",
                body: """Hello Sir,

The Learnify CI pipeline ran successfully on Jenkins (EC2).

Tests Repository: ${env.GIT_URL}
Branch:          ${env.GIT_BRANCH}
Build:           #${env.BUILD_NUMBER}
Status:          SUCCESS

All 10 Selenium smoke tests passed against the Dockerized Learnify app
running on ${APP_PUBLIC_URL} (public URL of the EC2 instance).

You can view the full console output here:
${env.BUILD_URL}console

Regards,
Muneeb Aslam
FA22-BCS-077
"""
            )
        }

        failure {
            echo "Some tests FAILED. Sending failure email..."
            emailext(
                subject: "Learnify CI - FAILED (Build #${env.BUILD_NUMBER})",
                to: "muneebaslam497@gmail.com muneebaslam157@gmail.com",
                body: """Hello Sir,

The Learnify CI pipeline FAILED on Jenkins (EC2).

Tests Repository: ${env.GIT_URL}
Branch:          ${env.GIT_BRANCH}
Build:           #${env.BUILD_NUMBER}
Status:          FAILED

Some Selenium tests did not pass against the Dockerized Learnify app
running on ${APP_PUBLIC_URL} (public URL of the EC2 instance).

Please review the Jenkins console logs here:
${env.BUILD_URL}console

Regards,
Muneeb Aslam
FA22-BCS-077
"""
            )
        }
    }
}


