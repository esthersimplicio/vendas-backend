# Sistema de Vendas - Backend

Este é o backend para um sistema de vendas desenvolvido em Flask, um framework web em Python. O backend é responsável por gerenciar o banco de dados MySQL, fornecer APIs para autenticação de usuários, operações de CRUD (criar, ler, atualizar, excluir) para usuários, e interagir com o frontend para fornecer dados dinâmicos ao usuário.

## Funcionalidades Principais

### 1. Autenticação de Usuários

O backend oferece endpoints para autenticação de usuários. Ele valida as credenciais do usuário (email e senha) no banco de dados MySQL. Se as credenciais forem válidas, o usuário é autenticado e uma sessão é criada para manter o estado da autenticação.

- **`POST /signin`**: Endpoint para autenticação de usuários. Requer um email e senha válidos. Retorna um token de autenticação se bem-sucedido.

### 2. Gerenciamento de Usuários

O backend permite que os usuários se cadastrem no sistema e gerenciem suas informações pessoais.

- **`POST /signup`**: Endpoint para registro de novos usuários. Requer nome, telefone, email e senha.
- **`GET /perfil`**: Obtém as informações do usuário autenticado.
- **`GET /editar_usuario`**: Obtém as informações do usuário autenticado para edição.
- **`POST /editar_usuario`**: Permite que os usuários editem suas informações. Pode incluir nome, telefone, email e senha.

### 3. Exclusão de Conta de Usuário

- **`DELETE /deletar_usuario`**: Exclui a conta do usuário autenticado do banco de dados.

## Configuração e Execução

### Requisitos

- Python 3.x
- Flask
- Flask-MySQLdb
- Flask-CORS
- Flask-RESTful
- PyMySQL
- Flasgger

### Passos para Execução

1. **Configuração do Banco de Dados MySQL**:
   - Configure o host, porta, usuário, senha e nome do banco de dados no arquivo `app.py`.
   - Certifique-se de que o serviço MySQL esteja em execução e acessível na configuração fornecida.

2. **Instalação de Dependências**:
   - No diretório do projeto, crie um ambiente virtual Python.
   - Instale as dependências do projeto usando o comando `pip install -r requirements.txt`.

3. **Execução do Backend**:
   - Execute o arquivo `app.py` usando o comando `python app.py`.
   - O servidor Flask será iniciado e estará disponível em `http://localhost:5000`.

### Endpoints da API

- **Documentação Swagger**: Acesse `http://localhost:5000/apidocs` para ver a documentação interativa da API, gerada automaticamente pelo Swagger.

## Estrutura do Projeto

- **`app.py`**: Contém a lógica principal do backend, incluindo endpoints e interações com o banco de dados.
- **`templates/`**: Contém os modelos HTML para as páginas da web.
- **`documentation/`**: Contém arquivos de especificação Swagger para documentação da API.

## Dockerização

O backend e o banco de dados MySQL estão configurados para serem executados em contêineres Docker. O arquivo `docker-compose.yml` define os serviços e configurações necessários para a execução do sistema.

### Execução com Docker

1. **Construção das Imagens**:
   - No diretório do projeto, execute `docker-compose build` para construir as imagens do backend e do banco de dados.

2. **Iniciar Serviços**:
   - Execute `docker-compose up` para iniciar os serviços em contêineres Docker.
   - O backend estará acessível em `http://localhost:5000`.

## Observações Importantes

- Certifique-se de proteger informações sensíveis, como chaves de acesso ao banco de dados e chaves de sessão, em ambientes de produção.
- Este README fornece uma visão geral básica do backend. Para informações detalhadas sobre endpoints, parâmetros e respostas, consulte a documentação Swagger fornecida pela API em `http://localhost:5000/apidocs`.
