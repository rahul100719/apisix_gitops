pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args '-u root'
        }
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
                archiveArtifacts artifacts: '*.zip'
            }
        }
    }
}
