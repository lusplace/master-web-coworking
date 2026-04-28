#!/usr/bin/env python
"""
Script de entrypoint para el contenedor Docker.
Ejecuta migraciones y crea superusuario antes de iniciar el servidor.
"""
import os
import sys
import time

# Configurar Django ANTES de importar cualquier cosa de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from dotenv import load_dotenv

load_dotenv() # will search for .env file in local folder and load variables

DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
DJANGO_SUPERUSER_FIRST_NAME = os.getenv('DJANGO_SUPERUSER_FIRST_NAME')

from django.core.management import execute_from_command_line

def wait_for_db():
    """Espera a que la base de datos esté lista."""
    print("Esperando a que la base de datos esté lista...")
    time.sleep(5)
    print("✓ Continuando...")

def run_migrations():
    """Ejecuta las migraciones de Django."""
    print("\nEjecutando migraciones...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Migraciones completadas")
    except Exception as e:
        print(f"✗ Error en migraciones: {e}")
        sys.exit(1)

def create_superuser():
    """Crea un superusuario si no existe."""
    print("\nCreando superusuario si no existe...")
    
    import django
    django.setup()
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        admin_email = DJANGO_SUPERUSER_EMAIL
        if not User.objects.filter(correo=admin_email).exists():
            User.objects.create_superuser(
                correo=DJANGO_SUPERUSER_EMAIL,
                password=DJANGO_SUPERUSER_PASSWORD
                username=DJANGO_SUPERUSER_USERNAME
                nombre=DJANGO_SUPERUSER_FIRST_NAME
            )
            print(f'✓ Superusuario creado: {DJANGO_SUPERUSER_USERNAME} ')
        else:
            print('✓ El superusuario ya existe')
    except Exception as e:
        print(f"⚠ Advertencia al crear superusuario: {e}")

def start_server():
    """Inicia el servidor de desarrollo."""
    print("\n" + "="*60)
    print("Iniciando servidor Django...")
    print("="*60 + "\n")
    
    try:
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except Exception as e:
        print(f"✗ Error al iniciar servidor: {e}")
        sys.exit(1)

def main():
    """Función principal del entrypoint."""
    # Solo ejecutar migraciones y crear superusuario en el proceso principal
    if os.environ.get('RUN_MAIN') != 'true':
        print("="*60)
        print("COWORKING PROJECT - Inicialización")
        print("="*60)
        
        wait_for_db()
        run_migrations()
        create_superuser()
    
    start_server()

if __name__ == '__main__':
    main()
