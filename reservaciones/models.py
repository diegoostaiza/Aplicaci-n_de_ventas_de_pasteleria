from django.db import models
from django.contrib.auth.models import User
# Modelos para la base de datos


class CategoriasProductos(models.Model):
    CategoriaID = models.AutoField(primary_key=True)
    NombreCategoria = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.NombreCategoria  
    
class SubCategoriaProductos(models.Model):
    SubcategoriaID = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    CategoriaID = models.ForeignKey(CategoriasProductos, on_delete=models.RESTRICT)
    def __str__(self):
        return self.Descripcion
    

class Productos(models.Model):
    ProductoID = models.AutoField(primary_key=True)
    NombreProducto = models.CharField(max_length=50)
    Descripcion = models.TextField(null=True)
    imagen = models.ImageField(upload_to="productos" , null = True)
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    CategoriaID = models.ForeignKey(CategoriasProductos, on_delete=models.RESTRICT)
    SubcategoriaID = models.ForeignKey(SubCategoriaProductos, on_delete=models.RESTRICT)
    def __str__(self):
        return self.NombreProducto

    
class Inventario(models.Model):
    InventarioID = models.AutoField(primary_key=True)
    ProductoID = models.ForeignKey(Productos, on_delete=models.RESTRICT)
    CantidadDisponible = models.IntegerField()

    def __str__(self):
        return f"{self.ProductoID} - Cantidad: {self.CantidadDisponible}"


class Usuarios(models.Model):
    UsuarioID = models.AutoField(primary_key=True)
    NombreUsuario = models.CharField(max_length=10)
    Nombre = models.CharField(max_length=20)
    Apellido = models.CharField(max_length=20)
    Contraseñauno = models.CharField(max_length=50)
    Contrados = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    USERNAME_FIELD = 'NombreUsuario'
    def __str__(self):
        return self.NombreUsuario






class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad_productos = models.IntegerField(default=0)
    productos = models.ManyToManyField('Productos')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    fecha_entrega = models.DateField()
    hora_entrega = models.TimeField()
    cantidad = models.IntegerField(default=0)  # Nueva campo para la cantidad de este producto en el carrito

    def __str__(self):
        return f"{self.producto.NombreProducto} ({self.cantidad} unidades) en Carrito de {self.carrito.usuario.username}"


class Entrega(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=10)  # Número de teléfono de 10 caracteres

    def __str__(self):
        return f"Entrega para {self.usuario.username}"

class EntregaDomicilio(models.Model):
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, primary_key=True)
    tipo_entrega = models.CharField(max_length=10, choices=[('domicilio', 'Entrega a domicilio')])
    provincia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    direccion_entrega = models.TextField(blank=True, null=True)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"Entrega domicilio para {self.entrega.usuario.username}"

class EntregaTienda(models.Model):
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, primary_key=True)
    tipo_entrega = models.CharField(max_length=10, choices=[('tienda', 'Entrega en tienda')])

    def __str__(self):
        return f"Entrega tienda para {self.entrega.usuario.username}"
    


class DetalleCompra(models.Model):
    DetalleCompraID = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    precioTotal = models.DecimalField(max_digits=10, decimal_places=2)
   
    id_transaccion_stripe = models.CharField(max_length=100, blank=True, null=True)
    estado_pago = models.CharField(max_length=20, blank=True, null=True)
   
    def __str__(self):
        return f"Detalle #{self.DetalleCompraID} - Producto: {self.carrito.productos.all()}"


class Compras(models.Model):
    CompraID = models.AutoField(primary_key=True)
    DetalleCompraID =   models.ForeignKey(DetalleCompra, on_delete=models.RESTRICT, null=True)
    FechaCompra = models.DateField()