from flaskr.db import get_db

def test_create(client, app):
    client.post(
        '/create',
        data={
          'nombre': 'Exprimidor fancy',
          'descripcion': 'No sirve para nada',
          'precio': 1894.00,
          'iva': 21.00,
          'imagen': 'imageText',
          'stock': 100,
        }
    )

    with app.app_context():
        db = get_db()
        assert db.execute('SELECT * FROM productos WHERE nombre="Exprimidor fancy"').fetchone() is not None

# TBD