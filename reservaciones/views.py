from django.shortcuts import render , redirect,  get_object_or_404 ,HttpResponse
from .models import Productos , CategoriasProductos , SubCategoriaProductos , Inventario , Carrito , ItemCarrito , Entrega , EntregaDomicilio,EntregaTienda ,DetalleCompra
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from .forms import CustomUserCreationForm 
from decimal import Decimal ,ROUND_HALF_UP
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
stripe.api_key = 'sk_test_51OfCOeKesiPT9DY7i36M7OcYO27sfJVieelnEXTEVM03uXp96ydthSpzg0kNhtuRDdi2zsFbgGYkYcg8bZ72KwNe00FC8jWKkS'


def inicio(request):
    producto = Productos.objects.all()
    productoPostre = Productos.objects.filter(CategoriaID = 2)
    return render(request , 'index.html', {'productos': producto ,
                                           'productoPostre': productoPostre} )



def productos(request):
    categorias = CategoriasProductos.objects.all()
    subcategorias = SubCategoriaProductos.objects.all()
    productos = Productos.objects.all()
    contexto = {
        'categorias': categorias,
        'productos':productos,
        'subcategorias': subcategorias,
    }
   
    return render(request, 'productos.html', contexto)



def salir(request):
    logout(request)
    return redirect('inicio')


def registrarse(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request , f'Usuario {username} creado')
            form.save()
         
            return redirect('inicio')
        else:
            messages.success(request , f'ERROR' )
    else:
        form = CustomUserCreationForm()

    
    context ={'form': form}

    return render(request, 'registration/registro.html', context)

@login_required
def producto_seleccionado(request , producto_id ):
    productos = Productos.objects.filter(ProductoID = producto_id)
    inventario = Inventario.objects.filter(ProductoID = producto_id)
    return render(request , 'detalle_producto.html' , {'productos': productos,
                                                       'inventario': inventario})



def productos_por_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(SubCategoriaProductos, SubcategoriaID=subcategoria_id)
    productos = Productos.objects.filter(SubcategoriaID=subcategoria)
    categorias = CategoriasProductos.objects.all()
    listasubcategorias = SubCategoriaProductos.objects.all()

    return render(request, 'productos_por_categoria.html', {'productos': productos, 'subcategoria': subcategoria, 'categorias': categorias, 'listasubcategorias': listasubcategorias})


from datetime import datetime
@login_required
def agregar_al_carrito(request, producto_id):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Productos, ProductoID=producto_id)
    fecha_entrega = request.POST.get('fecha_entrega', '')
    hora_entrega = request.POST.get('hora_entrega', '')
    try:
        fecha_entrega_obj = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()
        hora_entrega_obj = datetime.strptime(hora_entrega, '%H:%M').time()
    except ValueError:
        messages.error(request, 'Error en el formato de fecha u hora.')
        return redirect('productoSelecionado', producto_id=producto_id)

    if producto not in carrito.productos.all():
        producto_en_carrito = ItemCarrito.objects.create(
            carrito=carrito,
            producto=producto,
            fecha_entrega=fecha_entrega_obj,
            hora_entrega=hora_entrega_obj
        )
        carrito.cantidad_productos += 1
        carrito.save()

        carrito.productos.add(producto_en_carrito.producto)

        request.session['carrito'] = carrito.cantidad_productos

    return redirect('productoSelecionado', producto_id=producto_id)


@login_required
def ver_carrito(request):
    carrito = Carrito.objects.get(usuario=request.user)
    productos_en_carrito = carrito.itemcarrito_set.all()

    return render(request, 'carrito_compras.html', {'productos_en_carrito': productos_en_carrito, 'carrito': carrito})



from .models import ItemCarrito
@login_required

