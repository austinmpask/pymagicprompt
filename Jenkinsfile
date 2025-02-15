pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install poetry
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
