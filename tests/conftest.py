import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8') ## Interprete de archivo sql

@pytest.fixture # Setear contexto de testing de la aplicación
def app():
    db_fd, db_path = tempfile.mkstemp() ## Archivo temporal que reemplaza la carpeta instance

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    }) ## Mock app con el nuevo path de la db

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture # Setear contexto de testing para el cliente
def client(app):
    return app.test_client()


@pytest.fixture # Setear contexto de testing para el runner
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='usuarioTest', password='testPassword'):
        response = self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

        return response

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)