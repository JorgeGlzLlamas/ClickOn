# Generated by Django 5.1.6 on 2025-03-15 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metodospago',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='metodospago',
            name='precio_total',
        ),
    ]
