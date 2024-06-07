Muy buenas a todo el mundo, mi nombre es D4l1 y hoy explicare como conseguir entender y destrozar la máquina NodeBlog

Nos encontramos con una máquina de dificultad fácil, que no por ello lo tiene que ser.

Nos encontramos con una máquina linux, ¿como lo sabemos?
Aquí tenemos dos formas:

Yo suelo utilizar mi escaner de puertos to guapo que tengo en github o simplemente con un ping. Y sabiendo los numeros tty podemos saber a que máquina nos enfrentamos 

```
ping ip
```
Posteriormente a esto y sabiendo que es una máquina Linux, lo siguiente que deberemos hacer es escanear la red en busca de puertos abiertos, versiones, scripts, etc. 

Esto lo haremos con nmap y un comando que suelo utilizar.

```
sudo nmap -sCV -T4 --min-rate 5000 -p- -Pn ip
```
En esta máquina nos encontramos dos puertos abiertos:
El puerto 22 con SSH
El puerto 5000 con Node.js 

En el que si entramos vemos un blog básico.

Podemos hacer un curl o entrar desde un navegador 

```
curl -v ip:5000
```
Vemos que utiliza el framework Express

Nos encontramos con el blog y obviamente inspeccionamos que nos encontramos, los directorios el código fuente etc.
Posteriormente encontramos un inicio de sesión, lo más obvio es probar un ataque de SQL INJECTION
Después de probar diferentes cosas  probamos el NoSQL

###NOSQL
Es un tipo de base de datos no relacional diseñada para modelos de datos, incluyendo llaves, columnas y graficos. La diferencia entre SQL y noSQL es la forma de guardar información y la estructuración de los datos.

Gracias a esta información encontramos un repositorio de bastantes payloads sobre noSQL

#https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection#authentication-bypass
