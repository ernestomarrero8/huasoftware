# Huasoftware

## Descripción

Huasoftware es una aplicación web desarrollada en Flask para gestionar un sistema de puntuación y registro de jinetes y caballos en competencias de rodeo. La aplicación permite registrar jinetes y caballos, ingresar y consultar puntuaciones, y visualizar un tablero de posiciones.

## Estructura del Proyecto
huasoftware/
├── __pycache__/
├── env/
├── huasoftware/
│   ├── __pycache__/
│   ├── static/
│   │   ├── assets/
│   │       ├── bootstrap/
│   │       ├── css/
│   │       ├── img/
│   ├── templates/
│   │   ├── base.html
│   │   ├── fechas.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── nuevo_usuario.html
│   │   ├── puntaje.html
│   │   ├── registro.html
│   │   ├── tablaposicion.html
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
├── requirements.txt
├── rodeoLogin.png
├── rodeoLogin1.png
├── rodeoLogo.png
├── Dockerfile
├── docker-compose.yml
├── run.py
Instalación
Requisitos
Docker
Docker Compose


## Clona el repositorio:

git clone <URL_DEL_REPOSITORIO>
cd huasoftware 

## Construye y levanta los contenedores de Docker:
docker-compose up --build

## Accede a la aplicación en tu navegador:
http://localhost:5000


## Uso
Registro de Usuario
Ve a la página de registro.
Ingresa los datos del jinete y el caballo.
Guarda los datos.
Ingreso de Puntuaciones
Ve a la página de puntuaciones.
Ingresa el ID del jinete y las puntuaciones.
Guarda las puntuaciones.
Visualización de Tablero de Posiciones
Ve a la página del tablero de posiciones.
Visualiza las posiciones y las puntuaciones totales de los jinetes.
