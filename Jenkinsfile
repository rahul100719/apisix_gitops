pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'
        }
    }

    environment {
        PROJECT = "apisix_gitops"
        ZIP = "${PROJECT}.zip"

        // Your Jenkins credentials ID
        ENCRYPTED_CLIENTS_RAHUL = credentials('ENCRYPTED_CLIENTS_RAHUL')
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

       stage('Decrypt Secret') {
    steps {
        sh '''
            echo "Encrypted value: $ENCRYPTED_CLIENTS_RAHUL"
            make get_secret ENCRYPTED_CLIENTS_RAHUL="$ENCRYPTED_CLIENTS_RAHUL"
        '''
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
                archiveArtifacts artifacts: '*.zip'
            }
        }
    }
}
