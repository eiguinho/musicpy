from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = 'igorvjgssecret'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'playmusica'
    )

db = SQLAlchemy(app)

class Musica(db.Model):
    id_musica = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_musica = db.Column(db.String(50), nullable = False)
    cantor_banda = db.Column(db.String(50), nullable = False)
    genero_musica = db.Column(db.String(50), nullable = False)
    def __repr__(self):
        return '<Name %r>' %self.name

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_usuario = db.Column(db.String(50), nullable = False)
    login_usuario = db.Column(db.String(20), nullable = False)
    senha_usuario = db.Column(db.String(15), nullable = False)
    def __repr__(self):
        return '<Name %r>' %self.name

@app.route('/') #Rota principal
def listarMusicas():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    lista = Musica.query.order_by(Musica.id_musica)
    return render_template('lista_musicas.html',
                           titulo = 'Musicas Cadastradas',
                           musicas = lista)

@app.route('/cadastrar') #Rota para cadastrar musica
def cadastrarMusica():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('cadastra_musica.html',
                           titulo = "Cadastrar Música")

@app.route('/adicionar', methods = ['POST', ]) # Adicao de musicas
def adicionar_musica():
    nome = request.form['txtNome']
    cantor = request.form['txtCantor']
    genero = request.form['txtGenero']
    musica = Musica.query.filter_by(nome_musica=nome).first()
    if musica:
        flash("Musica já está cadastrada!")
        return redirect(url_for('listarMusicas'))
    else:
        nova_musica = Musica(nome_musica = nome, cantor_banda = cantor, genero_musica = genero)
        db.session.add(nova_musica)
        db.session.commit()
        return redirect(url_for('listarMusicas'))

@app.route('/login') #Rota de login
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST', ]) # Autenticacao
def autenticar():
    usuario = Usuario.query.filter_by(login_usuario = request.form['txtLogin']).first()
    if usuario:
        if request.form['txtSenha'] == usuario.senha_usuario:
            session['usuario_logado'] = request.form['txtLogin']
            flash(f"Usuario {usuario.login_usuario} logado com sucesso! Seja bem vindo {usuario.nome_usuario}")
            return redirect(url_for('listarMusicas'))
        else:
            flash("Senha incorreta!")
            return redirect(url_for('login'))
    else:
        flash("Acesso Negado! Credenciais invalidas!")
        return redirect(url_for('login'))

@app.route('/sair') #Rota de logout
def sair():
    session['usuario_logado'] = None
    return redirect(url_for('login'))
    
app.run(debug=True)