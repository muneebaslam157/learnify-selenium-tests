pipeline {
    agent any

    environment {
        APP_URL = "http://localhost:5173"
        // Ensure pip --user scripts are on PATH (for selenium, etc.)
        PATH = "/var/lib/jenkins/.local/bin:${env.PATH}"
    }

    stages {

        stage('Checkout Tests Repo') {
            steps {
                echo 'Checking out Selenium tests (this repo) from SCM...'
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
                        echo "Creating .env for CI build..."

                        cat > .env << 'EOF'
VITE_APP_FIREBASE_API=AIzaSyDXqhNa1AXP3l1v7FQIbafGKGR1bNN0vdI
VITE_APP_FIREBASE_AUTH_DOMAIN=lms-intern.firebaseapp.com
VITE_APP_FIREBASE_PROJECT_ID=lms-intern
VITE_APP_FIREBASE_STORAGE_BUCKET=lms-intern.appspot.com
VITE_APP_FIREBASE_MESSAGING_SENDER_ID=233535439534
VITE_APP_FIREBASE_APP_ID=1:233535439534:web:82413100859e0250ef233f
VITE_APP_FIREBASE_MEASUREMENT_ID=G-4HXB67S06H
EOF

                        docker build -t learnify-skillup-image .
                    '''
                }
            }
        }

        stage('Run App Container') {
            steps {
                echo 'Starting app container...'
                sh '''
                    docker rm -f learnify-skillup-app || true

                    docker run -d --name learnify-skillup-app \
                        -p 5173:5173 \
                        learnify-skillup-image

                    echo "Waiting for app to start..."
                    sleep 25
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running Selenium tests against ${APP_URL}..."
                sh '''
                    python3 -m pip install --user -r requirements.txt
                    export APP_URL="http://localhost:5173"
                    python3 -m unittest -v tests.test_learnify
                '''
            }
        }
    }

    post {

        success {
            echo 'All tests passed. Sending success email...'
            emailext(
                subject: "Learnify CI – SUCCESS (Build #${env.BUILD_NUMBER})",
                body: """Hello Sir,

The Learnify CI pipeline ran successfully on Jenkins (EC2).

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
                to: "muneebaslam497@gmail.com, muneebaslam157@gmail.com"
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
                to: "muneebaslam497@gmail.com, muneebaslam157@gmail.com"
            )
        }
    }
}
