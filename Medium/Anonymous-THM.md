# Anonymous

# Conectividad

![image](https://github.com/user-attachments/assets/c5118fad-9e91-4d50-b070-7ca8181bdb79)

- Damos por hecho que es una máquina Linux (ttl=64)

# Enumeración

```
udo nmap -sCV -T4 --min-rate 4000 10.10.13.16
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-21 09:36 GMT
Nmap scan report for 10.10.13.16
Host is up (0.00027s latency).
Not shown: 996 closed ports
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.104.182
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8b:ca:21:62:1c:2b:23:fa:6b:c6:1f:a8:13:fe:1c:68 (RSA)
|   256 95:89:a4:12:e2:e6:ab:90:5d:45:19:ff:41:5f:74:ce (ECDSA)
|_  256 e1:2a:96:a4:ea:8f:68:8f:cc:74:b8:f0:28:72:70:cd (ED25519)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
MAC Address: 02:0D:E6:1D:DF:8B (Unknown)
Service Info: Host: ANONYMOUS; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: ANONYMOUS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: anonymous
|   NetBIOS computer name: ANONYMOUS\x00
|   Domain name: \x00
|   FQDN: anonymous
|_  System time: 2025-01-21T09:37:09+00:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-01-21T09:37:09
|_  start_date: N/A
```

- 21 / FTP - Con Anonymous
- 22 / SSH
- 139 / SMB
- 445 / SMB

Nos conectamos al FTP por Anonymous, vemos que tenemos tres ficheros:

- clean.sh
- removed_files.log
- to_do.txt

No vemos información realmente importante por aquí, vamos a probar por el smb

Encontramos el directorio pics

```
smbclient -L ip
```

Dentro del mismo directorio encontramos dos imagenes

- corgo2.jpg
- puppos.jpeg

Vamos a ver que podemos hacer



# Explotación
