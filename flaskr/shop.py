from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flaskr.data import get_products, insert_product, get_product_by_id, update_product, delete_product, save_sale, get_sales, get_sales_by_user
from flaskr.auth import login_required
from flaskr.entities import Producto, Venta, DetalleVenta
from datetime import datetime



bp = Blueprint('shop', __name__)

@bp.route('/')
def index():
    productos = get_products()
    return render_template('shop/index.html', productos=productos)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        iva = request.form['iva']
        imagen= request.form['imagen']
        stock = request.form['stock']

        error = None


        if not nombre:
            error = 'Nombre requerido.'
        elif not descripcion:
            error = 'Descripción requerido.'
        elif not precio:
            error = 'Precio requerido.'
        elif not iva:
            error = 'IVA requerido.'

        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, iva=iva, imagen=imagen, stock=stock)

        if error is not None:
            flash(error)
        else:
            insert_product(producto)
            return redirect(url_for('shop.index'))

    return render_template('shop/create.html')



def get_product(id):
    product = get_product_by_id(id)

    if product is None:
        abort(404, f"Product id {id} doesn't exist.")

    return product


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_product_by_id(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        iva = request.form['iva']
        imagen= request.form['imagen']
        stock = request.form['stock']
        error = None

        if not nombre:
            error = 'Nombre requerido.'
        elif not descripcion:
            error = 'Descripción requerido.'
        elif not precio:
            error = 'Precio requerido.'
        elif not iva:
            error = 'IVA requerido.'

        p = Producto(nombre=nombre, descripcion=descripcion, precio=precio, iva=iva, imagen=imagen, stock=stock)
        if error is not None:
            flash(error)
        else:
            update_product(p, id)
            return redirect(url_for('shop.index'))

    return render_template('shop/update.html', product=product)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_product_by_id(id)
    delete_product(id)
    return redirect(url_for('shop.index'))



@bp.route('/<int:id>/add_to_cart', methods=('GET', 'POST'))
@login_required
def add_to_cart(id):
    product = get_product_by_id(id)

    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        error = None

        if cantidad > product['stock'] or cantidad <= 0:
            error = 'Cantidad Inválida.'

        
        if error is not None:
            flash(error)
        else:

            subtotal = float(product['precio']) * cantidad * ((float(product['iva']) / 100) + 1)

            detalle_actual = {"id_producto" : product['id'], "nombre" : product['nombre']
            ,"precio" : product['precio'], "iva" : product['iva'], "cantidad": cantidad, "subtotal" : subtotal}

            if 'detalles' in session:         
                detalles = session['detalles']    
                detalles.extend([detalle_actual])  
                session['detalles'] = detalles
                total = session['total']
                total += subtotal
                session['total'] = total
            else:
                session['detalles'] = [detalle_actual]
                session['total'] = subtotal

            return redirect(url_for('shop.show_cart'))

    return render_template('shop/add_to_cart.html', product=product)


@bp.route('/cart', methods=('GET', 'POST'))
@login_required
def show_cart():

    return render_template('shop/cart.html')



@bp.route('/clear_cart')
@login_required
def clear_cart():

    session['detalles'] = []
    session['total'] = 0

    return redirect(url_for('shop.index'))


    

@bp.route('/confirm_purchase', methods=('POST',))
@login_required
def confirm_purchase():

    error = validate_stock()

    if error is not None:
        flash(error)
        return redirect(url_for('shop.show_cart'))
    
    else:
        register_sale()
        session['detalles'] = []
        session['total'] = 0

        return redirect(url_for('shop.index'))




def validate_stock():
    details = session['detalles']
    for detail in details:
        id = detail['id_producto']
        quantity = detail['cantidad']
        product = get_product(id)
        if product['stock'] < int(quantity):
            return 'Stock insuficiente para el artículo ' + product['nombre']
    return None


def register_sale():
    venta = Venta(cliente=g.user['cuit'], fecha=datetime.now())
    detalles = []
    ds = session['detalles']
    total = 0
    item = 0
    for d in ds:
        item += 1
        p = get_product(d['id_producto'])
        producto = Producto(nombre=p['nombre'], descripcion=p['descripcion'], precio=p['precio'], iva=p['iva'], imagen=p['imagen'], stock=p['stock'])
        detalle = DetalleVenta(item=item, producto=d['id_producto'], cantidad=d['cantidad'])
        total += float(p['precio']) * int(d['cantidad']) * ((float(p['iva']) /100) +1)
        venta.detalles.append(detalle)
    venta.total = total
    save_sale(venta)

    
@bp.route('/sales')
@login_required
def show_sales():
    if g.user['rol'] == 0:
        ventas = get_sales()
        return render_template('shop/sales.html', ventas=ventas)
    else:
        return redirect(url_for('shop.index'))


@bp.route('/purchases')
@login_required
def show_purchases():
    if g.user['rol'] == 1:
        compras = get_sales_by_user(g.user['cuit'])
        return render_template('shop/purchases.html', compras=compras)
    else:
        return redirect(url_for('shop.index'))
