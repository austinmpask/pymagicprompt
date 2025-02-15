pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv .venv
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
