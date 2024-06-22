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
