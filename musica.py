from flask import Flask, render_template, request, redirect

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

@app.route('/')
def listarMusicas():
    return render_template('lista_musicas.html',
                           titulo = 'Aprendendo do inicio',
                           musicas = lista)

@app.route('/cadastrar')
def cadastrarMusica():
    return render_template('cadastra_musica.html')

@app.route('/adicionar', methods = ['POST', ])
def adicionar_musica():
    nome = request.form['txtNome']
    cantor = request.form['txtCantor']
    genero = request.form['txtGenero']

    novaMusica = Musica(nome, cantor, genero)
    lista.append(novaMusica)

    return redirect("/")

@app.route('/login')
def login():
    return render_template('login.html')

app.run(debug=True)