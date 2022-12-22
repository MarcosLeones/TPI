import logging

logger = logging.getLogger()

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={
          'cuit': 12345678,
          'usuario': 'testUser',
          'password': 'testPassword',
          'email': 'testEmail@gmail.com',
          'nombre': 'testNombre',
          'apellido': 'testApellido',
          'rol': 1
        }
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM usuarios WHERE usuario = 'a'",
        ).fetchone() is None


# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('', '', b'Username is required.'),
#     ('a', '', b'Password is required.'),
#     ('test', 'test', b'already registered'),
# ))
# def test_register_validate_input(client, username, password, message):
#     response = client.post(
#         '/auth/register',
#         data={'username': username, 'password': password}
#     )
#     assert message in response.data
