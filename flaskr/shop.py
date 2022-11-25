from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.data import get_products, insert_product
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


"""
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
"""