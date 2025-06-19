import os

SECRET_KEY = 'igorvjgssecret'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'playmusica'
    )

UPLOADS_PASTA = os.path.dirname(os.path.abspath(__file__)) + '/uploads'