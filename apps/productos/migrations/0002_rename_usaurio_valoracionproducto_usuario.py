# Generated by Django 5.1.6 on 2025-03-15 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='valoracionproducto',
            old_name='usaurio',
            new_name='usuario',
        ),
    ]
