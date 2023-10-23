### Repositorio
Esse repositorio implementa por meio das tecnologias:
 - Docker
 - Terraform
 - LocalStack
uma lambda que tem a responsabolidade de consumir arquivos csv de um bucket S3 e enviar mensagem a um sns ligado a um sns.
A lambda porvez não evia todo o arquivo de uma vez, ela ler pequenos blocos do arquivo e tranforma em mensagem sns.

<div style="text-align: center;">
  <img src="./asserts/localstack.png"/>
</div>


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
no corpo da requisição use o arquivo cardsets.csv para testar o lambda

### Insomnia
Importe o arquivo local-stack para obter as requisições relacionadas aos recursos da aws
