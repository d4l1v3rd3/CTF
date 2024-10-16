<img src="https://github.com/user-attachments/assets/6427dd2f-8751-48c8-9e79-1a8429d74588"  height=155 width=155>


<h1> Willow </h1>

```
udo nmap -sCV -T4 --min-rate 4000 -p- 10.10.7.8

Starting Nmap 7.60 ( https://nmap.org ) at 2024-10-16 10:02 BST
Nmap scan report for ip-10-10-7-8.eu-west-1.compute.internal (10.10.7.8)
Host is up (0.00087s latency).
Not shown: 65531 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 6.7p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   1024 43:b0:87:cd:e5:54:09:b1:c1:1e:78:65:d9:78:5e:1e (DSA)
|   2048 c2:65:91:c8:38:c9:cc:c7:f9:09:20:61:e5:54:bd:cf (RSA)
|   256 bf:3e:4b:3d:78:b6:79:41:f4:7d:90:63:5e:fb:2a:40 (ECDSA)
|_  256 2c:c8:87:4a:d8:f6:4c:c3:03:8d:4c:09:22:83:66:64 (EdDSA)
80/tcp   open  http    Apache httpd 2.4.10 ((Debian))
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Recovery Page
111/tcp  open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version   port/proto  service
|   100000  2,3,4        111/tcp  rpcbind
|   100000  2,3,4        111/udp  rpcbind
|   100003  2,3,4       2049/tcp  nfs
|   100003  2,3,4       2049/udp  nfs
|   100005  1,2,3      45528/udp  mountd
|   100005  1,2,3      57754/tcp  mountd
|   100021  1,3,4      40524/udp  nlockmgr
|   100021  1,3,4      57168/tcp  nlockmgr
|   100024  1          39072/udp  status
|   100024  1          54480/tcp  status
|   100227  2,3         2049/tcp  nfs_acl
|_  100227  2,3         2049/udp  nfs_acl
2049/tcp open  nfs_acl 2-3 (RPC #100227)
MAC Address: 02:3E:43:0F:ED:FB (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.62 seconds
```

- Puerto 22
- Puerto 80
- Puerto 111
- Puerto 2049

```
showmount ip
mount -t nfs 10.10.7.8:/var/failsafe new -o nolock
```
```
cat rsa_keys 
Public Key Pair: (23, 37627)
Private Key Pair: (61527, 37627
```

En la web encontramos un ponto de numeros 

![image](https://github.com/user-attachments/assets/771a338a-e673-4ffe-866e-5407a79b9ee2)

Si pasamos lo que encontramos por cyberchief nos da una pequeña pista y parece ser un nombre @Willow

![image](https://github.com/user-attachments/assets/6983f7d5-ee3d-41df-b69d-d209020b7659)

Como anteriormente hemos sacado el par de llaver podemos definir el numero

## Desencripttación

Ahora que sabemos el nombre del archivo "rsa_keys" podemos desencriptar el mensaje (nos dan un hint)

Vamos a coger el programita de python

```
import argparse

parser = argparse.ArgumentParser(description="Decode RSA")
parser.add_argument("file", help="The file containing the encrypted text")
parser.add_argument("d", help="The Private Key", type=int)
parser.add_argument("n", help="The Modulus", type=int)
args=parser.parse_args()

with open(args.file, "r") as coded:
    data = [int(i.strip("\n")) for i in coded.read().split(" ")]

for i in data:
    print(chr(i**args.d % args.n), end="")
```



