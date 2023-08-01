 ### Ficheros

- inidb.py  se encarga de rellenar la bbdd con datos de pruebas *datos.json* al arrancar el servicio
- cronjob  es la configuración de cron que se instalará en crontab
- generic
- postifx_main.cf    son los ficheros para hacer el intento de envio, que no he conseguido...
- sender_access  
- run.sh      el bash de inicio de ejecución en el final de despliegue


## Arranque

```bash
   docker-compose build
   docker-compose start
   o
   docker-compose up    si queremos ver el stdout, dará un aviso 
      ERROR: The image for the service you're trying to recreate has been removed. If you continue, volume data could be lost. Consider backing up your data before continuing.
      Continue with the new image? [yN]y


```

## Documentación

He usado **drf_yasg** para generar automáticamente la documentación con swagger

```url
   http://localhost:8002
   http://localhost:8002/swagger
```




Al final de la compra muestro por terminal el body del correo, intento enviar con un postfix instalado como servicio junto al django

```bash

web_1   | Resumen de compra en Gorras&Kmisetas:
web_1   | 
web_1   | 3 x Camiseta##Vans##Azul,Blanco,Blanco##2023##L##100% Poliester  35.00 €
web_1   | 
web_1   | Total: 105.00 €
web_1   | 
web_1   | Gracias por su compra, Jordi Escolà.
web_1   | {'info@melonmail.eu': (250, b'2.1.5 Ok'), 'data': (250, b'2.0.0 Ok: queued as B38C28824E')}

```
Para el tema del envio del correo he usado una modificación del smtplib para poder obtener el queue_id de entrega al server, no es reinventar la rueda ya que por defecto las librerias de envio de correo no retornan los datos de cola de entrega...

Aunque aparece como entregado **2.0.0 Ok: queued as B38C28824E** realmente el server destino me lo ha rechazado, supongo que es por temas de ip's o por algun fallo de configuración de smtp
## Cron
Al final opté por lo más sencillo que es montar tarea en el crontab con una llamada a un script de django, también podría ser una llamada http con  un curl... Iba a montar el django_cron pern tampoco quería liar mucho el código para una función fantasma.

## BBDD
Aquí no me complicó mucho, ya que opté por usar el SQLite que viene por defecto con Django. Aunque podría haber instalado MariaDB o MySQL, consideré que eso no era demasiado relevante para el propósito de esta prueba. Creí más interesante instalar el servicio smtp.

## Smtp
Quizá perdí demasiado tiempo intentando que funcionara el postfix como servicio.. bueno, por lo menos envia algo..que lo acepten los servers destino es otra cuestión ya de IP's y del dominio inventatis.
mail.log
```bash
Jul 31 19:21:26 ae2596e5124c postfix/qmgr[115]: 8D76488E28: from=<ventas@gorraskmisetas.com>, size=909, nrcpt=1 (queue active)
Jul 31 19:21:27 ae2596e5124c postfix/smtp[128]: connect to pop.melonmail.eu[37.222.109.31]:25: Connection refused
Jul 31 19:21:27 ae2596e5124c postfix/smtp[128]: connect to mail.melonmail.eu[37.222.109.31]:25: Connection refused
Jul 31 19:21:27 ae2596e5124c postfix/smtp[128]: 8D76488E28: to=<info@melonmail.eu>, relay=none, delay=0.48, delays=0.01/0.01/0.47/0, dsn=4.4.1, status=deferred (connect to mail.melonmail.eu[37.222.109.31]:25: Connection refused)
```


## Testing
Como testing lo he verificado directamente con swagger y con un par de scripts sencillos de python para hacer compras directas 

Carro
```python
import requests

data = {"producto": 10,"cantidad": 3}
url = "http://localhost:8002/productos/carrito"
response = requests.post(url, json=data)

if response.status_code == 201:
    print("Producto agregado al carrito exitosamente.")
    print("Detalles del producto agregado:")
    print(response.json())
elif response.status_code == 404:
    print("Producto no encontrado.")
elif response.status_code == 400:
    print("No hay suficiente stock disponible.")
else:
    print("Error al agregar el producto al carrito. Código de respuesta:", response.status_code)
```

Compra
```python
import requests

url_procesar_compra = "http://localhost:8002/productos/compra"
datos_cliente = {
    "nombre": "Jordi",
    "apellidos": "Escolà",
    "direccion": "Calle Mayor,1",
    "email": "info@melonmail.eu",
    "telefono": "6666666666",
}
response = requests.post(url_procesar_compra, json=datos_cliente)

if response.status_code == 200:
    print("Compra procesada correctamente.")
    print("Respuesta del servidor:")
    print(response.json())
else:
    print("Error al procesar la compra. Código de respuesta:", response.status_code)
