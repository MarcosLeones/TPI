from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.data import get_products, insert_product, get_product_by_id, update_product, delete_product
from flaskr.auth import login_required
from flaskr.entities import Producto


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
