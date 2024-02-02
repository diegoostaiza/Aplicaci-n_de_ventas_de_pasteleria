from django.contrib import admin
from .models import (
    CategoriasProductos,
    SubCategoriaProductos,
    Productos,
    Inventario,
    Usuarios,
    Carrito,
    ItemCarrito,
    Entrega,
    EntregaDomicilio,
    EntregaTienda,
    DetalleCompra,
    Compras,
)

class ProductosAdmin(admin.ModelAdmin):
    list_display = ('NombreProducto', 'Precio', 'CategoriaID', 'SubcategoriaID')

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('ProductoID', 'CantidadDisponible')

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('NombreUsuario', 'Nombre', 'Apellido', 'Email')

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cantidad_productos')

class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'fecha_entrega', 'hora_entrega', 'cantidad')


class EntregaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono')

class EntregaDomicilioAdmin(admin.ModelAdmin):
    list_display = ('entrega', 'tipo_entrega', 'provincia', 'ciudad', 'direccion_entrega', 'codigo_postal')

class EntregaTiendaAdmin(admin.ModelAdmin):
    list_display = ('entrega', 'tipo_entrega')


class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('carrito',  'precioTotal' , 'id_transaccion_stripe', 'estado_pago')

class ComprasAdmin(admin.ModelAdmin):
    list_display = ('CompraID', 'DetalleCompraID', 'FechaCompra')

# Registrar tus modelos en el admin
admin.site.register(CategoriasProductos)
admin.site.register(SubCategoriaProductos)
admin.site.register(Productos, ProductosAdmin)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Usuarios, UsuariosAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(ItemCarrito, ItemCarritoAdmin)
admin.site.register(Entrega, EntregaAdmin)
admin.site.register(EntregaDomicilio, EntregaDomicilioAdmin)
admin.site.register(EntregaTienda, EntregaTiendaAdmin)
admin.site.register(DetalleCompra, DetalleCompraAdmin)
admin.site.register(Compras, ComprasAdmin)
