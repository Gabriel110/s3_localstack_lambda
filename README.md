### PYENV
Para que não aja problemas de dependenciar crie um ambiente virtual python dentro da pasta lambda:
- 1 - cd lambda
- 2 - python -m venv gabriel_lambda
- 3 - .\gabriel_lambda\Scripts\activate
- 4 - pip install -r requirements.txt

### DOCKER
Execute o dockercompose com o comando:
- 1 - docker-compose up

### TERRAFORM
Execute os comando:
- 1 - terraform init
- 2 - terraform apply -auto-approve

### CURL
Execute essa curl no seu navegador preferido:

    curl --request PUT \
    --url 'http://s3.localhost.localstack.cloud:4566/gabriel-bucket-122345/input/arquivos?=' \
    --header 'Content-Type: text/plain' \
    --header 'User-Agent: insomnia/8.2.0' \
    --header 'x-amz-acl: public-read' \
    --data R0FCUklFTA0KTUVMSVNTQQ0KUkFGQUVM