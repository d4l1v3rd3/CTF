#by d4l1

<h1 align="center">Perfection</h1>

<p align="center"><img  src="https://github.com/D4l1-web/HTB/assets/79869523/fc054059-74b6-4363-bb86-72efafd10b9f"></p>

# INTRODUCCIÓN

Perfection es una maquina Linux fácil, en la que contiene una aplicacion web con la funcion de poder calcular notas de estudiantes. La aplicacion web es vulnerable a (SSTI) via regex.

## ENUMERACIÓN

Bienvenidos a esta máquina. Como siempre haremos los dos comandos básicos, comprobar que tenemos conexión y el escaner de puertos.

![image](https://github.com/D4l1-web/HTB/assets/79869523/7e0bd8ef-0907-49d5-b55a-1a110fec0663)

Posteriormente haremos el escaner a ver que encontramos.

![image](https://github.com/D4l1-web/HTB/assets/79869523/1d590945-d1bf-4065-917b-68ae3af286a1)

Como podemos comprobar nos encontramos con dos puertos abiertos el 22 (ssh) y el 80 (http) en un servidor ngnix .

Tenemos más información porque nos dan la versión de ssh.
![image](https://github.com/D4l1-web/HTB/assets/79869523/9059dbab-66b5-4f44-b7dd-5da9f3d85fa0)

### HTTP

Si nos conectamos al servidor web, veremos un "weighted grade calculator" una herramienta pa los alumnos vamos. 

![image](https://github.com/D4l1-web/HTB/assets/79869523/a90ff5e5-7bd4-45a7-85f7-b16a2221ee8f)

Encontramos dos cosas importantes el lenguaje de programación "Ruby" y el framework que utiliza "WEBrick 1.7.0"

![image](https://github.com/D4l1-web/HTB/assets/79869523/774a6134-463a-4047-9e35-48d4bdd6cc9e)

Si nos vamos a la tercera pestaña nos encontramos con una calculadora, vamos a intentar poner datos reales para que no nos de error.

![image](https://github.com/D4l1-web/HTB/assets/79869523/00a3c90b-584f-4750-8e5a-e337a279db22)

Como entenderemos, al tener un boton Sumbit damos por hecho que tiene que ir a algun lado. Con lo cual utilizaremos BurpSuite para pillar la request y ver donde va.
