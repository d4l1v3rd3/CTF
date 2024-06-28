# CAP

Hoy haremos la máquina Linux easy Cap de HTB, nos encontraremos con un servicio HTTP en la que deberemos capturar la flag .

## INTRODUCCIÓN

Como siempre lo principal que haremos es comprobar el sistema operativo y la conectividad.
```
ping -c 1 10.10.10.245
```
y el script que tengo en mi repositorio para darnos cuenta que es un sistema oeprativo Linux.

Posteriormente haremos el escaner de puertos con nmap
```
sudo nmap -sCV -T4 --min-rate 4000 10.10.10.245
```
Nos encontramos tres puertos abiertos el 21 - ftp 22- ssh 80 - http

Posteriormente a esto visitamos la web alojada

```
http://10.10.10.245
```
Nos encontramos con un "Dahboard" con diferentes apartados y yo creo que nos centraremos en los servicios y puertos que corren gracias al "network status"

Si nos vamos al apartado de "security snapshot" podemos descargar la trazabilidad de los paquetes y posteriormente leernlos con whireshark.

Si inspeccionamos la URL vemos un /data/1 si lo probamos a cambiar a /data/0 y nos descargamos esos paquetes, veremos algo bastante curioso.

Paquetes por FTP con el usuario y contraseña de ssh para conectarnos.

```
nathan / Buck3tH4TF0RM3!
```
Vamos a conectarnos via ssh

Con esto nos conectamos y tenemos facilita la primera flag de usuario.

Ya dentro podemos utilizar el script de linPEAS para aprovechar otros vectores de privilegios. 
```
curl nuestra ip por hhtp linpeas.sh
```
El reporte que nos da el script contiene datos interesantes la ruta /usr/bin/python3.8 debe tener cap_setuid que esto alude al proceso de ganar privilegios de SUID (root)

si hacemos un 
```
/usr/bin/python3.8
```
```
id
```
nos daremos cuenta que somos root
gg
