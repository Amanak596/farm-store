pipeline {
    agent any

    environment {
        IMAGE_NAME = "aman5250/farm-store"
    }

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
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to OpenShift') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'openshift-token',
                        variable: 'OC_TOKEN'
                    )
                ]) {
                    sh '''
                        oc login \
                          --server="https://api.rm3.7wse.p1.openshiftapps.com:6443" \
                          --token="$OC_TOKEN"

                        oc project aman-dev-dev

                        oc set image deployment/farm-store \
                          farm-store=${IMAGE_NAME}:${BUILD_NUMBER}

                        oc rollout status deployment/farm-store

                        oc logout
                    '''
                }
            }
        }
    }
}
