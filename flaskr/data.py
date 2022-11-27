from flaskr.db import get_db
from flaskr.entities import Usuario, Producto
from werkzeug.security import check_password_hash, generate_password_hash


def insert_user(u):
    db = get_db()
    try:
        db.execute(
                "INSERT INTO usuarios (cuit, usuario, password, email, nombre, apellido, rol) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (u.cuit, u.usuario, generate_password_hash(u.password), u.email, u.nombre, u.apellido, u.rol),
                )
        db.commit()
    except db.IntegrityError:
        error = f"User is already registered."
    

def get_user(usuario, password):
    db = get_db()
    return  db.execute(
            'SELECT * FROM usuarios WHERE usuario = ?', (usuario,)
        ).fetchone()

    
def get_user_by_cuit(cuit):
    return get_db().execute(
            'SELECT * FROM usuarios WHERE cuit = ?', (cuit,)
        ).fetchone()



def get_products():
    return get_db().execute(
        'SELECT * FROM productos'
    ).fetchall()


def insert_product(p):
    db = get_db()
    try:
        db.execute(
                "INSERT INTO productos (nombre, descripcion, precio, iva, imagen, stock) VALUES (?, ?, ?, ?, ?, ?)",
                (p.nombre, p.descripcion, p.precio, p.iva, p.imagen, p.stock),
                )
        db.commit()
    except db.IntegrityError:
        error = f"Product is already registered."


def get_product_by_id(id):
    return get_db().execute(
        'SELECT * FROM productos'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()


def update_product(p,id):
    db = get_db()
    db.execute(
            'UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, iva = ?, imagen = ?, stock = ?'
            ' WHERE id = ?',
            (p.nombre, p.descripcion, p.precio, p.iva, p.imagen, p.stock, id)
        )
    db.commit()

def delete_product(id):
    db = get_db()
    db.execute('DELETE FROM productos WHERE id = ?', (id,))
    db.commit()