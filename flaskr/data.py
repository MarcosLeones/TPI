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
        ' WHERE id = ?',
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


def save_sale(sale):
    db = get_db()
    #Guardar cabecera de venta
    cursor = db.execute(
            "INSERT INTO ventas (cliente, fecha, total) VALUES (?, ?, ?)",
            (sale.cliente, sale.fecha, sale.total)
        )
    #db.commit()
    
    sale_number = cursor.lastrowid

    #Guardar detalles de venta
    insert = "INSERT INTO detalle_ventas (numero, item, producto, cantidad) VALUES "
    for detail in sale.detalles:
        insert += " (" + str(sale_number) + ", " + str(detail.item) + ", " + str(detail.producto) + ", " + str(detail.cantidad) + "),"   
    insert = insert[:-1]
    db.execute(insert)
    #db.commit()

    #Actualizar stock de productos
    for detail in sale.detalles:
        update = "UPDATE productos SET stock = stock - " + str(detail.cantidad) + " WHERE id = " + str(detail.producto)  
        print(update)
        db.execute(update)
    
    db.commit()


def get_sales():
    return get_db().execute(
        'SELECT v.fecha as fecha, v.total as total, u.cuit as cuit, u.nombre as nombre, u.apellido as apellido FROM ventas v INNER JOIN usuarios u ON v.cliente = u.cuit'
    ).fetchall()


def get_sales_by_user(cuit):
    return get_db().execute(
        ' SELECT v.numero as numero, v.fecha as fecha, p.nombre as producto, p.precio as precio, dv.cantidad as cantidad, (dv.cantidad * p.precio) as subtotal, v.total as total '
        + ' FROM ventas v '
        + ' INNER JOIN  detalle_ventas dv on v.numero = dv.numero ' 
        + ' INNER JOIN productos p on dv.producto = p.id '
        + ' WHERE v.cliente = ' + str(cuit)
        + ' ORDER BY v.numero '
    ).fetchall()