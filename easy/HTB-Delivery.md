#by d4l1

<p align="center"><img src="https://github.com/user-attachments/assets/f9990bea-bf1f-4946-adfe-15d92d104bd7"></p>
<h1 align="center">Delivery</h1>

# ÍNDICE

# INICIO

Hoy nos enfrentamos a la máquina "Delivery" vamos a hacer una enumeración de información

- Test de conectividad:

  ![image](https://github.com/user-attachments/assets/a18e0202-b5a5-45f8-8835-a1630e185ada)

- Escaner de puertos:

 ![image](https://github.com/user-attachments/assets/9414c415-c8e5-41d3-9ea8-504601a31926)
 
 Aquí solo encontramos 2 puertos TCP 22 (ssh) y el 80 (http)
 
 ![image](https://github.com/user-attachments/assets/78e659db-43ef-470e-b199-264895b3fa68)
 
Nos falta por aquí el puerto (8065) que no sabemos nada de el 
 
- Sistema Operativo:

  ![image](https://github.com/user-attachments/assets/3a957d2c-25da-485e-a591-bddda8c0593e)

Linux

## ENUMERACIÓN

Empezamos enumerando los servicios y a ver si podemos hacer algo con ellos.

Con un escaner más fuerte al puerto que no sabiamos anda nos encontramos un dominio (cdn.rudderlabs.com) en la que tenemos una página web. 

![image](https://github.com/user-attachments/assets/5aec8b4f-fa65-45c4-8ea4-b389046c7f99)

Encontramos en ese puerto un /login pero en el puero 80 encontramos una página normal

![image](https://github.com/user-attachments/assets/d7d05ca8-2e60-434b-b12f-54664223fcee)

Después de ver por la página no encontramos nada importante, lo que haremos ahora será hacer un escaner de subdirectorios dentro del dominio @delivery.htb

Probemos con ffuf

Primero de todo deberemos añadir dicho dominio en nuestro hosts
```
echo "10.10.10.222 delivery.htb" | sudo tee -a /etc/hosts
```
Nada he probado con subdominios pero no encuentro nada.

![image](https://github.com/user-attachments/assets/43b80cf7-ac04-46e2-a384-30a8e20522e8)

La cosa era más fácil de lo que pensaba simplemente era pulsar dentro de "HelpDesk" y nos salía el dominio jaja

![image](https://github.com/user-attachments/assets/059b6c5f-dcae-4df9-98ec-843a16ac35cd)

Tenemos el dominio "helpdesk.delivery.htb" añadamoslo

Nos encontramos con un sistema de tickets, probemos a crear uno a veer que pasa

Genial tenemos al disponibilidad de crear. 

![image](https://github.com/user-attachments/assets/7cc2961b-220c-41b3-ae9a-d9dfffa0483c)

Dentro del puerto 8065 nos encontramos esto

![image](https://github.com/user-attachments/assets/2fcbdc37-eb7c-4874-a7dc-496bfadbddcd)

Vemos que podemos crear una cuenta pero nos pide un email de verificacion, vamos a crearnos uan cuenta con temp-mail

Vale probemos otra cosa, probare con el email que nos dan en el ticket y a ver si nos envian algo ahi.

Creamos un ticket nos daun un codigo y el email

![image](https://github.com/user-attachments/assets/4d9e28fe-6e1e-41b5-98ad-e299b09ce149)

Porfin conseguimos el email después de tanto 

![image](https://github.com/user-attachments/assets/7149a54a-e310-4e3c-bb85-1c75801e4792)

Estamos dentro

![image](https://github.com/user-attachments/assets/768bdaac-31ae-45e0-a896-105eddf08279)

Vemos dentro un chat interno en el cuál vemos gente hablando. 

Gracias a las credenciales que nos da root maildeliverer:Youve_G0t_Mail!

nos metemos por ssh a dicha cuenta

![image](https://github.com/user-attachments/assets/61132eb3-c39b-43dc-bac3-11d6e9d42256)

Tenemos la flag user.txt

Ahora deberemos enumerar todo lo que disponemos y por ejemplo empezar por la aplciación "matermat" estaría bien 

Ruta encontrada vamos a ver lo que encontramos 

![image](https://github.com/user-attachments/assets/fcd51a02-384b-440a-abd6-a00f90b0ec83)

mmuser:Crack_The_MM_Admin_PW (Esto esta dentro del archivo que hemos leido) vemos que esta dentro de la misma red

![image](https://github.com/user-attachments/assets/4dc959a8-15f2-46bf-b7a1-9b31ec9b6070)

Esto nos esta dando las credenciales de la sql

```
mysql -u mmuser -p
use mattermost;
```

![image](https://github.com/user-attachments/assets/1e652d05-a9fc-40b4-96ff-40ebd1d34718)

Vamos a ver si encontramos algo dentro de "users"
```
select * from Users;
```

![image](https://github.com/user-attachments/assets/68fc9902-fe7f-4562-893e-0c97df7623ad)

Encontrado y tenemos el hash

```
echo "$2a$10$VM6EeymRxJ29r8Wjkr8Dtev0O.1STWb4.4ScG.anuu7v0EFJwgjjO" > hash
```
He intentado usar el john de ripper fácilmente pero no llego a nada.

Después de leer algun write up se me habia pasado la frase de "PleaseSuscribe!" y crear una wordlists desde ahi.
```
echo PleaseSubscribe! | hashcat -r /usr/share/hashcat/rules/best64.rule --stdout
```

![image](https://github.com/user-attachments/assets/d7599da8-bc4b-4f8f-bda3-32818cc98a5f)

![image](https://github.com/user-attachments/assets/b60ab857-e755-40c6-bb4e-fb88a5aee0a2)

GG











