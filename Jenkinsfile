pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                dir('iaemp-backend') {
                    sh 'docker build -t iaemp-backend-ci .'
                }
            }
        }
    }
}
