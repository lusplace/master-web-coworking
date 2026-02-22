# Coworking-project-UE
## Requisitos

- Docker
- Docker Compose

## Levantar el proyecto

```bash
docker-compose up --build
```

Esto iniciará dos contenedores:
- **db**: MySQL 8.0
- **web**: Django (puerto 8000)

## Endpoints disponibles

- `http://localhost:8000/health/` - Health check (verifica conexión a la base de datos)
- `http://localhost:8000/admin/` - Panel de administración de Django

## Variables de entorno

Las siguientes variables se configuran en `.env` y `docker-compose.yml`:

| Variable | Valor por defecto |
|----------|-------------------|
| MYSQL_DATABASE | coworking_db |
| MYSQL_USER | coworking_user |
| MYSQL_PASSWORD | coworking_pass |
| MYSQL_HOST | db |
| MYSQL_PORT | 3306 |
| SECRET_KEY | Un1v3rs1d4dEur0p34 |
| DEBUG | 1 |

## Super usuario

También se crea automáticamente un superusuario con las siguientes credenciales:
- **Usuario**: admin
- **Contraseña**: admin123
- **Email**: admin@universidadeuropea.com

ejecutar migraciones manualmente:

```bash
docker-compose exec web python manage.py migrate
```

## Crear superusuario adicional

```bash
docker-compose exec web python manage.py createsuperuser
```