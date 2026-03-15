# Frontend - Coworking

Estructura básica de frontend con React, Vite y Docker.

## Requisitos

- Docker
- Docker Compose

## Desarrollo con Docker


### Levantar el proyecto

```bash
docker-compose up --build
```

### Iniciar el proyecto

```bash
docker-compose up
```

La aplicación estará disponible en `http://localhost:5173`

### Reconstruir la imagen

```bash
docker-compose up --build
```

### Detener el proyecto

```bash
docker-compose down
```

## Desarrollo local (sin Docker)

### Instalar dependencias

```bash
npm install
```

### Iniciar servidor de desarrollo

```bash
npm run dev
```

### Construir para producción

```bash
npm run build
```

## Estructura del proyecto

```
Front-end/
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación del contenedor
├── package.json            # Dependencias del proyecto
├── vite.config.js          # Configuración de Vite
├── index.html              # HTML base
├── src/
│   ├── main.jsx           # Punto de entrada
│   └── App.jsx            # Componente principal
└── public/                # Archivos estáticos
```

## Tecnologías

- React 18
- Vite 5
- Docker
