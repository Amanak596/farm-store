pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Farm Store source code'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    cd backend
                    python3 -m venv jenkins-venv
                    . jenkins-venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    cd backend
                    . jenkins-venv/bin/activate
                    python -m py_compile app.py auth_utils.py db.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t farm-store:${BUILD_NUMBER} .'
            }
        }
    }
}
