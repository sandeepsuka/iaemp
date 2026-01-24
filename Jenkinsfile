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
          powershell 'docker build -t iaemp-backend-ci .'
        }
      }
    }

    stage('Load Image into Minikube') {
      steps {
        powershell 'minikube image load iaemp-backend-ci'
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        powershell 'kubectl apply -f k8s/backend-deployment.yaml'
        powershell 'kubectl apply -f k8s/backend-hpa.yaml'
        powershell 'kubectl rollout restart deployment iaemp-backend'
      }
    }
  }
}
