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

app = Flask(__name__)

app.secret_key = 'igorvjgssecret'

@app.route('/')
def listarMusicas():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('lista_musicas.html',
                           titulo = 'Musicas Cadastradas',
                           musicas = lista)

@app.route('/cadastrar')
def cadastrarMusica():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('cadastra_musica.html',
                           titulo = "Cadastrar Música")

@app.route('/adicionar', methods = ['POST', ])
def adicionar_musica():
    nome = request.form['txtNome']
    cantor = request.form['txtCantor']
    genero = request.form['txtGenero']
    novaMusica = Musica(nome, cantor, genero)
    lista.append(novaMusica)
    return redirect(url_for('listarMusicas'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['txtSenha'] == 'admin':
        session['usuario_logado'] = request.form['txtLogin']
        flash("Usuario logado com sucesso!")
        return redirect(url_for('listarMusicas'))
    else:
        flash("Acesso Negado! Credenciais invalidas!")
        return redirect(url_for('login'))

@app.route('/sair')
def sair():
    session['usuario_logado'] = None
    return redirect(url_for('login'))
    
app.run(debug=True)