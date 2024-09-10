<h1 align="center">CMesS</h1>

![image](https://github.com/user-attachments/assets/822eb782-91ae-408d-8867-3a8c4f0cfd88)

# ENUMERACIÓN

Test Conectividad:

![image](https://github.com/user-attachments/assets/103b245d-76c9-4db6-9315-c79e049c533e)

Escaneo Puertos:

![image](https://github.com/user-attachments/assets/65a716bc-fb78-44d4-a40d-658b75e4959b)

Nos encontramos con el puerto 22 abierto (ssh) y por otro lado un apache en el puerto 80, el mismo escaneo nos encuentra el "robots.txt" con 3 redirecciones /src/ /themes/ /lib/

Antes de nada meteremos el dominio "cmess.thm" a nuestro dns /etc/hosts

```
echo "10.10.39.36 cmess.thm" | sudo tee -a /etc/hosts
```

![image](https://github.com/user-attachments/assets/f9f997cd-377b-4e63-ac09-baa0125a2d49)

Dentro de la web nos necontramos dentro de un CMS "Gila CMS" dentro de la web no encontramos nada importante, vamos a probar las urls que antes hemos cogido del robots.txt a ver si sacamos algo importante.

He probado a conectarme a las 3 y no tengo permisos en ninguna, busquemos otro vector

Lo posterior que he hecho ha sido un escaner de directorios con ffuf 

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-20000.txt:FUZZ -u http://cmess.thm/FUZZ
```

En la que nos encontramos urls importantes como: /login/ /admin/ pero no sacamos cosas importantes ahora si que si vamos a probar con subdominios

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-20000.txt:FUZZ -u http://cmess.thm/ -H "Host: FUZZ.cmess.thm" -fw 522
```

![image](https://github.com/user-attachments/assets/e9d70f00-0e98-4cfe-86ed-b18800ead3b3)

Gracias a esto sacamos otra ruta más "dev.cmess.thm" ruta que vamos a meter dentro del DNS.

![image](https://github.com/user-attachments/assets/25ba1402-eb7c-45a9-a0c5-045b5ee71ddd)

Dentro de dicha URL encontramos varias credenciales, como una mala configuración en el archivo ".htaccess" y 

andre@cmess.thm:KPFTN_f2yxe% 

Vamos a probar a irnos al panel de admin.

![image](https://github.com/user-attachments/assets/74130c3d-ebf0-4eb0-ab82-2a03d3c15b45)

Ya dentro vamos a ver que tenemos y que información podemos sacar.

Primero de todo identificamos la versión de Gila 1.10.9

Por otro lado si vamos por "Content - File Manager" nos encontramos los archivos del CMS donde nos explican un poco el funcionamiento y encontramos el archivo ".htaccess" cosa que como vemos no es muy relevante, busquemos más ficheros a ver si encontramos algo de valor.

![image](https://github.com/user-attachments/assets/82e0c2ff-d906-4d13-9f03-2ee1bb83e204)

En el clavo, en el archivo "config.php" nos encontramos un usuario y contraseña de una base de datos, y una cosa que no me había fijado esque disponemos con que podemos nosotros añadir código al fichero, pudiendo leer o crear una rev shell.

Por supuesto cogeremos la shell de pentest "https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php"



