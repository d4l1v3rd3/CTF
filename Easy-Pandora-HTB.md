# INICIO BY d4l1

Muy buenas, hoy estaremos tratando la máquina Pandora de HTB.

Como siempre haremos un poco de resumen a lo que nos enfrentaremos, conocimientos y demás.

Empezaremos haciendo un escaner de sistema operativo, (tengo un repositorio con dicho escaneo).

Gracias a ello entendemos que nos estamos enfrentando a una máquina Linux, posteriormente toca un escaner de puertos, para ver si llegaramos a poder sacar alguna información.

```
sudo nmap -sCV -T4 --min-rate 5000 IP
```
Si queremos podemos poner un "-p-" o "-Pn" pero en este caso no se si hara falta.

Nos encontramos con los puertos "22" (SSH) y "80" (HTTP) abiertos.

Lo que haremos primero sera inspeccionar la página a ver que encontramos.

## PROCESO

Lo primero que encontramos nada más entrar es un dominio "panda.htb" lo añadimos
```
echo "ip panda.htb" | sudo tee -a /etc/hosts
```
En este momento, podemos hacer un escaner de directorios o dominios, pero no vamos a encontrar nada importante.

Probaremos a hacer un nuevo escaner de nmap pero en este caso enfocandonos en udp
```
sudo nmap -sU ip
```
Aquí viene lo importante, nos encontramos con tres puertos UDP abiertos y nos centraremos en el 161

### SNMP
Simple Network Management Protocol, protocolo para la gestión de la transferencia de información en redes, especialmente para uso en LAN.

Gracias a esto aprenderemos a usar los comandos para escanear dicho puerto. 

```
snmpwalk  -v 1 -c public IP
```
Posteriormente a esto encontramos algo importante que es un usuario llamado "Daniel" con su respectiva contraseña "HotelBabylon23" para conectarnos por ssh
```
ssh daniel@ip
```
Dentro vemos del directorio /home/matt el "user.txt" pero aún no tenemos los permisos para leerlo.

## MOVIMIENTO LATERAL

El siguiente paso que haremos será ver la página web que en el puerto 80 vimos, como sabemos normalmente las páginas estan guardadas en /var/www con lo cual haremos un ls -a
```
ls -al /var/www
```
Dentro encontramos el directorio "html" y así sabemos y comprobamos que lo tenemos.

El siguiente paso sera ir donde apache guarda los sitios 
```
/etc/apache2/sites-enabled/pandora.conf
```
El cual nos encontramos con este código 
```
<VirtualHost localhost:80>
  ServerAdmin admin@panda.htb
  ServerName pandora.panda.htb
  DocumentRoot /var/www/pandora
  AssignUserID matt matt
  <Directory /var/www/pandora>
    AllowOverride All
  </Directory>
  ErrorLog /var/log/apache2/error.log
  CustomLog /var/log/apache2/access.log combined
</VirtualHost>
```
Gracias a eso odemos reenviar nuestra conexión al puerto interno del host remoto y luego podremos acceder a su
contenido web. Hay varias formas de realizar el reenvío de puertos, aunque lo haremos utilizando el
Conexión SSH en sí. Usando este túnel, podemos configurar un proxy para ver la página web.
```
ssh -D 9090 daniel@ip
```
También necesitaremos configurar un proxy SOCKS en la extensión del navegador foxy-proxy para poder realizar el
El navegador enruta el tráfico a través del puerto que se reenvía.

Cuando este todo creado, en el navegador ponemos "localhost"

y aquí conseguimos la información de versión de pandora "v7.0NG.742_FIX_PERL2020"

Con esto hemos encontrado [esta](https://www.sonarsource.com/blog/pandora-fms-742-critical-code-vulnerabilities-explained/) vulnerabilidad