def eliminar_del_carrito(request, producto_id):
    carrito = request.user.carrito_set.get()
    
    # Obtén el objeto ItemCarrito a eliminar
    item_a_eliminar = get_object_or_404(ItemCarrito, carrito=carrito, producto__ProductoID=producto_id)

    # Elimina el objeto ItemCarrito
    item_a_eliminar.delete()

    # Actualiza la relación 'productos' en el modelo Carrito
    carrito.productos.remove(item_a_eliminar.producto)

    # Actualiza la cantidad de productos en el carrito
    carrito.cantidad_productos -= 1
    carrito.save()

    # Actualiza la sesión con la nueva cantidad de productos en el carrito
    request.session['carrito'] = carrito.cantidad_productos

    return redirect('carrito')



@login_required
@csrf_exempt
def direccion_compra(request):
    carrito = Carrito.objects.get(usuario=request.user)
    productos_en_carrito = carrito.itemcarrito_set.all()

    sub_total_carrito = sum(item.producto.Precio * 1 for item in productos_en_carrito)

    # Calcula el IVA
    iva = sub_total_carrito * Decimal(0.12)
    iva_redondeado = iva.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    # Calcula el total
    total = sub_total_carrito + iva_redondeado
    
    ciudades_ecuador = obtener_provincias_ecuador()

    return render(request, 'direccion_compra.html', {'productos_en_carrito': productos_en_carrito, 'carrito': carrito, 'total': total, 'sub_total_carrito': sub_total_carrito, 'iva_redondeado': iva_redondeado, 'ciudades_ecuador': ciudades_ecuador})

import json
def obtener_provincias_ecuador():
    json_file_path = "reservaciones/provincias.json"
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        provincias_ecuador = {provincia_id: {'provincia': data[provincia_id]['provincia'], 'cantones': []} for provincia_id in data if 'provincia' in data[provincia_id]}
        
        # for provincia_id, provincia_info in data.items():
        #     if 'provincia' in provincia_info:
        #         cantones = provincia_info.get('cantones', {})
        #         provincias_ecuador[provincia_id]['cantones'] = [{'canton_id': canton_id, 'canton': canton_info['canton']} for canton_id, canton_info in cantones.items()]
       

        return provincias_ecuador
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo JSON en la ruta especificada: {json_file_path}")
        return {}

if __name__ == "__main__":
    provincias_ecuador = obtener_provincias_ecuador()
    print(provincias_ecuador)
    
    
import json
def pago(request):
    if request.method == 'POST':
        print(request.POST)
        numero_telefono = request.POST.get('phone', '')
        provincia = request.POST.get('provincia', '')
        ciudad = request.POST.get('ciudad', '')
        direccion = request.POST.get('direccion', '')
        c_postal = request.POST.get('c_postal', '')
        formulario1 = request.POST.get('form-1', '')
        formulario2 = request.POST.get('form-2', '')

        # Crear la entrega base
        entrega = Entrega.objects.create(
            usuario=request.user,
            telefono=numero_telefono
        )

        if formulario1 == "1": 
            EntregaDomicilio.objects.create(
                entrega=entrega,
                tipo_entrega='domicilio',
                provincia=provincia,
                ciudad=ciudad,
                direccion_entrega=direccion,
                codigo_postal=c_postal
            )
        elif formulario2 == "2": 
            EntregaTienda.objects.create(
                entrega=entrega,
                tipo_entrega='tienda'
            )

    return render(request, 'pago.html')
        



def confirmacion_pago(request):
    # Obtén el carrito actual del usuario
    carrito = Carrito.objects.get(usuario=request.user)

    # Obtiene todos los elementos del carrito con sus cantidades
    items_carrito = ItemCarrito.objects.filter(carrito=carrito)

    # Calcula el total sumando el precio de cada producto multiplicado por su cantidad
    total_a_pagar = sum(item.producto.Precio * item.cantidad for item in items_carrito)
    
    iva = total_a_pagar * Decimal(0.12)
    iva_redondeado = iva.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total = total_a_pagar + iva_redondeado
    
    detalle_compra = DetalleCompra.objects.create(
        carrito=carrito,
        precioTotal=total,
    )

    

    return render(request, 'confirmacion_pago.html', {'total_a_pagar': total_a_pagar, 'items_carrito': items_carrito})



