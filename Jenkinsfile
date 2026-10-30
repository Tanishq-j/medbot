pipeline {
    agent any

    environment {
        APP_NAME = 'medbot'
        IMAGE_NAME = 'medbot'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout Source') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m pip install --no-cache-dir --upgrade pip
                    python3 -m pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Execute Automated Tests') {
            steps {
                echo 'Running pytest test suite...'
                sh '''
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                }
            }
        }

        stage('Build Docker Container Image') {
            steps {
                echo 'Building MedBot container image...'
                sh '''
                    if docker info > /dev/null 2>&1; then
                        echo "Docker daemon detected. Building Docker image..."
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        echo "Docker image built successfully: ${IMAGE_NAME}:${IMAGE_TAG}"
                    else
                        echo "Docker daemon socket not mounted in Jenkins container. Skipping container build stage."
                    fi
                '''
            }
        }

        stage('Sanity Check') {
            steps {
                echo 'Verifying FastAPI & Streamlit files...'
                sh '''
                    python3 -c "from app import main; print('FastAPI app imported successfully')"
                    python3 -c "from app.agents import AGENT_NAMES; print('Registered agents:', AGENT_NAMES)"
                '''
            }
        }
    }

    post {
        success {
            echo '========================================='
            echo ' MedBot CI/CD Pipeline Build SUCCESSFUL!'
            echo '========================================='
        }
        failure {
            echo '========================================='
            echo ' MedBot CI/CD Pipeline Build FAILED!'
            echo '========================================='
        }
    }
}
