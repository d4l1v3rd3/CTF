#by d4l1

<p align="center"><img src=""></p>
<h1 align="center">Armageddon</h1>

# ÍNDICE

# INICIO

Arageddib es una máquina Linux fácil. Encontramos un drupal vulnerable en una página web en el que podremos acceder remotamente al host.
Dentro de la enumeración de Drupal y su entrcutra de fichero encontramos las credenciales para conectarnos al servidor de MySQL y extraer el hash del usuario del sistema.
Con esas credenciales nos conectamos por SSH. Tenemos la disponibilidad de instalar aplicacion. Escalamos privilegios subiendo e instalando una aplicacion maliciosa

Para empezar el ping para comprobar

![image](https://github.com/D4l1-web/HTB/assets/79869523/da7167a0-810e-4f1c-9242-fe537d22af87)

Posteriormente el escaner de directorios

![image](https://github.com/D4l1-web/HTB/assets/79869523/bdb1ae67-cf5d-4ed7-9d73-bb5e6568fe35)

En el que encontramos dos puertos abiertos un puerto 22 SSH y un 80 con un apache 2.4.6 un drupta 7 e información relevante.

En mi caso utilizare searchspoit para buscar algún exploit sobre "drupal 7"

![image](https://github.com/D4l1-web/HTB/assets/79869523/773c384e-e52f-41c6-aad6-2bf15a5ffb11)

```
git clone https://github.com/dreadlocked/Drupalgeddon2.git
```
Alfinal me he metido con metasploit buscando el exploit directamente con un 
```
search drupal 7
```
He cogido el exploit drupaggedon2 he configurado los RHOST y los LHOST y estamos dentro con el usuario "apache"
![image](https://github.com/D4l1-web/HTB/assets/79869523/f8c9306e-fb27-4e87-a317-5ee974ba48f7)

Posteriormente me he ido a la ruta de la configuracion de la base de datos y hemos enumerado los archivos y encontrado la contraseña.

![image](https://github.com/D4l1-web/HTB/assets/79869523/f910248f-a65d-4dd8-abdd-9521194ba9e6)

```
cat /var/www/html/sites/default/settings.php
mysql -u drupaluser -pCQHEy@9M*m23gBVj -e 'show databases;'
```


