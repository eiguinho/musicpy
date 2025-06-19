from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Musica, Usuario
from musica import db, app
from definicoes import recupera_imagem, deletar_imagem
import time

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
        arquivo = request.files['arquivo']
        pasta_arquivos = app.config['UPLOADS_PASTA']
        nome_arquivo = arquivo.filename
        nome_arquivo = nome_arquivo.split('.')
        extensao = nome_arquivo[len(nome_arquivo)-1]
        momento = time.time()
        nome_completo = f'album{nova_musica.id_musica}_{momento}.{extensao}'
        arquivo.save(f'{pasta_arquivos}/{nome_completo}')
        return redirect(url_for('listarMusicas'))
    
@app.route('/editar/<int:id>') #Rota de login
def editar(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    musicaBuscada = Musica.query.filter_by(id_musica=id).first()
    album = recupera_imagem(id)
    return render_template('editar_musica.html',
                           titulo = 'Editar Música',
                           musica = musicaBuscada,
                           album_musica = album)

@app.route('/atualizar', methods=['POST', ]) #Rota de login
def atualizar():
    musica = Musica.query.get(request.form['txtId'])
    musica.nome_musica = request.form['txtNome']
    musica.cantor_banda = request.form['txtCantor']
    musica.genero_musica = request.form['txtGenero']
    db.session.add(musica)
    db.session.commit()
    arquivo = request.files['arquivo']
    pasta_upload = app.config['UPLOADS_PASTA']
    nome_arquivo = arquivo.filename
    nome_arquivo = nome_arquivo.split('.')
    extensao = nome_arquivo[len(nome_arquivo)-1]
    momento = time.time()
    nome_completo = f'album{musica.id_musica}_{momento}.{extensao}'
    deletar_imagem(musica.id_musica)
    arquivo.save(f'{pasta_upload}/{nome_completo}')
    return redirect(url_for('listarMusicas'))

@app.route('/excluir/<int:id>') #Rota de login
def excluir(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    Musica.query.filter_by(id_musica=id).delete()
    deletar_imagem(id)
    db.session.commit()
    flash("Música excluída com sucesso")
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

@app.route('/uploads/<nome_imagem>') #Rota de
def imagem(nome_imagem):
    return send_from_directory('uploads', nome_imagem)