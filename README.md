# Lucro
Actividad promocional en la cual se busca incentivar la compra de ciertos productos por parte de los usuarios

## Acerca del proyecto
Este sistema se encanga de validaciones de imagenes de producto en dinde se hace la consulta a un sistema externo simulado.
El sistema de calificacion es el siguiente:
* Si el score está entre 0.8 y 1, se le asignan los puntos inmediatamente.
* Si el score está entre 0.5 y 0.8, se asignan los puntos pero las imágenes se validan después y se le pueden descontar los puntos.
* Si el score es menor a 0.5, no se le asignan los puntos.

## Caratecristica
* El usuario puede subir hasta 5 imagenes validas por día, y ganar puntos.
* El usuario puede consultar cuantas imagenes a subido en el día.
* El usuario puede consultar su puntaje total.
* El usuario puede cambiar puntos por bonos, por cada mil puntos un bono.
* El usuario puede registrarse e iniciar y cerrar sesion.
* El administrador puede ver cuantos usuarios estan registardo en la promocion.
* El administrador puede ver los codigos redimidos y generados.
* El administrador puede ver el producto mas registardo en la promocion.
* El administrador puede ver imagenes no validadas.por la imagen.
* El administrador puede validar las imagenes manualmente, reafirmando los puntos o quintarlo.
* Para utilizar las carateristicas de administrador se debe utilizar una variable de entorno llamada API_KEY esta va en el header 

### Construido con
* Lenguaje: Python3.8
* Framework: Fastapi
* Base de dato: MongoDB


<!-- GETTING STARTED -->
## Iniciando

Este es un ejemplo de como deberian instalar el proyecto localmente dada las instruciones.

### Prerequisites
* [MongoDB Installation](https://docs.mongodb.com/manual/installation/)

Una vez que tengas mongoDB instalado, deberia obtener la Uri de conexion a tu base de datos, establecerla como variable de entorno MONGO_URI.

sh
sudo systemctl status mongod


### Intalacion 

1. Instalar virtualEnv e instalarlo
```sh
$ virtualenv -p python3 venv
```
```sh
$ source venv/bin/activate
```
2. Instalar requirements.txt
```sh
$ pip3 install -r requirements.txt
```
### Correr servidor

```sh
$ uvicorn config:app --host=localhost --port=8001 --reload
```

### Documentacion de la API

La documentacion esta hecha cumpliendo los estadares de OpenAPI con ayuda del framework FastAPI y la libreria BaseModel.

La ruta de la documentacion se encuentra disponible en http://localhost:8001/docs
