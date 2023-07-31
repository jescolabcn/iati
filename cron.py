import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iati.settings')
django.setup()

from productos.models import Producto


print("TAREA DE ANALISIS DE STOCK....")