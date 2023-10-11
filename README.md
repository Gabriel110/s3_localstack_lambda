### DOCKER
Execute o dockercompose com o comando:
- docker-compose up

### TERRAFORM
Execute os comando:
- terraform init
- terraform apply -auto-approve

### CURL
Execute essa curl no seu navegador preferido:
    curl --request PUT \
    --url 'http://s3.localhost.localstack.cloud:4566/gabriel-bucket-122345/input/arquivos?=' \
    --header 'Content-Type: text/plain' \
    --header 'User-Agent: insomnia/8.2.0' \
    --header 'x-amz-acl: public-read' \
    --data R0FCUklFTA0KTUVMSVNTQQ0KUkFGQUVM