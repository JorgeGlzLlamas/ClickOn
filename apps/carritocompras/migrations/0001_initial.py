# Generated by Django 5.1.6 on 2025-03-14 23:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrito', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'carrito',
                'db_table': 'carrito_compras',
            },
        ),
        migrations.CreateModel(
            name='ProductoCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_carritos', to='carritocompras.carrito', verbose_name='Carrito')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos_carritos', to='productos.producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'producto_carrito',
                'verbose_name_plural': 'productos_carrito',
                'db_table': 'producto_carrito',
            },
        ),
        migrations.CreateModel(
            name='ProductoFavoritos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_favorito', to='productos.producto', verbose_name='Producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_favorito', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'producto_favorito',
                'verbose_name_plural': 'productos_favoritos',
                'db_table': 'producto_favorito',
            },
        ),
        migrations.CreateModel(
            name='ProductoWishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_wishlist', to='productos.producto', verbose_name='Producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_wishlist', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'producto_wishlist',
                'verbose_name_plural': 'productos_wishlist',
                'db_table': 'producto_wishlist',
            },
        ),
    ]
