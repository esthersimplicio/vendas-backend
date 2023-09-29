from flask import Flask, jsonify, render_template, session, url_for, redirect, request, flash
from flask_cors import CORS 
from flask_restful import Api, Resource
from flask_mysqldb import MySQL
import pymysql
from flasgger import Swagger, swag_from
import time

app = Flask(__name__)

app.secret_key = 'admin'

app.config['MYSQL_HOST'] = 'db' #localhost: localhost, docker: db
app.config['MYSQL_PORT'] = '3326' #docker = 3326, localhost = 3306
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'S1SViageN5' #localhost: root, docker: S1SViageN5
app.config['MYSQL_DB'] = 'site_vendas'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

template = 'documentation/swagger.yml'
CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})
swagger = Swagger(app, template_file=template)


db = MySQL(app)

while True:
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        print("Conexão com o servidor MySQL estabelecida com sucesso!")
        break  # Se a conexão for bem-sucedida, saia do loop
    except pymysql.MySQLError as e:
        print("Não foi possível estabelecer conexão com o servidor MySQL:", str(e))
        print("Tentando novamente em 5 segundos...")
        time.sleep(5)  # Espere por 5 segundos antes de tentar novamente

try:
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )
    print("Conexão com o servidor MySQL estabelecida com sucesso!")
except pymysql.MySQLError as e:
    print("Não foi possível estabelecer conexão com o servidor MySQL:", str(e))

@app.route('/')
def index():
    return redirect(url_for('signin_form'))

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('signin.html')

@app.route('/signin', methods=['POST'])
@swag_from('documentation/api/signin.yml')
def signin():
    try:
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM signup WHERE email = %s AND senha = %s", (email, senha))
            usuario = cursor.fetchone()
            cursor.close()

            if usuario:
                session['usuario_id'] = usuario[0]
                flash('Login realizado com sucesso!', 'success')

                # Redireciona o usuário para a página "catalago"
                return redirect(url_for('catalago'))

            else:
                flash('Credenciais inválidas. Tente novamente.', 'danger')
                return render_template('signin.html')

    except pymysql.Error as e:
        print("Erro durante o login:", str(e))
        flash('Erro durante o login. Tente novamente mais tarde.', 'danger')
        return render_template('signin.html')

    # Se a solicitação for POST e não for bem-sucedida, retorne o formulário de login
    return render_template('signin.html')



     
@app.route('/catalago')
def catalago():
    if 'usuario_id' in session:  # Verifica se o usuário está logado na sessão
        usuario_id = session['usuario_id']
        
        # Verifica se o usuário está cadastrado no banco de dados
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM signup WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            return render_template('catalago.html')
        else:
            flash('Usuário não encontrado no banco de dados.', 'danger')
            return redirect(url_for('signin_form'))
    else:
        flash('Faça login para acessar a página de catalago', 'danger')
        return redirect(url_for('signin_form'))


# Rota para solicitações GET
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

# Rota para solicitações POST
@app.route('/signup', methods=['POST'])
@swag_from('documentation/api/signup.yml')
def signup():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        senha = request.form['senha']

        cursor = connection.cursor()
        cursor.execute("INSERT INTO signup (nome, telefone, email, senha) VALUES (%s, %s, %s, %s)", (nome, telefone, email, senha))
        connection.commit()
        cursor.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/perfil')
def perfil():
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM signup WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            return render_template('perfil.html', usuario=usuario)
        else:
            flash('Usuário não encontrado no banco de dados.', 'danger')
            return redirect(url_for('signin'))
    else:
        flash('Faça login para acessar a página de perfil.', 'danger')
        return redirect(url_for('signin'))


# Rota para solicitações GET
@app.route('/editar_usuario', methods=['GET'])
def editar_usuario_form():
    if 'usuario_id' in session:
        # Obtém o ID do usuário da sessão
        usuario_id = session['usuario_id']

        # Consulte o banco de dados para obter os dados do usuário
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM signup WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            return render_template('editar_usuario.html', usuario=usuario)
        else:
            flash('Usuário não encontrado.', 'danger')

    # Se o usuário não estiver autenticado, redirecioná-lo para a página de login
    flash('Faça login para editar suas informações.', 'danger')
    return redirect(url_for('signin'))

# Rota para solicitações POST
@app.route('/editar_usuario', methods=['POST'])
@swag_from('documentation/api/editar_usuario.yml')
def editar_usuario():
    if 'usuario_id' in session:
        # Obtém o ID do usuário da sessão
        usuario_id = session['usuario_id']

        if request.method == 'POST':
            # Obtém os dados do formulário
            nome = request.form.get('nome')
            telefone = request.form.get('telefone')
            email = request.form.get('email')
            senha = request.form.get('senha')

            try:
                # Conecte-se ao banco de dados usando Flask-MySQLdb (certifique-se de configurar a conexão corretamente)
                cursor = connection.cursor()

                # Construa a consulta SQL dinamicamente com base nos campos fornecidos
                query = "UPDATE signup SET"
                values = []

                if nome:
                    query += " nome = %s,"
                    values.append(nome)

                if telefone:
                    query += " telefone = %s,"
                    values.append(telefone)

                if email:
                    query += " email = %s,"
                    values.append(email)

                if senha:
                    query += " senha = %s,"
                    values.append(senha)

                # Remova a vírgula extra no final da consulta
                query = query.rstrip(',') + " WHERE id_usuario = %s"
                values.append(usuario_id)

                # Execute a consulta SQL
                cursor.execute(query, tuple(values))

                # Commit para aplicar a atualização no banco de dados
                connection.commit()

                # Feche o cursor
                cursor.close()

                # Redirecione o usuário de volta à página de perfil do usuário
                flash('Informações do usuário atualizadas com sucesso!', 'success')
                return redirect(url_for('perfil'))

            except Exception as e:
                # Em caso de erro, reverta qualquer alteração e exiba uma mensagem de erro
                connection.rollback()
                flash('Erro ao atualizar informações do usuário. Tente novamente.', 'danger')
                return redirect(url_for('perfil'))

    # Se o usuário não estiver autenticado, redirecioná-lo para a página de login
    flash('Faça login para editar suas informações.', 'danger')
    return redirect(url_for('signin'))

            
  
class DeletarUsuario(Resource):
    @swag_from('documentation/api/delete.yml')
    def delete(self):
        try:
            # Obtenha o ID do usuário a ser excluído a partir dos dados da sessão ou da solicitação (dependendo da autenticação)
            usuario_id = session.get('usuario_id')  # Substitua isso pelo seu método de autenticação

            if not usuario_id:
                return {'message': 'Usuário não autenticado'}, 401

            # Conecte-se ao banco de dados
            cursor = connection.cursor()

            # Exclua o usuário da tabela 'cadastro' (substitua 'cadastro' pelo nome da sua tabela)
            cursor.execute("DELETE FROM signup WHERE id_usuario = %s", (usuario_id,))

            # Commit para aplicar a exclusão no banco de dados
            connection.commit()

            # Feche o cursor
            cursor.close()

            # Remova o ID do usuário da sessão após a exclusão
            session.pop('usuario_id', None)

            return {'message': 'Conta de usuário excluída com sucesso'}, 200

        except Exception as e:
            return {'error': str(e)}, 500

api = Api(app)  # Defina a instância da classe api após a criação do aplicativo Flask

# Adicione a rota à API
api.add_resource(DeletarUsuario, '/deletar_usuario')




if __name__ == "__main__":
    app.run(debug=True, port=5000)
