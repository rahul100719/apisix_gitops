pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'   // allow apt install inside container
        }
    }

    environment {
        PROJECT = "apisix_gitops"
        ZIP = "${PROJECT}.zip"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    apt update
                    apt install -y make zip git curl
                    pip install poetry
                '''
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Init') {
            steps {
                sh 'make init'
            }
        }

        stage('Lint') {
            steps {
                sh 'make lint || true'
            }
        }

        stage('Build') {
            steps {
                sh 'make build'
            }
        }

        stage('Test') {
            steps {
                sh 'make test'
            }
        }

        stage('Package') {
            steps {
                sh 'make zip'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: '*.zip', fingerprint: true
            }
        }

        stage('Deploy to K8s') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        make deploy
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
