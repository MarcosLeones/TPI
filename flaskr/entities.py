class Usuario:
    def __init__(self, cuit, usuario, password, email, nombre, apellido, rol):
        self.cuit=cuit
        self.usuario=usuario
        self.password=password
        self.email=email
        self.nombre=nombre
        self.apellido=apellido
        self.rol=rol


class Producto:
    def __init__(self, nombre, descripcion, precio, iva, imagen='', stock=0):
        self.nombre=nombre
        self.descripcion=descripcion
        self.precio=precio
        self.iva=iva
        self.imagen=imagen
        self.stock=stock


class Venta:
    def __init__(self, cliente, fecha):
        self.cliente=cliente
        self.fecha=fecha
        self.detalles = []

class DetalleVenta:
     def __init__(self,  producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        