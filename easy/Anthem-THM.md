# INTRODUCCIÓN

Nombre : Anthem

Sistema operativo : Windows

# ENUMERACION

Test conectividad

En este caso los paquetes ICMP no pasan, pero eso no significa que no haya conectividad.

Escáner puertos

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.174.38

Starting Nmap 7.60 ( https://nmap.org ) at 2024-09-25 08:29 BST
Nmap scan report for ip-10-10-174-38.eu-west-1.compute.internal (10.10.174.38)
Host is up (0.00041s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=WIN-LU09299160F
| Not valid before: 2024-09-24T07:26:22
|_Not valid after:  2025-03-26T07:26:22
|_ssl-date: 2024-09-25T07:29:25+00:00; 0s from scanner time.
MAC Address: 02:FD:A8:DE:76:C3 (Unknown)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 92.24 seconds
```

Como vemos nos encontramos el puerto 80 abierto con un servidor web.

También encontramos el puerto 3389 con un RDP (Remote Desktop Service)

Como es obvio vamos a ir a la web a ver que encontramos.

![image](https://github.com/user-attachments/assets/12f7161b-4240-4a9b-b0ff-bb840bb5e23e)

Vemos que es un blog con el dominio "Anthem.com" investigando un poco encontramos dos usuarios "james Orchard Halliwell" y "Jane Doe" 

También encontramos un correo "JD@anthem.com" 

También nos dirijimos al archivo "robots.txt"

```
UmbracoIsTheBest!

# Use for all search robots
User-agent: *

# Define the directories not to crawl
Disallow: /bin/
Disallow: /config/
Disallow: /umbraco/
Disallow: /umbraco_client/
```

Genial con todo esto vamos a ver si encontramos más cosas, posiblemente haga un escaner de directorios. Y si no encontramos nada uno de VHOST

```
ffuf -w path:FUZZ -u http://ip/FUZZ
```

Nos encontramos con un directorio muy interesante /Install y nos lleva a /umbraco/#/login

Vamos a ver si podemos encontrar algo desde aquí.

Sabemos que tenemos un login en "umbraco" y que el administrador tiene toda la pinta que es uno de los blogeros, vemos que en el robots.txt encontramos una contraseña, vamos a probar a ver si nos podemos conectar por rdp.

También descubrimos la cuenta del admin poniendo el poema en google "Solomon Grundy" y el correo es igual que el ejemplo anterior.

```
apt-get install rdesktop
rdesktop -u sg ip
```

![image](https://github.com/user-attachments/assets/22338888-67f5-47cd-b64e-5a5838347d7f)

Hay una forma muy rápida para sacar todas las flags de código fuente y es descargandose la página web entera

```
wget --recursive http://ip
```

Podemos localizar todas las flags grepeando

```
grep -R 'THM' .
./index.html:        <input type="text" name="term" placeholder="Search... 	THM{G!T_G00D}" />
./authors/jane-doe/index.html:        <input type="text" name="term" placeholder="Search... 								THM{G!T_G00D}" />
./authors/jane-doe/index.html:                <p>Website: <a href="THM{L0L_WH0_D15}">THM{L0L_WH0_D15}</a>
./tags:        <input type="text" name="term" placeholder="Search... 		THM{G!T_G00D}" />
./categories:        <input type="text" name="term" placeholder="Search... 	THM{G!T_G00D}" />
./archive/a-cheers-to-our-it-department/index.html:<meta content="THM{AN0TH3R_M3TA}" property="og:description" />
./archive/a-cheers-to-our-it-department/index.html:        <input type="text" name="term" placeholder="Search... 						THM{G!T_G00D}" />
./archive/we-are-hiring/index.html:<meta content="THM{L0L_WH0_US3S_M3T4}" property="og:description" />
./archive/we-are-hiring/index.html:        <input type="text" name="term" placeholder="Search... 								THM{G!T_G00D}" />
```

# PASOS FINALES

Ya dentro de el RDP vamos a ver que hacemos primero de todo cogemos la flag user.txt

Vamos a enumerar archivos por windows que sean ocultos.

![image](https://github.com/user-attachments/assets/b9e70d70-45c1-4f87-b765-4550982d0dc3)

Encontramos 2 directorios ocultos, uno que siempre existe y un "backup" vamos a ver pero no tenemos permisos para abrir este archivo.

Vamos a probar a añadirnos nosotros como usuarios que podemos leer jaja

![image](https://github.com/user-attachments/assets/cf05fcd5-577b-48fd-9699-cf7d320f9c25)

Funciona!!!

Tiene toda la pinta que es la password del admin = ChangeMeBaby1MoreTime

![image](https://github.com/user-attachments/assets/0a3f52ca-bd34-4a78-bc1c-8adf2c4df009)

Pues parece ser que todo esta correcto, ahora simplemente nos vamos al root.txt y terminamos la máquina

GG!!


