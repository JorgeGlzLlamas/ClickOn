# Versiones
Django 5.1.6
Python 3.12.9

# Instalar dependencias
pip install -r requirements/requirements.txt

# Actualizar dependencias
pip freeze > requirements/requirements.txt

# Ejecutar aplicación
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migracioens
python manage.py migrate
