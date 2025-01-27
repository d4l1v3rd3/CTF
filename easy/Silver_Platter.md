# Introducción

Piensas que eres el hacker más inteligente?, encuentra las flags ocultas y enseñale al mndo tus hack skills

Tenemos un servidor fortificado a ataques comunes y con unas contraseñas de politicas que son muy complicadas de crackear pero (Han mirado la rockyou.txt).

# Conectividad

![image](https://github.com/user-attachments/assets/309f50cf-0f67-4138-bfe8-15f32854cea2)

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.59.156
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-27 15:29 GMT
Nmap scan report for 10.10.59.156
Host is up (0.00043s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http       nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Hack Smarter Security
8080/tcp open  http-proxy
| fingerprint-strings: 
|   FourOhFourRequest, GetRequest, HTTPOptions: 
|     HTTP/1.1 404 Not Found
|     Connection: close
|     Content-Length: 74
|     Content-Type: text/html
|     Date: Mon, 27 Jan 2025 15:29:48 GMT
|     <html><head><title>Error</title></head><body>404 - Not Found</body></html>
|   GenericLines, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SMBProgNeg, SSLSessionReq, Socks5, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Length: 0
|_    Connection: close
|_http-title: Error
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8080-TCP:V=7.80%I=7%D=1/27%Time=6797A66C%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,C9,"HTTP/1\.1\x20404\x20Not\x20Found\r\nConnection:\x20close\r
SF:\nContent-Length:\x2074\r\nContent-Type:\x20text/html\r\nDate:\x20Mon,\
SF:x2027\x20Jan\x202025\x2015:29:48\x20GMT\r\n\r\n<html><head><title>Error
SF:</title></head><body>404\x20-\x20Not\x20Found</body></html>")%r(HTTPOpt
SF:ions,C9,"HTTP/1\.1\x20404\x20Not\x20Found\r\nConnection:\x20close\r\nCo
SF:ntent-Length:\x2074\r\nContent-Type:\x20text/html\r\nDate:\x20Mon,\x202
SF:7\x20Jan\x202025\x2015:29:48\x20GMT\r\n\r\n<html><head><title>Error</ti
SF:tle></head><body>404\x20-\x20Not\x20Found</body></html>")%r(RTSPRequest
SF:,42,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Length:\x200\r\nConn
SF:ection:\x20close\r\n\r\n")%r(FourOhFourRequest,C9,"HTTP/1\.1\x20404\x20
SF:Not\x20Found\r\nConnection:\x20close\r\nContent-Length:\x2074\r\nConten
SF:t-Type:\x20text/html\r\nDate:\x20Mon,\x2027\x20Jan\x202025\x2015:29:48\
SF:x20GMT\r\n\r\n<html><head><title>Error</title></head><body>404\x20-\x20
SF:Not\x20Found</body></html>")%r(Socks5,42,"HTTP/1\.1\x20400\x20Bad\x20Re
SF:quest\r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n")%r(Gener
SF:icLines,42,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Length:\x200\
SF:r\nConnection:\x20close\r\n\r\n")%r(Help,42,"HTTP/1\.1\x20400\x20Bad\x2
SF:0Request\r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n")%r(SS
SF:LSessionReq,42,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Length:\x
SF:200\r\nConnection:\x20close\r\n\r\n")%r(TerminalServerCookie,42,"HTTP/1
SF:\.1\x20400\x20Bad\x20Request\r\nContent-Length:\x200\r\nConnection:\x20
SF:close\r\n\r\n")%r(TLSSessionReq,42,"HTTP/1\.1\x20400\x20Bad\x20Request\
SF:r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n")%r(Kerberos,42
SF:,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Length:\x200\r\nConnect
SF:ion:\x20close\r\n\r\n")%r(SMBProgNeg,42,"HTTP/1\.1\x20400\x20Bad\x20Req
SF:uest\r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n")%r(LPDStr
SF:ing,42,"HTTP/1\.1\x20400\x20Bad\x20Request\r\nContent-Length:\x200\r\nC
SF:onnection:\x20close\r\n\r\n")%r(LDAPSearchReq,42,"HTTP/1\.1\x20400\x20B
SF:ad\x20Request\r\nContent-Length:\x200\r\nConnection:\x20close\r\n\r\n");
MAC Address: 02:98:C9:C7:87:8D (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/
```

- 22 / ssh
- 80 / http nginx 1.18.0
- 8080 / http

![image](https://github.com/user-attachments/assets/2061e272-2b3f-4237-add3-f6e47988633d)

Usuario enumerado: scr1ptkiddy

En el readme.txt encontramos esto:

```
Dimension by HTML5 UP
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)


This is Dimension, a fun little one-pager with modal-ized (is that a word?) "pages"
and a cool depth effect (click on a menu item to see what I mean). Simple, fully
responsive, and kitted out with all the usual pre-styled elements you'd expect.
Hope you dig it :)

Demo images* courtesy of Unsplash, a radtastic collection of CC0 (public domain) images
you can use for pretty much whatever.

(* = not included)

AJ
aj@lkn.io | @ajlkn


Credits:

	Demo Images:
		Unsplash (unsplash.com)

	Icons:
		Font Awesome (fontawesome.io)

	Other:
		jQuery (jquery.com)
		Responsive Tools (github.com/ajlkn/responsive-tools)
```

Sabemos que han utilizado HTML5 

He probado a hacer un ffuf y no he encontrado gran información

Enumerando el código encontramos la ruta /#elements y además tenemos accesos a todos los recuros .css y .js

Parece ser que no vamos a encontrar mucha información, voy a probar por suerte enumerar el 8080 a ver 

A la primera

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.59.156:8080/FUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.59.156:8080/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

:: Progress: [40/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [541/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [1093/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: E:: Progress: [1574/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Ewebsite                 [Status: 302, Size: 0, Words: 1, Lines: 1]
:: Progress: [2105/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: E:: Progress: [2159/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: E:: Progress: [3087/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Econsole                 [Status: 302, Size: 0, Words: 1, Lines: 1]
ebsite                 [Status: 302, Size: 0, Words: 1, Lines: 1]
:: Progress: [2105/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: E:: Progress: [2159/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: E:: Progress: [3087/220560] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Econsole                 [Status: 302, Size: 0, Words: 1, Lines: 1]

```

Pues nada tampoco jaja, uno da Forbidden y el otro 404

Después de mirar un wp vemos que en Contact había que coger y luego de hay saber que hay una ruta en la 8080 un silverpeas jajaja por la cara pero bueno

![image](https://github.com/user-attachments/assets/f1c6dfa9-cd08-43bd-af69-ff60c26135f0)

Sabemos que hay un usuario llamado "scr1ptkiddy"

Si somos un poco curiosos y nos fijamos en los derechos reservados esta versión es hasta el 2022 con lo cuál cualquier vulnerabilidad de silverpeas posteiror pues funcionara.. 

Después de epxlorar encontramos una autheticacion bpyass CVE-2024-36042

![image](https://github.com/user-attachments/assets/2d61d4fc-7c80-45b2-858a-4960e90f7c60)

Simplemente cogemos la requeest con el Burp y quitamos la pass y hacemos un forward

![image](https://github.com/user-attachments/assets/72b819e2-f48c-4be3-9992-39ffbec05a33)

Para ir enumerando sabemos que tiene mas CVE como la CVE-2023-47323 para poder leer todos los mensajes

```
http://localhost:8080/silverpeas/RSILVERMAIL/jsp/ReadMessage.jsp?ID=[messageID]
```

Si vamos explorando entre 1,2,3 ,etc 

![image](https://github.com/user-attachments/assets/b6a85975-ee6f-4d5b-ae34-3b702ce94241)

Encontramos esto

Vamos a probar a conectarnos por ssh ejej

tim:cm0nt!md0ntf0rg3tth!spa$$w0rdagainlol 

Puede que este no valga para ssh

# Explotación

![image](https://github.com/user-attachments/assets/8d4a546e-4126-42af-994f-941f9d0f684d)

Estamos dentro y ahora podemos ir a por la primera flag que es la de uusario

![image](https://github.com/user-attachments/assets/57e3737a-83a7-4908-927d-69d49d6d13ae)

Ahora vamos a escalar privilegios

# Escala de privilegios

Si enumeramos los permisos parece que pertenecemos al grupo de adm

![image](https://github.com/user-attachments/assets/be5e9f88-25fc-4715-83a7-8041362cee5e)

Con el sudo parece ser que no encontramos nada ni tenemos permisos de nada

Vamos a ir enumerando archivos 

```
cat /var/log/auth* | grep -i pass
```

![image](https://github.com/user-attachments/assets/cee11d2d-53eb-4723-a45b-ec28623a66c9)

Vaya vayaaaaa

![image](https://github.com/user-attachments/assets/e22acfd8-d874-4f70-b27e-cc2dcf1b689f)

Parece ser que esto se esta volviendo divertido

![image](https://github.com/user-attachments/assets/a932770d-94df-481e-9828-b014eaff6d62)

GG!!!!!!!! pensaba que iba a ser mas dificil esta parte por eso es fácil porque por lo demás...

Esta guay simplemente ahora o podemos ser sudo 

```
sudo su
```

 O simplemente ir a leer la root.txt

 ```
sudo cat /root/root.txt
```

GG
