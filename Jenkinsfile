pipeline {
    agent {
        docker {
            image 'python:3.13'
        }
    }

    stages {
        stage('Something') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install poetry
                    poetry install
                    poetry run pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'poetry run pytest'
            }
        }

    // stage('Build and Publish') {
    //     environment {
    //         PYPI_TOKEN = credentials('PYPI_TOKEN')
    //     }
    //     steps {
    //         sh '''
    //             poetry config pypi-token.pypi $PYPI_TOKEN
    //             poetry build
    //             poetry publish --no-interaction
    //         '''
    //     }
    // }
    }
}
