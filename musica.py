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
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_usuario = db.Column(db.String(50), nullable = False)
    login_usuario = db.Column(db.String(20), nullable = False)
    senha_usuario = db.Column(db.String(15), nullable = False)
    def __repr__(self):
        return '<Name %r>' %self.name

@app.route('/') #Rota principal
def listarMusicas():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
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
    novaMusica = Musica(nome, cantor, genero)
    lista.append(novaMusica)
    return redirect(url_for('listarMusicas'))

@app.route('/login') #Rota de login
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST', ]) # Autenticacao
def autenticar():
    if request.form['txtLogin'] in usuarios:
        usuarioEncontrado = usuarios[request.form['txtLogin']]
        if request.form['txtSenha'] == usuarioEncontrado.senha:
            session['usuario_logado'] = request.form['txtLogin']
            flash(f"Usuario {usuarioEncontrado.login} logado com sucesso! Seja bem vindo {usuarioEncontrado.nome}")
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