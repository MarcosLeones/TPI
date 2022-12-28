import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db() # Comparo que cada instancia de la conexión es la misma post llamado de la función.

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1') # Sentencia arbitraria

    assert 'closed' in str(e.value) # Asegurar que la instancia de base de datos cierra luego de ejecutar una sentencia.

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called