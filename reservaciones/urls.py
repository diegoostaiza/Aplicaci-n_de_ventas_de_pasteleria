from django.urls import path
from . import views
from django.contrib.auth.views import LoginView , LogoutView


urlpatterns = [
   path('',views.inicio , name="inicio"),
   path('productos/',views.productos , name="productos"),
   path('logout/',views.salir , name="salir"),
   path('login/',LoginView.as_view(template_name = 'registration/login.html') , name="login"),
   path('registro/', views.registrarse, name='registro'),
   path('productos/categoria/<int:subcategoria_id>/', views.productos_por_subcategoria, name='productosCategoria'),
   path('productos/<int:producto_id>/', views.producto_seleccionado , name='productoSelecionado'),
   path('productos/carrito', views.ver_carrito , name='carrito'),
   path('productos/carrito/agg', views.agregarProducto , name='agregar_producto'),
   path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
   path('eliminar_producto/carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
   path('productos/carrito/direccion', views.direccion_compra , name='direccion'),
   path('productos/carrito/direccion/pago', views.pago , name='pago'),
   path('productos/carrito/direccion/factura', views.generar_factura_pdf , name='pdf'),
   path('productos/carrito/direccion/pago/confirmacion', views.confirmacion_pago , name='confirmacion_pago'),
]
