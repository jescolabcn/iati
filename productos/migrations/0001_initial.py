# Generated by Django 4.2.3 on 2023-07-30 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('gorra', 'Gorra'), ('camiseta', 'Camiseta')], max_length=10)),
                ('marca', models.CharField(max_length=100)),
                ('colorPrincipal', models.CharField(max_length=50)),
                ('coloresSecundarios', models.CharField(max_length=200)),
                ('colorLogo', models.CharField(blank=True, max_length=50, null=True)),
                ('talla', models.CharField(blank=True, max_length=10, null=True)),
                ('composicion', models.JSONField(blank=True, null=True)),
                ('tallaje', models.CharField(blank=True, max_length=10, null=True)),
                ('mangas', models.BooleanField(blank=True, null=True)),
                ('fechaInclusion', models.DateField()),
                ('urlFoto', models.URLField()),
                ('precioUnidad', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stockInicial', models.PositiveIntegerField(editable=False)),
                ('stockActual', models.PositiveIntegerField()),
                ('elimiado', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]