def agregarProducto(request):
    if request.method == "GET":
        productoid = request.GET['productoid']
        cantidad_nueva = Decimal(request.GET['cantidad']) 
        carrito = Carrito.objects.get(usuario=request.user)
        productos_en_carrito = carrito.itemcarrito_set.all()
      
        for p in productos_en_carrito:
            if p.producto.ProductoID == int(productoid):
                p.cantidad = cantidad_nueva
                p.save()       
         

        sub_total_carrito = 0

        for i in productos_en_carrito:
            precio = Decimal(str(i.producto.Precio))
            sub_total_carrito += precio * Decimal(str(i.cantidad))
            print(sub_total_carrito)
            
            

        iva = sub_total_carrito * Decimal(0.12)
        iva_redondeado = iva.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        total = sub_total_carrito + iva_redondeado
        
      
        
        data={
           'total': total , 'iva_redondeado': iva_redondeado , 'sub_total_carrito': sub_total_carrito
        }
        return JsonResponse(data)
    
    


from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter




def generar_factura_pdf(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items_carrito = ItemCarrito.objects.filter(carrito=carrito)

    total_a_pagar = sum(item.producto.Precio * item.cantidad for item in items_carrito)

    iva = total_a_pagar * Decimal(0.12)
    iva_redondeado = iva.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total = total_a_pagar + iva_redondeado

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear un objeto BytesIO para almacenar el contenido del PDF
    buffer = BytesIO()

    # Crear el objeto PDF usando reportlab
    p = canvas.Canvas(buffer, pagesize=letter)

    # Configurar el estilo del PDF
    p.setFont("Helvetica", 12)

    # Agregar encabezado
    p.drawString(100, 750, "Factura")
    p.drawString(100, 730, "Cafe Dulce")
    p.drawString(100, 710, "RUC: 1203454788001")

    # Agregar datos de contacto
    p.drawString(100, 670, "Teléfono: 0997840372")
    p.drawString(100, 650, "Dirección: Av.25 Abril- Juan Celico Secaira")
    p.drawString(100, 630, "Correo Electrónico: cafedulce@gmail.com")

    # Agregar número de factura
    p.drawString(400, 750, f"Nro. Factura: 123456")
    p.drawString(400, 730, f"Fecha: {fecha_actual}")

# Agregar detalles del cliente
    p.drawString(100, 600, f"Cliente: {request.user.username}")

    # Agregar encabezados de productos
    p.drawString(100, 570, "Cantidad")
    p.drawString(200, 570, "Producto")
    p.drawString(300, 570, "Precio Unitario")
    p.drawString(400, 570, "Total")

    y_position = 550  # ajusta la posición inicial
    for item in items_carrito:
        # Línea horizontal

        # Agregar detalles del producto
        p.drawString(100, y_position , f"{item.cantidad}")
        p.drawString(200, y_position, f"{item.producto.NombreProducto}")
        p.drawString(300, y_position, f"{item.producto.Precio}")
        p.drawString(400, y_position, f"{item.producto.Precio * item.cantidad}")
       

        y_position -= 20
    p.line(100, y_position - 10, 500, y_position - 10)
    # Agregar el total al PDF
# Agregar el subtotal al PDF
    p.drawString(100, y_position - 30, f"SubTotal: {total_a_pagar}")

    # Agregar el IVA al PDF
    p.drawString(100, y_position - 50, f"Iva 12%: {iva_redondeado}")

    # Agregar el total al PDF
    p.drawString(100, y_position - 70, f"Total a pagar: {total}")

    # Guardar el PDF en el objeto BytesIO
    p.showPage()
    p.save()

    # Establecer la posición de lectura del objeto BytesIO al principio
    buffer.seek(0)

    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="factura.pdf"'
    response.write(buffer.read())

    return response