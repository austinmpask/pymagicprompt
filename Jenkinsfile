pipeline {
    agent any

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                    sudo add-apt-repository ppa:deadsnakes/ppa
                    sudo apt-get update
                    sudo apt-get install -y python3.13 python3.13-venv
                    python3.13 -m venv .venv
                '''
            }
        }

        stage('Setup Dependencies') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install poetry
                    poetry install
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
