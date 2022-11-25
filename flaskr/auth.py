import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.entities import Usuario
from flaskr.data import insert_user, get_user, get_user_by_cuit

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        cuit = request.form['cuit']
        usuario = request.form['usuario']
        password = request.form['password']
        email = request.form['email']
        nombre  = request.form['nombre']
        apellido = request.form['apellido']
        rol = 1
               
        error = None

        if not cuit:
            error = 'CUIT requerido.'
        elif not usuario:
            error = 'Usuario requerido.'
        elif not password:
            error = 'Password requerido.'
        elif not email:
            error = 'e-mail requerido.'
        elif not nombre:
            error = 'Nombre requerido.'
        elif not apellido:
            error = 'Apellido requerido.'

        u = Usuario(cuit, usuario, password, email, nombre, apellido, rol)

        if error is None:
            try:
                insert_user(u)
            except:
                error = 'Ha ocurrido un error'
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['cuit']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_cuit(user_id)



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view