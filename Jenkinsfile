pipeline {
    agent any

    environment {
        // App URL inside EC2 / Jenkins
        APP_URL = "http://localhost:5173"

        // Make sure user-level pip binaries are on PATH
        PATH = "/var/lib/jenkins/.local/bin:${env.PATH}"
    }

    stages {

        stage('Checkout Tests Repo') {
            steps {
                echo 'Checking out Selenium tests (this repo) from SCM...'
                // Jenkins has already done the initial checkout via "Declarative: Checkout SCM",
                // but we call checkout scm to make sure workspace is up to date.
                checkout scm
            }
        }

        stage('Checkout App Repo') {
            steps {
                echo 'Cloning Learnify app repo...'
                sh '''
                    rm -rf app
                    git clone https://github.com/muneebaslam157/Learnify-Skillup.git app
                '''
            }
        }

        stage('Build App Docker Image') {
            steps {
                echo 'Building Docker image for Learnify app...'
                dir('app') {
                    sh '''
                        docker build -t learnify-skillup-image .
                    '''
                }
            }
        }

        stage('Run App Container') {
            steps {
                echo 'Starting app container...'
                sh '''
                    # Remove any old container if present
                    docker rm -f learnify-skillup-app || true

                    # Run new container
                    docker run -d --name learnify-skillup-app -p 5173:5173 learnify-skillup-image

                    echo "Waiting for app to start..."
                    sleep 25
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests against ${APP_URL}..."

                sh '''
                    # Install Python dependencies for Selenium tests
                    python3 -m pip install --user -r requirements.txt

                    # Run tests with APP_URL exported for the test suite
                    export APP_URL="http://localhost:5173"
                    python3 -m unittest -v tests.test_learnify
                '''
            }
        }
    }

    post {

        // Do NOT remove the container here, so the app stays running on port 5173
        // and can be accessed at http://13.233.96.170:5173/ after the build.

        success {
            echo 'All tests passed. Sending success email...'
            emailext(
                subject: "Learnify CI – SUCCESS (Build #${env.BUILD_NUMBER})",
                body: """Hello Sir,

The Learnify CI pipeline ran successfully on Jenkins.

Tests Repository: ${env.GIT_URL}
Branch:           ${env.GIT_BRANCH}
Build:            #${env.BUILD_NUMBER}
Status:           SUCCESS

All 10 Selenium smoke tests passed against the Dockerized Learnify app
running on ${APP_URL} inside the EC2 instance.

You can view the full console output here:
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

Tests Repository: ${env.GIT_URL}
Branch:           ${env.GIT_BRANCH}
Build:            #${env.BUILD_NUMBER}
Status:           FAILURE

Please check the Jenkins console for detailed logs:
${env.BUILD_URL}console

Regards,
Automated CI Pipeline
""",
                to: "muneebaslam497@gmail.com"
            )
        }
    }
}



