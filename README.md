# master-web-coworking

Ejercicio del Master Web del Grupo 6, con: Luis Rodríguez Arriero (lulu), Ivan Rene Arevalo Venegas, Luis Enrique Quinto Munive

## Requisitos

- Docker
- Docker Compose

## Ejecución con Docker

Para iniciar todos los servicios (base de datos, backend y frontend):

Ubicarse en la carpeta raiz del proyecto:

```bash
docker-compose up
```

Para ejecutar en segundo plano:

```bash
docker-compose up -d
```

Para ver los logs:

```bash
docker-compose logs -f
```

Para detener los servicios:

```bash
docker-compose down
```

Para detener y eliminar los volúmenes (elimina datos de la base de datos):

```bash
docker-compose down -v
```

## Servicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| MySQL | 3306 | Base de datos |
| Backend | 8000 | API Django |
| Frontend | 5173 | Aplicación React (Vite) |

## Guía de la API (Endpoints)

| Recurso  | Endpoint Base | Métodos | Descripción|
|----------|---------------|---------|------------|
|Sedes:    |/api/coworking/sedes/ | GET, POST | Centros de coworking.|
|Espacios: | /api/coworking/espacios/ | GET, POST | Salas y escritorios.|
|Reservas: | /api/coworking/reservas/ | GET, POST | Gestión de bookings.|
|Pagos:    | /api/coworking/pagos/ | GET, POST | Transacciones.|

## Estructura del proyecto

```
master-web-coworking/
├── Back-end/           # API Django
│   ├── Dockerfile
│   └── ...
├── Front-end/          # Aplicación React
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml  # Docker Compose unificado
├── .env        #variables de entorno
└── README.md
```

Tambien se pueden ejecutar los contenedores para el backend y el frontend de forma independiente, para esto es necesario ubicarse en la carpeta del backend o frontend y ejecutar:

```bash
docker-compose up
```