
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tools import mysmtp
from .models import Producto
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from datetime import date
from .serializers import ProductoSerializer,ProductoCreateSerializer,ProductoCarritoSerializer,ProductoCarritoSerializerPost

from .models import Carrito, ProductoCarrito
from .serializers import ProductoCarritoSerializer


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



    

class ProductoList(generics.ListAPIView):
    queryset = Producto.objects.filter(eliminado=False).order_by('tipo', '-fechaInclusion')
    serializer_class = ProductoSerializer
    @swagger_auto_schema(
        operation_description="Obtener lista de productos",
        responses={200: ProductoSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.filter(eliminado=False).order_by('tipo', '-fechaInclusion')
    @swagger_auto_schema(
        operation_description="Obtener lista de productos",
        responses={200: ProductoSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Insertar un nuevo producto",
        responses={200: ProductoSerializer()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == 'POST':        
            return ProductoCreateSerializer
        return ProductoSerializer
    
    
class ProductoRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.filter(eliminado=False)
    serializer_class = ProductoSerializer
    def perform_destroy(self, producto):        
        producto.eliminado = True
        producto.fechaEliminacion=date.today()
        producto.save()


        

@swagger_auto_schema(method='GET', responses={200: ProductoCarritoSerializer(many=True)}, 
                     operation_description=""" Muestra la lista de los productos que hayan sido añadidos y
                                                el sumatorio del total de los productos añadidos""")                    
@swagger_auto_schema(method='POST', request_body=ProductoCarritoSerializerPost, responses={200: ProductoCarritoSerializerPost()},
                     operation_description="""Agrega elementos al carrito junto con la cantidad de dicho producto que se quiere añadir (por defecto la cantidad es una unidad                     
                        Cantidades negativas restarán elementos del carrito. El stock deberá ser actualizado en
                        cuanto el producto entre al carrito""")

@api_view(['POST','GET'])
def carrito(request):
    pendiente = Carrito.objects.filter(fecha=date.today(), compra=False).first()
    if request.method=='GET':            
        if not pendiente:
            return Response({"productos": [], "total": 0}, status=status.HTTP_200_OK)
           
        productos_carrito = ProductoCarrito.objects.filter(carrito=pendiente)
        total_carrito = sum(item.producto.precioUnidad * item.cantidad for item in productos_carrito)   
        
        productos = []
        for item in productos_carrito:
            producto = {
                "id": item.producto.id,
                "descripcion": item.producto.descripcion,
                "urlFoto": item.producto.urlFoto,
                "cantidad": item.cantidad,
                "precioUnidad": item.producto.precioUnidad
            }
            productos.append(producto)

        return Response({"productos": productos, "total": total_carrito}, status=status.HTTP_200_OK)



    if request.method=='POST':            
        if not pendiente:
            pendiente = Carrito.objects.create()

        # Obtener datos del producto y cantidad desde el cuerpo de la solicitud
        data = request.data
        id = data.get('producto')
        cantidad = data.get('cantidad', 1)
        print(f"ID {id}")
        producto = get_object_or_404(Producto, pk=id, eliminado=False)



        if cantidad > producto.stockActual:
            return Response({"Error": "Sin Stock"},
                            status=status.HTTP_400_BAD_REQUEST)


        producto_carrito, created = ProductoCarrito.objects.get_or_create(
            carrito=pendiente,
            producto=producto,
            defaults={'cantidad': cantidad}
        )

        if not created:
            producto_carrito.cantidad += cantidad
            producto_carrito.save()


        producto.stockActual -= cantidad
        producto.save()

        serializer = ProductoCarritoSerializer(producto_carrito)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='POST', request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,                   
                         properties={
                             'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre'),
                             'apellidos': openapi.Schema(type=openapi.TYPE_STRING, description='Apellidos'),
                             'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Direccion'),
                             'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                             'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='telefono'),
                         },
                         required=['nombre', 'apellidos','direccion','email']
                     ),
                     responses={
                         200: openapi.Response(
                             description="Compra finalizada",                        
                         ),
                         400: "Carro vacio",                         
                     },
                     operation_description="""
                     Recibe un formulario con los datos personales del cliente:
                     nombre, apellidos, dirección postal, email y teléfono. Simulamos la compra enviando al
                     cliente un email con el resumen de su compra.""")
@api_view(['POST'])
def compra(request):
    
    pendiente = Carrito.objects.filter(fecha=date.today(), compra=False).first()

    if not pendiente:
        return Response({"Error": "No hay productos en el carrito"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    direccion = data.get('direccion')
    email = data.get('email')
    telefono = data.get('telefono')

    
    pendiente.compra = True
    pendiente.save()

    
    productos_carrito = ProductoCarrito.objects.filter(carrito=pendiente)   
    total_compra = sum(item.producto.precioUnidad * item.cantidad for item in productos_carrito)

    # Crear el contenido del correo electrónico
    body = f"Resumen de compra en Gorras&Kmisetas:\n\n"
    for item in productos_carrito:
        body += f"{item.cantidad} x {item.producto.descripcion}  {item.producto.precioUnidad} €\n"

    body += f"\nTotal: {total_compra} €\n"    
    body += f"\nGracias por su compra, {nombre} {apellidos}."
    remitente="ventas@gorraskmisetas.com"
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = email
    mensaje['Subject'] = 'Resumen compra Gorras&kmisetas'
    mensaje.attach(MIMEText(body, 'plain'))
    print(body)
    try:
        servidor = mysmtp("localhost:25")
        res=servidor.sendmail(remitente, email, mensaje.as_string())
        print(res)
        servidor.quit()       
    except Exception as e:        
        print("Error enviando email",str(e))
    return Response({"mensaje": f"Compra procesada correctamente. Se ha enviado un correo electrónico  {email} con el resumen de su compra."}, status=status.HTTP_200_OK)

