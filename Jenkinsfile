pipeline {
    agent {
        docker {
            image 'python:3.13'
            args '--user root'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh '''
                    pip install pytest setuptools twine wheel
                    pytest
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'python setup.py sdist bdist_wheel'
            }
        }

        stage('Publish') {
            environment {
                PYPI_TOKEN = credentials('pypi-magicprompt')
            }
            steps {
                sh '''
                    twine upload dist/* --username __token__ --password $PYPI_TOKEN
                '''
            }
        }
    }
}
