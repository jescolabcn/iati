# Generated by Django 4.2.3 on 2023-07-31 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0008_carrito_productocarrito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stockActual',
            field=models.IntegerField(),
        ),
    ]
