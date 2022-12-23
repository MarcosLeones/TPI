/* Populo tablas con data de testing */

INSERT INTO usuarios (cuit,usuario,password,email,nombre,apellido,rol)
VALUES
  (12345678, 'test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'email@test.com','nombreTest','apellidoTest', 1);

INSERT INTO productos (nombre,descripcion,precio,iva,imagen,stock)
VALUES
  ('Exprimidor fancy', 'No sirve para nada', 1894.00, 21.00,'imageText',100);
