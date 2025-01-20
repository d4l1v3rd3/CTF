# Conectividad

![image](https://github.com/user-attachments/assets/86ccf26f-4f42-4816-9071-148a03cb1ec7)

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.221.64
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-20 11:41 GMT
Nmap scan report for 10.10.221.64
Host is up (0.00022s latency).
Not shown: 996 closed ports
PORT    STATE SERVICE VERSION
21/tcp  open  ftp     vsftpd 3.0.2
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 56:50:bd:11:ef:d4:ac:56:32:c3:ee:73:3e:de:87:f4 (DSA)
|   2048 39:6f:3a:9c:b6:2d:ad:0c:d8:6d:be:77:13:07:25:d6 (RSA)
|   256 a6:69:96:d7:6d:61:27:96:7e:bb:9f:83:60:1b:52:12 (ECDSA)
|_  256 3f:43:76:75:a8:5a:a6:cd:33:b0:66:42:04:91:fe:a0 (ED25519)
80/tcp  open  http    Apache httpd
|_http-server-header: Apache
|_http-title: Purgatory
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          33330/udp   status
|   100024  1          37084/tcp   status
|   100024  1          57177/tcp6  status
|_  100024  1          60277/udp6  status
MAC Address: 02:6E:A9:1E:26:D9 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.55 seconds
```

- 21 / FTP
- 22 / SSH
- 80 / HTTP
- 111 / RCP

Encontramos el directorio "island" con FFUF

Posteriormente:

![image](https://github.com/user-attachments/assets/f4031fb8-ed17-4e89-bf76-ac3b24d4472f)

Después de enumerar no encuentro nada con el HINT vemos que es un numero vamos a hacer un FFUF de numeros de directorio al principal (NADA)

Hacemos lo mismo en /island - Encontramos el directorio 2100

![image](https://github.com/user-attachments/assets/38ae7b25-81cb-4a63-9bd8-ec526c0ba5bd)

También otra cosa que no nos dejamos por alto dentro de /island tenemos en el HTML "vigilante" igual nos sirve en un futuro

![image](https://github.com/user-attachments/assets/ba38baab-afc2-4b5e-b108-58d454e8f721)

![image](https://github.com/user-attachments/assets/e66a85e1-f800-48e2-a3ce-58635f9660a3)

Viendo en el código después de tantos fuzzing vamos a hacer un fucking con la extensión .ticket

![image](https://github.com/user-attachments/assets/532b1a69-b9ef-4712-86c1-e9bf9abcf4be)

![image](https://github.com/user-attachments/assets/7a8f5642-41f3-4bba-a3fa-43577d3a2f1a)

Parece que tenemos un token vamos a pasarlo por Cyberchief a ver si sacamos algo

Parece ser codifico en base58

![image](https://github.com/user-attachments/assets/393d246a-88fe-4134-a46e-e2762bb1de12)

!#th3h00d

Vamos a probar a conectarnos via ftp o via ssh vamos a probar las dos con las credenciales: vigilante:!#th3h00d

![image](https://github.com/user-attachments/assets/0bebeca5-fd4c-4477-846d-9b8a5385e1fe)

Estamos dentro del FTP a ver que podemos sacar

![image](https://github.com/user-attachments/assets/bc5c3407-106b-4986-b352-1261ca7908b7)

Tenemos varias archivos importantes, los descargamos todos y encontramos dos archivos chulos el otheruser y el aa.jpg

probamos con la contraseña: password por la cara y si funciona

```
steghide extract -sf aa.jpg
```

Encontramos parcee ser una contraseña en el archivo "sado"

En el anterior archivo que hemos visto parece ser el usuario slade:M3tahuman

vamos a probar la conexión

Estamos dentro

![image](https://github.com/user-attachments/assets/a52251ea-6d34-46c4-9de5-6240cc67d8cc)

Una vez esto hacemos un sudo -l -l

En que encontramos que la función pkexec tenemos opciones de root

Gtfobins - pkexec teneis la respuesta super simple y tenemos root

GG!!!!!!!!!!



