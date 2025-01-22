# Conectividad

![image](https://github.com/user-attachments/assets/e34fa562-5479-4cd4-9745-0412fbda8d81)

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.237.230
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-22 11:51 GMT
Nmap scan report for 10.10.237.230
Host is up (0.00020s latency).
Not shown: 997 filtered ports
PORT   STATE  SERVICE  VERSION
20/tcp closed ftp-data
21/tcp open   ftp      vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 ftp      ftp            17 May 15  2020 test.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.209.46
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open   ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 04:d5:75:9d:c1:40:51:37:73:4c:42:30:38:b8:d6:df (RSA)
|   256 7f:95:1a:d7:59:2f:19:06:ea:c1:55:ec:58:35:0c:05 (ECDSA)
|_  256 a5:15:36:92:1c:aa:59:9b:8a:d8:ea:13:c9:c0:ff:b6 (ED25519)
MAC Address: 02:5E:41:0A:55:07 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.90 seconds
```

- 21 / FTP - Anonymous
- 22 / SSH

![image](https://github.com/user-attachments/assets/85578d42-3ce4-4c4c-bdd1-8a4187d834f8)

- Recoguemos el test.txt (vsftpd test file)

Nada importante vamos a seguir enumerando

![image](https://github.com/user-attachments/assets/39fa7acb-6ffb-4e14-a6ca-832ed0cdfc3e)

Encontramos otro arhicvo .creds

![image](https://github.com/user-attachments/assets/5be720ef-a981-44cd-914a-f6b95be0614b)

Tiene toda la pinta de ser un archivo en binario

![image](https://github.com/user-attachments/assets/3b45d316-cd7c-452f-bf73-1a5846299c3b)

Parece ser que nos da un output no muy informativo, pero en la CTF nos dicen que deberemos seguramente utilizar librerias de python y la foto de la CTF es un pepinillo con lo cuál podemos ir tirando por una libreria parecida.






