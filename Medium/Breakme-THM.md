# Introducción

Hoy nos enfrentamos a una de las máquinas mas interesantes de THM, siendo de nivel Medio, (yo considero dificil).

Nos enfrentamos a una máquina en la que nos encontramos un Linux como Sistema Operativo y un Apache y un SSH

# Conectividad

Para empezar el primer paso que debemos hacer es un test de conectividad y comprobar que estamos dentro de la red.

```
┌──(root㉿kali)-[~]
└─# ping 10.10.102.26
PING 10.10.102.26 (10.10.102.26) 56(84) bytes of data.
64 bytes from 10.10.102.26: icmp_seq=1 ttl=64 time=1.03 ms
64 bytes from 10.10.102.26: icmp_seq=2 ttl=64 time=1.30 ms
^C
--- 10.10.102.26 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 1.027/1.163/1.299/0.136 ms
```

Como vemos nos encontramos a una máquina Linux (ttl=64)

# Enumeración

Para empezar solemos hacer un escaneo de puertos a la IP o si queremos meter la IP dentro de un DNS para tener mayor control del nombre, cosa que yo no voy a hacer.

```
┌──(root㉿kali)-[~]
└─# sudo nmap -sCVS -T4 -p- --min-rate 5000 10.10.102.26
Starting Nmap 7.93 ( https://nmap.org ) at 2025-02-18 14:07 UTC
Nmap scan report for ip-10-10-102-26.eu-west-1.compute.internal (10.10.102.26)
Host is up (0.0055s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 8e4f777ff6aa6adc17c9bf5a2beb8c41 (RSA)
|   256 a39c6673fcb923c00fda1dc984d6b14a (ECDSA)
|_  256 6dc20e89255510a99e416e0d819a17cb (ED25519)
80/tcp open  http    Apache httpd 2.4.56 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.56 (Debian)
MAC Address: 02:DE:B5:20:31:85 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.86 seconds
```

- 22 / ssh
- 80 / http - 2.4.56

Si nos vamos a la web alojada en el puerto 80 veremos que es un apache por defecto, normalmente en estos casos enumeramos servicios, la versión de apache y enumeramos directorios.

Para empezar suelo enumerar directorios antes que versiones, por si podemos encontrar mas información.

En mi caso voy a utilizar ffuf 

```
ffuf -w /usr/share/wordlists/dirb/big.txt:FUZZ -u http://10.10.102.26/FUZZ
```

Si nos fijamos bien encontramos dos directorios /manual y /wordpress 

Manual suele ser el manual mismo de apache en el que dudo que podamos encontrar algo, pero podríamos probar a hacer un escaneo de directorios recursivos a esta url e encontrar igual información importante.

Vamos a enumerar el wordpress a ver que encontramos, normalmente para un wordpress se utiliza wp-scan, también podemos ir enumerando manualmente y buscar o usuarios por Post o cosas diferentes.

```
wpscan --url http://10.10.102.26/wordpress
```

```
[+] wp-data-access
 | Location: http://10.10.102.26/wordpress/wp-content/plugins/wp-data-access/
 | Last Updated: 2025-02-16T23:59:00.000Z
 | [!] The version is out of date, the latest version is 5.5.34
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 5.3.5 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://10.10.102.26/wordpress/wp-content/plugins/wp-data-access/readme.txt
```

Parece que encontramos información importante como el tema que esta usando y un plugin desactualizado, pero igualmente con esto poco hacemos vamos a probar a enumerar usuarios

```
┌──(root㉿kali)-[~]
└─# wpscan --url http://10.10.102.26/wordpress --enumerate u
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.22
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://10.10.102.26/wordpress/ [10.10.102.26]
[+] Started: Tue Feb 18 14:14:38 2025

Interesting Finding(s):

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://10.10.102.26/wordpress/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] bob
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

Parece ser que hemos encontrado al usuario bob, desde aquí tiene toda la pinta de que le vamos a poder entrar por fuerza bruta.

```
wpscan --url http://10.10.102.26/wordpress -U bob -P /usr/share/wordlists/rockyou.txt

[!] Valid Combinations Found:
 | Username: bob, Password: ####
```

Como podemos ver y era un poco obvio ibamos a encontrar la pass con esto, ni me he molestado en poner el admin.

Vamos a irnos a iniciar sesión al wodpress y desde ahi enumerarlo, la cosa es que ni wp-admin ni wp-login existen, vamos a tener que encontrar la forma de loguearnos.

Parece ser que en la "sample page" hay un link al "login"

```
http://10.10.102.26/wordpress/index.php/sample-page/
```

Estamos dentro del wordpress con bob, ahora toca enumerar y no olvidarnos del plugin anteriormente encontrado ya que seguramente tenga algo que vero  no.

Enumerando el wordpress la verdad que no he encontrado una mierda, voy a buscar info de los plugins de wordpress







