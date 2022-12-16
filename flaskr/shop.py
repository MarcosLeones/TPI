from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flaskr.data import get_products, insert_product, get_product_by_id, update_product, delete_product
from flaskr.auth import login_required
from flaskr.entities import Producto, Venta, DetalleVenta



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

        dv = DetalleVenta(producto = product['id'], cantidad = cantidad)
        
        if error is not None:
            flash(error)
        else:

            subtotal = float(product['precio']) * float(product['iva']) * cantidad

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


    

@bp.route('/confirm_purchase', methods=('GET', 'POST'))
@login_required
def confirm_purchase():

    return redirect(url_for('shop.index'))