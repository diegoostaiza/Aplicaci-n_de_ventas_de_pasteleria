from django.db import models

# Modelos para la base de datos

class CategoriasProductos(models.Model):
    CategoriaID = models.AutoField(primary_key=True)
    NombreCategoria = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.NombreCategoria


class Productos(models.Model):
    ProductoID = models.AutoField(primary_key=True)
    NombreProducto = models.CharField(max_length=50)
    Descripcion = models.TextField(null=True)
    imagen = models.ImageField(upload_to="productos" , null = True)
    Precio = models.DecimalField(max_digits=10, decimal_places=2)
    CategoriaID = models.ForeignKey(CategoriasProductos, on_delete=models.RESTRICT)

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
    NombreUsuario = models.CharField(max_length=50)
    Contraseña = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)

    def __str__(self):
        return self.NombreUsuario



class DetalleCompra(models.Model):
    DetalleCompraID = models.AutoField(primary_key=True)
    ProductoID = models.ForeignKey(Productos, on_delete=models.RESTRICT)
    Cantidad = models.IntegerField()
    PrecioUnitario = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_precio_unitario(self):
        # Calcula el precio unitario multiplicando la cantidad por el precio del producto
        self.PrecioUnitario = self.ProductoID.Precio * self.Cantidad

    def save(self, *args, **kwargs):
        # Antes de guardar, asegúrate de calcular el precio unitario
        self.calcular_precio_unitario()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle #{self.DetalleCompraID} - Producto: {self.ProductoID.NombreProducto}"


class Compras(models.Model):
    CompraID = models.AutoField(primary_key=True)
    DetalleCompraID = models.ForeignKey(DetalleCompra, on_delete=models.RESTRICT, null=True)
    UsuarioID = models.ForeignKey(Usuarios, on_delete=models.RESTRICT)
    FechaCompra = models.DateField()
    PrecioTotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.CompraID} - Usuario: {self.UsuarioID}"
