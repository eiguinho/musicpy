import os
from musica import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField

class FormularioMusica(FlaskForm):
    nome = StringField('Nome da Música', [validators.DataRequired(), validators.length(min=2,max=50)])
    grupo = StringField('Cantor / Banda / Grupo', [validators.DataRequired(), validators.length(min=2,max=50)])
    genero = StringField('Genero', [validators.DataRequired(), validators.length(min=2,max=50)])
    cadastrar = SubmitField('Cadastrar Música')

class FormularioUsuario(FlaskForm):
    usuario = StringField('Usuário', [validators.DataRequired(),
                                  validators.length(min=2, max=20)])
    senha = PasswordField('Senha', [validators.DataRequired(),
                                    validators.length(min=5, max=15)])
    logar = SubmitField('Entrar')

class FormularioCadastroUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(),
                                           validators.length(min=2, max=50)])
    usuario = StringField('Usuario', [validators.DataRequired(),
                                           validators.length(min=2, max=20)])
    senha = PasswordField('Senha', [validators.DataRequired(),
                                    validators.length(min=6, max=255)])
    cadastrar = SubmitField('Cadastrar Usuário')

def recupera_imagem(id):
    for nome_imagem in os.listdir(app.config['UPLOADS_PASTA']):
        nome = str(nome_imagem)
        nome = nome.split('.')
        if f'album{id}_' in nome[0]:
            return nome_imagem
    return 'default.png' 

def deletar_imagem(id):
    imagem = recupera_imagem(id)
    if imagem != 'default.png':
        os.remove(os.path.join(app.config['UPLOADS_PASTA'], imagem))