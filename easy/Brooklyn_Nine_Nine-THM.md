# Brooklyn Nine Nine

# Conectividad

![image](https://github.com/user-attachments/assets/f9ed2f82-d74b-462d-8a24-3207ebd9a8fb)

- Parece ser que nos enfrentamos a una máquina Linux (ttl=64)

# Enumeracion

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.224.208
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-21 12:04 GMT
Nmap scan report for 10.10.224.208
Host is up (0.0060s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.2.226
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 16:7f:2f:fe:0f:ba:98:77:7d:6d:3e:b6:25:72:c6:a3 (RSA)
|   256 2e:3b:61:59:4b:c4:29:b5:e8:58:39:6f:6f:e9:9b:ee (ECDSA)
|_  256 ab:16:2e:79:20:3c:9b:0a:01:9c:8c:44:26:01:58:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 02:06:EF:88:FC:97 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- 21 / FTP - Anonymous
- 22 / SSH
- 80 / HTTP

Vamos a empezar enumerando el FTP a ver si encontramos algun recurso importante, no hago otro escaner, pero si es necesario lo hare posterior.

En el FTP encontramos un archivo note_to_jake.txt vamos a leerlo

```
From Amy,

Jake please change your password. It is too weak and holt will be mad if someone hacks into the nine nine
```

Parece ser que tenemos un usuario:jake que tiene una contraseña bastante fácil, podemos probar a hacer fuerza bruta al ssh pero vamos a enumerar también el puerto 80 a ver si encontramos algo interesante.

Parece ser que en el código fuente tenemos una imagen y nos esta diciendo si sabemos algo de esteganografía, vamos a descargala a ver

- brooklyn99.jpg

Parece ser que tiene una contraseña embedida tendremos que crackearla

![image](https://github.com/user-attachments/assets/ab9abac7-69ea-4741-bf25-dc91b7657cd0)

https://github.com/RickdeJager/stegseek

Una vez lo tenemos descargado vamos a ello. 

![image](https://github.com/user-attachments/assets/f23a8c46-069a-4bf4-9129-1e6da2732044)

La contraseña era... admin madre mia

Lo extraemos:

```
steghide extact -sf brooklyn99.jpg
```

y parece ser que nos dan unos credenciales para entrar imagino por ssh

```
holt:fluffydog12@ninenine
```

![image](https://github.com/user-attachments/assets/eebdfcab-b17b-4bbe-8a53-204223d8df0e)

Sacamos la primera flag ahora escalaremos privilegios

# Escala de privilegios

Ahora desde aquí podemos hacer dos cosas muy simples

```
sudo -l -l
```

![image](https://github.com/user-attachments/assets/3060e255-d238-49b1-8af8-8f2e87b46241)

Sabiendo que tenemos el sudo de nano para que queramos tenemos miles de posibilidades...

- Hacer un rev shell en un archivo en root
- Coger las keys de ssh
- Cambiar la contraseña de root o quitarle la contraseña

Yo voy a terminar la room fácil simplemente un 

```
sudo nano /root/root.txt
```

GG!!!!!!!!!!!!!!!




