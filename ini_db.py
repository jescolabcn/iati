import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iati.settings')
django.setup()

from productos.models import Producto
from datetime import datetime

with open("datos.json","r") as f:
    datos_ejemplo=json.loads(f.read())

# Función para insertar los datos en la base de datos
def insertar_datos():
    contador=0
    try:
        for dato in datos_ejemplo:
            if not Producto.objects.filter(tipo=dato["tipo"],
                                           colorPrincipal=dato["colorPrincipal"],
                                           coloresSecundarios=dato["coloresSecundarios"],
                                           colorLogo=dato["colorLogo"],
                                           talla=dato["talla"],
                                           mangas=dato["mangas"],
                                           tallaje=dato["tallaje"],
                                           marca=dato["marca"]).exists():
                dato["fechaInclusion"]=datetime.strptime(dato["fechaInclusion"],"%Y-%m-%d")                
                Producto.objects.create(**dato)
                contador+=1

        print(f" {contador} Datos insertados correctamente en la base de datos.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    insertar_datos()