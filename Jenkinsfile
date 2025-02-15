pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    curl https://pyenv.run | bash
                    export PATH="$HOME/.pyenv/bin:$PATH"
                    eval "$(pyenv init -)"
                    pyenv install 3.13
                    pyenv global 3.13
                    python3 -m venv .venv
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
