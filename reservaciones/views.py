from django.shortcuts import render , redirect
from .models import Productos
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def inicio(request):
    producto = Productos.objects.all()
    productoPostre = Productos.objects.filter(CategoriaID = 2)
    return render(request , 'index.html', {'productos': producto ,
                                           'productoPostre': productoPostre} )


@login_required
def productos(request):
    return render(request ,'productos.html')



def salir(request):
    logout(request)
    return redirect('inicio')

def registrarse(request):
    return render(request ,'registration/registro.html')
  

# def login(request):
#     return render(request ,'registration/login.html')


# def registro(request):
#     return render(request ,'registration/registro.html')