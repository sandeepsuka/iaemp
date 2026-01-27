pipeline {
  agent any

  environment {
    KUBECONFIG = "C:\\ProgramData\\Jenkins\\.kube\\config"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('DEBUG — List workspace') {
      steps {
        powershell 'pwd'
        powershell 'dir'
        powershell 'dir iaemp'
        powershell 'dir iaemp\\k8s'
      }
    }

    stage('Build Backend Image') {
      steps {
        dir('iaemp/iaemp-backend') {
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
        powershell 'kubectl apply -f iaemp/k8s/backend-deployment.yaml'
        powershell 'kubectl apply -f iaemp/k8s/backend-hpa.yaml'
        powershell 'kubectl rollout restart deployment iaemp-backend'
      }
    }
  }
}
