from flask import Flask, render_template, request, redirect, session, flash, url_for

class Musica:
    def __init__(self, nome, cantorBandaGrupo, genero):
        self.nome = nome
        self.cantorBandaGrupo = cantorBandaGrupo
        self.genero = genero
musica01 = Musica('Musica', 'Docara', 'top')
musica02 = Musica('Musica', 'Docara', 'top')
musica03 = Musica('Musica', 'Docara', 'top')
lista = [musica01, musica02, musica03]

class Usuario:
    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha

usuario01 = Usuario("Igor Silva", "igorv.gama", "123")
usuario02 = Usuario("Geraldo Augusto", "gerardo.aug", "admin")

usuarios = {
    usuario01.login : usuario01,
    usuario02.login : usuario02
}

app = Flask(__name__)

app.secret_key = 'igorvjgssecret'

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