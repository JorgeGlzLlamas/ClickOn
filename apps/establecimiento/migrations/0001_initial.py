# Generated by Django 5.1.6 on 2025-03-14 23:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del establecimiento')),
                ('logo', models.ImageField(upload_to='img/establecimiento_logo/', verbose_name='Logo del establecimiento')),
                ('entidad', models.CharField(max_length=60, verbose_name='Entidad del establecimiento')),
                ('municipio', models.CharField(max_length=60, verbose_name='Muncipio del establecimiento')),
                ('codigo_postal', models.CharField(max_length=6, verbose_name='Código postal del establecimiento')),
                ('colonia', models.CharField(max_length=50, verbose_name='Colonia del establecimiento')),
                ('calle', models.CharField(max_length=50, verbose_name='Calle del establecimiento')),
                ('numero_exterior', models.CharField(max_length=5, verbose_name='Num. Exterior del establecimiento')),
                ('numero_interior', models.CharField(blank=True, max_length=5, null=True, verbose_name='Num. Interior del establecimiento')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='establecimiento', to=settings.AUTH_USER_MODEL, verbose_name='ID usuario - dueño ')),
            ],
            options={
                'verbose_name': 'establecimiento',
                'db_table': 'establecimiento',
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('1', 'Lunes'), ('2', 'Martes'), ('3', 'Miercoles'), ('4', 'Jueves'), ('5', 'Viernes'), ('6', 'Sábado'), ('7', 'Domingo')], max_length=1)),
                ('hora_apertura', models.TimeField()),
                ('hora_cierre', models.TimeField()),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horario', to='establecimiento.establecimiento', verbose_name='Establecimiento')),
            ],
            options={
                'verbose_name': 'horario',
                'verbose_name_plural': 'horarios',
                'db_table': 'horario',
                'ordering': ['dia'],
            },
        ),
    ]
