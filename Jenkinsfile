pipeline {
    agent any

    environment {
        // Base URL where the app will be available from inside Jenkins/EC2
        APP_URL = "http://localhost:5173"
        // Git repo for the React app (Learnify)
        APP_REPO = "https://github.com/muneebaslam157/Learnify-Skillup.git"
    }

    stages {
        stage('Checkout Tests Repo') {
            steps {
                echo 'Checking out Selenium tests (this repo)...'
                // Uses the Jenkins job SCM configuration
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
                    sh 'docker build -t learnify-skillup-image .'
                }
            }
        }

        stage('Run App Container') {
            steps {
                echo 'Starting app container...'
                sh """
                    docker rm -f learnify-skillup-app || true
                    docker run -d --name learnify-skillup-app -p 5173:5173 learnify-skillup-image
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
            echo 'Cleaning up app container...'
            sh 'docker rm -f learnify-skillup-app || true'
        }

        success {
            echo 'All tests passed. Sending success email...'
            emailext(
                subject: "Learnify CI – SUCCESS (Build #${env.BUILD_NUMBER})",
                body: """Hello Sir,

The Learnify CI pipeline ran successfully on Jenkins.

Repository (tests): ${env.GIT_URL}
Branch:             ${env.GIT_BRANCH}
Build:              #${env.BUILD_NUMBER}
Status:             SUCCESS

All 10 Selenium smoke tests passed against the Dockerized Learnify app
running on ${APP_URL}.

You can view full console output here:
${env.BUILD_URL}console

Regards,
Automated CI Pipeline
""",
                to: "muneebaslam497@gmail.com"
            )
        }

        failure {
            echo 'Some tests FAILED. Sending failure email...'
            emailext(
                subject: "Learnify CI – FAILED (Build #${env.BUILD_NUMBER})",
                body: """Hello Sir,

The Learnify CI pipeline encountered a FAILURE.

Repository (tests): ${env.GIT_URL}
Branch:             ${env.GIT_BRANCH}
Build:              #${env.BUILD_NUMBER}
Status:             FAILURE

Please check the Jenkins console for details:
${env.BUILD_URL}console

Regards,
Automated CI Pipeline
""",
                to: "muneebaslam497@gmail.com"
            )
        }
    }
}
