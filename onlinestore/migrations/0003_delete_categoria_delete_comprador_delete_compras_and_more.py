# Generated by Django 4.2.4 on 2023-09-04 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0002_compras_orden_productoorden_review_tarjeta_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Categoria',
        ),
        migrations.DeleteModel(
            name='Comprador',
        ),
        migrations.DeleteModel(
            name='Compras',
        ),
        migrations.DeleteModel(
            name='Detallecarrito',
        ),
        migrations.DeleteModel(
            name='Empresa',
        ),
        migrations.DeleteModel(
            name='Listadeseo',
        ),
        migrations.DeleteModel(
            name='Orden',
        ),
        migrations.DeleteModel(
            name='Paypal',
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
        migrations.DeleteModel(
            name='ProductoOrden',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Tarjeta',
        ),
        migrations.DeleteModel(
            name='Transferencia',
        ),
    ]
