
from rest_framework import serializers
from .models import Producto,ProductoCarrito


class ProductoCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoCarrito
        fields = '__all__'
        
class ProductoCarritoSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = ProductoCarrito
        exclude =["carrito"]


class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields= '__all__'
        

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        exclude = ['stockInicial'] 