# Sistema de Transferência entre Usuários
Este projeto implementa um sistema de transferência de saldo entre usuários utilizando Django e Django REST Framework. O sistema permite o registro, autenticação, gerenciamento de carteira (wallet) e transferência de saldo entre os usuários, proporcionando uma API robusta e segura para operações financeiras básicas.

## Recursos
Cadastro de Usuários: Endpoint para registrar novos usuários.

Autenticação: Endpoint para login de usuários.

Gerenciamento de Conta: Endpoints para atualizar o saldo da carteira e consultar o saldo do usuário autenticado.

Consulta de Saldo de Outros Usuários: Permite visualizar o saldo da carteira de outros usuários mediante autorização.

Transferência de Saldo: Endpoints para realizar transferências de saldo entre usuários.

Listagem de Transferências: Possibilita a listagem de transferências realizadas, com suporte a filtragem por intervalo de datas.

## Endpoints Principais
/register/: Cadastro de novos usuários.

/login/: Login e obtenção de token de autenticação.

/delete/: Exclusão de usuário.

/wallet/update/: Atualização do saldo da carteira do usuário autenticado.

/wallet/: Consulta do saldo da carteira do usuário autenticado.

/wallet/str:name/: Consulta do saldo da carteira de um outro usuário.

/transfer/: Realização de transferência de saldo entre usuários.

/transfer/list/: Listagem de transferências realizadas, com suporte a filtros por data.

## Tecnologias Utilizadas
Django: Framework principal para desenvolvimento web.

Django REST Framework (DRF): Ferramenta para criação de APIs RESTful.

Django ORM: Gerenciamento e manipulação do banco de dados.

Python: Linguagem de programação utilizada para o desenvolvimento do sistema.

## Qualidade de Código
Testes Automatizados: O projeto possui uma suíte de testes automatizados utilizando o framework pytest e Django Test Client. Os testes abrangem casos de uso essenciais, tais como a criação e consulta de carteiras, transferências de saldo, validação de dados e manipulação de erros.

Linter: O código segue padrões de qualidade e estilo definidos, utilizando ferramentas de linting para garantir a manutenção de um código limpo, consistente e aderente às boas práticas de desenvolvimento.


## Como Executar o Projeto
Instalação das Dependências:
pip install -r requirements.txt

Migração do Banco de Dados:
python manage.py migrate

Execução do Servidor:
python manage.py runserver

Executar Testes Automatizados:
python -m pytest users/tests

## Considerações Finais
Este sistema foi desenvolvido com foco em robustez, segurança e facilidade de manutenção. A implementação dos testes automatizados e a utilização de ferramentas de linting garantem um ambiente de desenvolvimento estável e propício para futuras expansões e melhorias. O projeto é ideal para ser utilizado como base em aplicações que demandam operações financeiras simples e seguras entre usuários.


