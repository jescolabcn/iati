# Generated by Django 4.2.3 on 2023-07-30 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='elimiado',
            new_name='eliminado',
        ),
    ]
