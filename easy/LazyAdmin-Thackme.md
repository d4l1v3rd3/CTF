<h1 alig="center">LazyAdmin</h1>

# INTRODUCCIÓN

Máquina Linux fácil para practicas nuestras habilidades.

Test de conectividad:

```
ping ip
```
![image](https://github.com/user-attachments/assets/26e92704-17fb-4a65-be43-3a9c0ec6e7e5)

Escaneo de puertos:

```
sudo nmap -sCV -T4 --min-rate 4000 ip
```

![image](https://github.com/user-attachments/assets/d935efa7-01f0-4100-ad38-f5eec94082c8)

Podemos poner si quremos un -p- o un -Pn en otros casos por si queremos abarcar más.

En la página principal nos encontramos con un apache sin configurar aún.

![image](https://github.com/user-attachments/assets/12a4c304-d01a-490b-b782-1a47b12aa7a6)

Lo primero que hare sera hacer un escaner de directorios con ffuf

```
ffuf -w wordlist:FUZZ -u ip/FUZZ
```

Vemos un directorio llamado /content/ 

![image](https://github.com/user-attachments/assets/5d336369-e66a-458e-818a-aa7383f293c4)

Nos encontramos en una página que se llama "SweetRice" busquemos si tiene algun exploit o vulnerabilidad

![image](https://github.com/user-attachments/assets/83ced06b-c69c-46bd-94c9-68eb48a70104)

![image](https://github.com/user-attachments/assets/a727c5fd-c54a-4aa3-b0ba-229f05253233)

Vemos que necesitamos un usuario y contraseña cosa que ahora no disponinemos. Probaremos a hacer otro escaner de directorios recursivo al ya encontrado

Gracias a esto encontramos el directortio /inc/

![image](https://github.com/user-attachments/assets/b8cd4ca1-a0a1-48a6-806f-0473d848c1f9)

Si investigamos nos encontramos con una backup de una base de datos.

![image](https://github.com/user-attachments/assets/f8ed6a86-7eea-40ab-95a9-ada58212f943)

En la que nos encontramos al usuario "manager" y un hash 

![image](https://github.com/user-attachments/assets/dbf1f359-b37a-4750-bc6e-3742d4111472)

Si lo desencriptamos simplemente sacamos la pass

![image](https://github.com/user-attachments/assets/2e60d2c0-a699-4ee1-9a83-0dc0b42725ce)

Esto nos da el acceso al dashboard y también acceso a poder utilizar el anterior exploit.

Gracias al anterior escaneo encontramos el directorio /as en el que es un dashboar de admin veamos si podemos entrar.

![image](https://github.com/user-attachments/assets/cd87b725-2cf5-4f8f-afc5-ac23e0ea75e9)

![image](https://github.com/user-attachments/assets/6c1fc10c-c64d-434a-8e32-26ebf9a9f666)

Dentro realmente no encontramos muchas cosas importantes pero podemos usar el exploit probremos.

Primero de todo deberemos tener un reverse shell

![image](https://github.com/user-attachments/assets/b9c1cdc3-50d7-442e-acdc-dc3ccc68ff20)

Simplemente utilizamos un rev shell lo ponemos en formato ".phtml" y en "media center" lo subimos hacemos un nc para estar en escucha en el puerto elegido y lo ejecutamos.

![image](https://github.com/user-attachments/assets/53f4c398-d344-4084-8e62-9e31383c5d02)

```
/bin/bash -i
```
 y sacamos la primera flag 

 ![image](https://github.com/user-attachments/assets/128a9eba-941d-4ea9-a09f-56a125dfcf46)

Si hacemos un "sudo -l" 

Vemos qeu tenemos posibilidad de ejecutar el /home/itguy/backup.pl 

![image](https://github.com/user-attachments/assets/329d7f0f-9d32-49f0-b57e-c4f11aa1f6a1)

Vemos que dicho archivo se dirige a otro 

![image](https://github.com/user-attachments/assets/e36b05ff-7c4f-44b6-b084-0409f2fb2d37)

vamos aver que tiene "copy.sh"

![image](https://github.com/user-attachments/assets/da95a934-c99e-4b39-8597-73b3d6532cc4)

Gracias a esto podemos hacer una simple modificación una copia del /bin/bash y una 

```
echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > /etc/copy.sh

sudo /usr/bin/perl /home/itguy/backup.pl

ls -la /tmp/bash

/tmp/bash -p
```









