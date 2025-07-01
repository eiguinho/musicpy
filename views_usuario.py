from flask import render_template, request, redirect, session, flash, url_for
from musica import app
from definicoes import FormularioUsuario

@app.route('/login') #Rota de login
def login():
    form = FormularioUsuario()
    return render_template('login.html', form= form)


@app.route('/autenticar', methods=['POST', ]) # Autenticacao
def autenticar():
    from models import Usuario
    form = FormularioUsuario(request.form)
    usuario = Usuario.query.filter_by(login_usuario = form.usuario.data).first()
    if usuario:
        if form.senha.data == usuario.senha_usuario:
            session['usuario_logado'] = usuario.login_usuario
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