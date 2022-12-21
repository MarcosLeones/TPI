
from entities import Usuario
def test_usuario():
  """
  GIVEN el modelo de usuario
  WHEN un usuario es creado
  THEN validar que los campos sean correctos
  """
  cuit = '20-39285009-8'
  nick = 'testerman'
  password = 'admintesterman'
  correo = 'testerman@gmail.com'
  nombre = 'tester'
  apellido = 'man'
  rol = 'Cliente'

  usuario = Usuario(cuit, nick, password, correo, nombre, apellido, rol)

  assert usuario.cuit == cuit
  assert usuario.usuario == nick
  assert usuario.password == password
  assert usuario.email == correo
  assert usuario.nombre == nombre
  assert usuario.apellido == apellido
  assert usuario.rol == rol # Y rol debería ser al menos: OP1 | OP2 ...

test_usuario()