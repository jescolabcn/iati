from django.db import models
from datetime import datetime

TIPO_PRODUCTO = [("gorra", "Gorra"), ("camiseta", "Camiseta")]    

class Producto(models.Model):
    tipo = models.CharField(max_length=10, choices=TIPO_PRODUCTO)
    id = models.AutoField(primary_key=True) 
    marca = models.CharField(max_length=100)    
    colorPrincipal = models.CharField(max_length=50)
    coloresSecundarios = models.CharField(max_length=200)
    colorLogo = models.CharField(max_length=50, null=True, blank=True)
    talla = models.CharField(max_length=10, null=True, blank=True)
    composicion = models.CharField(max_length=100, null=True, blank=True)
    tallaje = models.CharField(max_length=10, null=True, blank=True)
    mangas = models.BooleanField(null=True, blank=True)
    fechaInclusion = models.DateField()
    fechaEliminacion = models.DateField(blank=True,default=None,null=True)
    urlFoto = models.URLField()
    precioUnidad = models.DecimalField(max_digits=8, decimal_places=2)
    stockInicial = models.PositiveIntegerField()
    stockActual = models.IntegerField()
    eliminado=models.BooleanField(null=True,blank=True)
    descripcion=models.CharField(max_length=400,blank=True)

    class Meta:
        unique_together = (("tipo", "marca","colorPrincipal","coloresSecundarios","colorLogo","talla","mangas"),)
    
    def save(self, *args, **kwargs):                
        composicion=""
        if self.tipo.lower()=="camiseta":
            composicion=f"##{self.composicion}"
        colores=f"{self.colorPrincipal},{self.coloresSecundarios},{self.colorLogo}"
        self.descripcion=f"{self.tipo}##{self.marca}##{colores}##{self.fechaInclusion.year}##{self.talla}{composicion}"
        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.marca} - {self.colorPrincipal} - {self.fechaInclusion}"


class Carrito(models.Model):
    fecha = models.DateField(auto_now_add=True)
    compra = models.BooleanField(default=False)

class ProductoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        self.producto.stockActual -= self.cantidad
        self.producto.save()


