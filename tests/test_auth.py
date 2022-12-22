import logging

logger = logging.getLogger()

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200  # Validar que register es un path disponible
    response = client.post( # Request con datos de testeo sobre la testing_db
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

    assert response.headers["Location"] == "/auth/login" # Validar que redirigió a login post crear el usuario

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM usuarios WHERE cuit = 12345678", # Validar que el usuario está registrado en la instancia de la db
        ).fetchone() is not None

@pytest.mark.parametrize(
  ('cuit','usuario','password','email','nombre','apellido','rol','message'), # Todos los campos, más el mensaje de error que debe mostrar y validar
  (
    ('','','','','','','', b'CUIT requerido.'),
    (12345678,'','','','','','', b'Usuario requerido.'),
    (12345678,'testUser','','','','','', b'Password requerido.'),
    (12345678,'testUser','testPassword','','','','', b'e-mail requerido.'),
    (12345678,'testUser','testPassword','testEmail@gmail.com','','','', b'Nombre requerido.'),
    (12345678,'testUser','testPassword','testEmail@gmail.com','testNombre','','', b'Apellido requerido.'),
    (12345678,'testUser','testPassword','testEmail@gmail.com','testNombre','testApellido','', b'Rol requerido.'),
  )
)
def test_register_validate_input(client, cuit, usuario, password, email, nombre, apellido, rol, message):
    response = client.post(
        '/auth/register',
        data={
          'cuit': cuit,
          'usuario': usuario,
          'password': password,
          'email': email,
          'nombre': nombre,
          'apellido': apellido,
          'rol': rol
        }
    )
    assert message in response.data
