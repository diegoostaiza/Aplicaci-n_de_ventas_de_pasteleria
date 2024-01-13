from django.contrib import admin
from .models import (
    CategoriasProductos,
    Productos,
    Inventario,
    Usuarios,
    Compras,
    DetalleCompra,
)

# Registra tus modelos aquí

@admin.register(CategoriasProductos)
class CategoriasProductosAdmin(admin.ModelAdmin):
    list_display = ('CategoriaID', 'NombreCategoria')

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('ProductoID', 'NombreProducto', 'Descripcion', 'Precio', 'CategoriaID')

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('InventarioID', 'ProductoID', 'CantidadDisponible')

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('UsuarioID', 'NombreUsuario', 'Email')

@admin.register(Compras)
class ComprasAdmin(admin.ModelAdmin):
    list_display = ('CompraID', 'DetalleCompraID' ,'UsuarioID', 'FechaCompra', 'PrecioTotal')

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('DetalleCompraID', 'ProductoID', 'Cantidad', 'PrecioUnitario')

