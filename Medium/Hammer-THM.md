# Conectividad

![image](https://github.com/user-attachments/assets/92b3491d-540e-454a-bdad-79c80066db47)

# Enumeración

Parece que nos estamos enfrentando a una máquina Linux ttl=64

Con una escáner de purtos básicos encontramos solo el puerto 22 abierto, si luego hacemos con el parametro -p-:

```
sudo nmap -sCV -T4 -p- --min-rate 4000 10.10.179.183
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-30 07:52 GMT
Nmap scan report for 10.10.179.183
Host is up (0.00029s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
1337/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Login
MAC Address: 02:7F:13:6C:17:99 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.58 seconds
```

![image](https://github.com/user-attachments/assets/45d04405-1de6-4810-b409-1114d5389c8d)

Parece ser que nos encontramos con un login a ver si podemos enumerar y encontrar algun vector para saltear o enumerar

- Primero de todo he pensado en enumerar correos electronicos a base de "forgot your password" pero no es factible
- Por otra parte enumerar direcotrios, si nos fijamos en el código fuente encontramos que si enumeramos tal deberemos empezar por _hmr con lo cuál con ffuf vamos a hacerlo

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.179.183:1337/hmr_FUZZ
```

- css
- js
- logs
- images

Vamos a ir enumerando a ver si encontramos algo interesante

![image](https://github.com/user-attachments/assets/b74048bd-aa98-453a-bf0b-83435fcb5c94)

![image](https://github.com/user-attachments/assets/40bac6ae-1cce-41f6-8a34-b4c94b01d636)

Parece ser que en los logs encontramos info intersenate como un usuario = tester:Mismatch

tester@hammer.thm 

Mismatch

![image](https://github.com/user-attachments/assets/c6538d2a-29ac-4328-ba76-cb846367e466)

Vamos a ver si nos conectamos a la web, porque por ssh ya os digo que no va otra cosa que apuntar /restricted-area

# Explotación

Parece ser que vamos a tener que bypassear el reseteo de password vamos a ello


# Escala de privilegios

