from flask import render_template, request, redirect, session, flash, url_for
from models import Musica, Usuario
from musica import db, app

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
    
@app.route('/editar/<int:id>') #Rota de login
def editar(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    musicaBuscada = Musica.query.filter_by(id_musica=id).first()
    return render_template('editar_musica.html',
                           titulo = 'Editar Música',
                           musica = musicaBuscada)

@app.route('/atualizar', methods=['POST', ]) #Rota de login
def atualizar():
    musica = Musica.query.get(request.form['txtId'])
    musica.nome_musica = request.form['txtNome']
    musica.cantor_banda = request.form['txtCantor']
    musica.genero_musica = request.form['txtGenero']
    db.session.add(musica)
    db.session.commit()
    return redirect(url_for('listarMusicas'))

@app.route('/excluir/<int:id>') #Rota de login
def excluir(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    Musica.query.filter_by(id_musica=id).delete()
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