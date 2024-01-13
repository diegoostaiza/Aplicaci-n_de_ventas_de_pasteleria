from django.urls import path
from . import views


urlpatterns = [
   path('',views.inicio , name="inicio"),
   path('productos/',views.productos , name="productos"),
   path('logout/',views.salir , name="salir"),
   path('registro/', views.registrarse, name='registro'),
   # path('registro/',views.registro , name="registro"),
  
]
