<h1 align="center"> Biohazard </h1>

# INTRODUCCIÓN

Biohazard es una CTF basada en el viejo juego de horror survival, Resident Evil.

Es un CTF basado en un puzle. En lo que recolectaremos objetos, resolviendo el objeto para escapar. Podremos sobrevivir?

# ENUMERACIÓN

Test Conectividad:

![image](https://github.com/user-attachments/assets/0baa4d79-9d3b-4c28-b94a-6383d7889107)

Escaner puertos y servicios:

```
sudo nmap -sCV -T4 -p- --min-rate 4000 <ip>
```

# MANSIÓN

![image](https://github.com/user-attachments/assets/28d00729-648e-4eb2-8645-96190acb3773)

Nos encontramos con 3 puertos abiertos 21 - ftp , 22 - ssh , 80 - hhtp

![image](https://github.com/user-attachments/assets/b3a7eadb-6820-457c-acfd-2167a8b795aa)

Dentro de la web nos encontramos que nos explican un poco como funciona todo el equipo "STAR alpha team" estan en una operacion buscando al "STARS bravo team" en el nor este de "Racoon City" fue atacado por un perro zombie.

El equipo decide correr cerca de la mansion y la noche comienza.

Dentro de la mansion, Jill intenta abrir una puerta pero le paran, se escucha una escopeta cerca de la puerta. Weaker ordena que investigue la escopera donde esta la sala?

Esta es fácilita, simplemente abrimos el developer y nos los dice 

![image](https://github.com/user-attachments/assets/df300176-b323-4c32-b2bc-6c50369f8480)

/diningRoom/

![image](https://github.com/user-attachments/assets/9fa2e57e-0ffe-4a7a-906c-4a12db409739)

Después de encontrar esta habitación, empezamos a investigar. Encontramos sangre cerca de un extintor. Después de una pequeña investigación no encontramos nada importante. Igual otra habitación?

Tenemos el primer emblem flag: 

![image](https://github.com/user-attachments/assets/dc1a7d5a-9839-4e32-9972-b27f22dc3428)

Nos dice una pista y es podemos poner algo en el "emblem shot" refresa /diningRoom/

Si nos volvemos a ir a developer encontramos un hash

![image](https://github.com/user-attachments/assets/99222af4-732a-4a60-bd27-35dcfb5b1a43)

Si lo llevamos al "CyberChef" nos dice otra habitación

![image](https://github.com/user-attachments/assets/7d2e8c2c-f78e-4cf3-bcc0-baf15f531ad2)

Probemos a ver:

![image](https://github.com/user-attachments/assets/e06c8905-3bc1-4d96-b4a6-92437fee36b5)

Nos encontramos con un zombie, se acerca a nosotros pero Jill le pega 6 tiros, En adición el cuerpo se cae a lsuelo, despues de investigarlo era un antiguo perteneciente del equipo bravo, nos encontramos con una llave y podemos ir a la siguiente rom /artRoom/

tenemos la flag 

![image](https://github.com/user-attachments/assets/d352656d-c389-4ab7-825e-6a10b57d1c5a)

Vemos que un numero esta pintado y una escultura dentro de la habitación, hay un papel lo investigamos

Guay nos da un mapa de las habitaciones:

Location:
/diningRoom/
/teaRoom/
/artRoom/
/barRoom/
/diningRoom2F/
/tigerStatusRoom/
/galleryRoom/
/studyRoom/
/armorRoom/
/attic/

Vayamos viendo las que no tenemos investigadas a ver que encontramos

Nos vamos al bar como no:

![image](https://github.com/user-attachments/assets/a4850cb8-13f9-40a8-8c25-0eaf52d8bfca)

Nos encontramos que la puerta esta abierta y tiene que abrirse con la llave (cosa que tenemos) vamos a abrirla

![image](https://github.com/user-attachments/assets/994299b2-0c89-41f6-b385-fde715aa46eb)

Dentro de la puerta nos encontramos con una mesa de bar y un piano que nos pide flag (cosa que no tenemos) pero encontramos una nota que pone "moonlight somata" vamos a leerla

Parece ser que nos han vuelto a encriptar

![image](https://github.com/user-attachments/assets/ef4a5d2b-7442-4847-8a91-698077c661f0)

Cual sacamos la partitura

![image](https://github.com/user-attachments/assets/ae8f7dc1-6a26-4a3c-acde-ac6d92cd77d0)

Vamos a tocar el piano!

Encontramos una entrada secreta al bar con un emblema de oro en la pared

![image](https://github.com/user-attachments/assets/9922648a-1430-4390-9639-ba2a4c75b40c)

Sacamos flag del emblema de oro

![image](https://github.com/user-attachments/assets/9454512d-3815-44ac-8478-f4e5a0d692b0)

Nos dice que podemos poner algo en el slot del emblema que sera?

Si refrescamos la pagina nos deja poner una flag cosa que es la primera que hemos encontrado

![image](https://github.com/user-attachments/assets/d805deab-c04c-4559-babc-49e9d1099a21)

Nos da un nombre "rebecca"

Vamos a seguir investigando otras habitaciones

En el diningRoom2f vemos que jill no encuentra gran cosa, solo una gema azul pero nada mas

![image](https://github.com/user-attachments/assets/ff8d9b59-746e-4bb9-bd6f-1d21cee37623)

Si inspeccionamos la página veremos algo interesante

![image](https://github.com/user-attachments/assets/b7fc656a-2319-46f3-8f65-0d42d9203121)

Genial lo desciframos por el metodo cesar

You get the blue gem by pushing the status to the lower floor. The gem is on the diningRoom first floor. Visit sapphire.html Suiqh

GG tenemos la gema azul

![image](https://github.com/user-attachments/assets/8d99795e-c9fd-4887-8ee6-6e0f94d29d07)

Vamos a seguir investigando otras habitaciones

![image](https://github.com/user-attachments/assets/bec3e761-2fc2-401b-9a5f-ac19f15fcbfe)

Vemos que nos pide la flag de la gema azul vamos a ver que pasa

![image](https://github.com/user-attachments/assets/7dc57ce7-a249-40ee-81e2-2c7dc15cf800)

Nos da otro cifrado pero nos da pista, ha sido una vez codificado, contiene 14 letras y necesitamos recoletar los 4 crest combinarlos y codificarlos 1 + 2 + 4 + 4 genial pues tenemos el primero:

"S0pXRkVVS0pKQkxIVVdTWUpFM0VTUlk9"

Nos vamos a la galeria

![image](https://github.com/user-attachments/assets/da0191ab-1d9d-4fcc-885f-43d68175f73c)

Vemos una nota vamos a explorarla

Genial nos da la parte dos de la codificación

"GVFWK5KHK5WTGTCILE4DKY3DNN4GQQRTM5AVCTKE"

Va cifrado 2 veces  y contiene 18 letras 

Vamos a otra habitación

Que yo sepa ahora mismo no tenemos la flag de aquí

![image](https://github.com/user-attachments/assets/e4a72e84-7517-4861-808e-65a4a1dbeeee)

Vemos que en el atico y en los otros 3 nos pide lo mismo, con lo cual tenemos que encontrar dicha flag.

Una cosa que nos hemos pasado es volver a la /diningRoom/ y poner la flag de emblema de oro y nos encontramos con esto

![image](https://github.com/user-attachments/assets/ea0ac30f-8847-460f-b007-543baf3b1278)

Después de estar un buen rato buscando nos damos cuenta que no es un cifrado cesar si no un "cifrado Vigenere" tenemos otra flag

![image](https://github.com/user-attachments/assets/6fb07998-77c9-42a3-be9b-f7d2ed4ebe86)

![image](https://github.com/user-attachments/assets/5851fd95-6f6f-43c6-bfaa-aa95bfccdc79)

Genial vamos a probar en las puertas que antes no podiamos abrir

En el estudio nos dice que necesita un simbolo de armadura con lo cual no creo que funcione

Pero en la habitación de "armor Room" si que nos deja poner el simbolo del escudo

Estamos dentro: 

![image](https://github.com/user-attachments/assets/db9e8a80-d571-4110-8561-105bed9350d6)

Vemos 8 armaduras en la izquierda y derecha y encontramos una nota 

el crest 3:

"MDAxMTAxMTAgMDAxMTAwMTEgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAwMTEgMDAxMDAwMDAgMDAxMTAxMDAgMDExMDAxMDAgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAxMTAgMDAxMDAwMDAgMDAxMTAxMDAgMDAxMTEwMDEgMDAxMDAwMDAgMDAxMTAxMDAgMDAxMTEwMDAgMDAxMDAwMDAgMDAxMTAxMTAgMDExMDAwMTEgMDAxMDAwMDAgMDAxMTAxMTEgMDAxMTAxMTAgMDAxMDAwMDAgMDAxMTAxMTAgMDAxMTAxMDAgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTAxMTAgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTEwMDEgMDAxMDAwMDAgMDAxMTAxMTAgMDExMDAwMDEgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTEwMDEgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTAxMTEgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAxMDEgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAwMDAgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTEwMDAgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAwMTAgMDAxMDAwMDAgMDAxMTAxMTAgMDAxMTEwMDA="

Va encriptado 3 veces y contiene 19 letras

Vamos que nos falta solo 1 !

En el atico también nos dice que utilicemos el simbolo del escudo

Estamos dentro, que nos ataca una serpiente gigante le dispara 10 veces antes de que se vaya, encontramos otro cuerpo "Richard" del equipo brazo y dentro del bolsillo tiene una nota

No da la ultima crest

crest 4:

gSUERauVpvKzRpyPpuYz66JDmRTbJubaoArM6CAQsnVwte6zF9J4GGYyun3k5qM9ma4s

Codificada dos veces. y contiene 17 caracteres

## DESCIFRAR LAS 4 CREST

### CREST 1

S0pXRkVVS0pKQkxIVVdTWUpFM0VTUlk9

- Codificado 1 vez
- Cotiene 14 letras

Con "CyberChef" sacamos la primera parte de la crest

Solución: RlRQIHVzZXI6IG

### CREST 2

GVFWK5KHK5WTGTCILE4DKY3DNN4GQQRTM5AVCTKE

- Cifrado 2 veces
- Cotiene 18 letras

Después de muchisimo lo hemos sacado

![image](https://github.com/user-attachments/assets/c364f239-ae95-4ecd-9381-1d2affe3f95b)

h1bnRlciwgRlRQIHBh

### CREST 3

MDAxMTAxMTAgMDAxMTAwMTEgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAwMTEgMDAxMDAwMDAgMDAxMTAxMDAgMDExMDAxMDAgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAxMTAgMDAxMDAwMDAgMDAxMTAxMDAgMDAxMTEwMDEgMDAxMDAwMDAgMDAxMTAxMDAgMDAxMTEwMDAgMDAxMDAwMDAgMDAxMTAxMTAgMDExMDAwMTEgMDAxMDAwMDAgMDAxMTAxMTEgMDAxMTAxMTAgMDAxMDAwMDAgMDAxMTAxMTAgMDAxMTAxMDAgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTAxMTAgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTEwMDEgMDAxMDAwMDAgMDAxMTAxMTAgMDExMDAwMDEgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTEwMDEgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTAxMTEgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAxMDEgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAwMDAgMDAxMDAwMDAgMDAxMTAxMDEgMDAxMTEwMDAgMDAxMDAwMDAgMDAxMTAwMTEgMDAxMTAwMTAgMDAxMDAwMDAgMDAxMTAxMTAgMDAxMTEwMDA=

- 3 veces cifrado
- contiene 19 letras

Este ha sido bastante simple

![image](https://github.com/user-attachments/assets/957db785-49fb-4b3e-a1d4-c51bb88ef525)

c3M6IHlvdV9jYW50X2h

### CREST 4 

gSUERauVpvKzRpyPpuYz66JDmRTbJubaoArM6CAQsnVwte6zF9J4GGYyun3k5qM9ma4s

- Va cifrado 2 veces
- contiene 17 caracteres

![image](https://github.com/user-attachments/assets/059375ff-c811-4bd8-9a37-9babed5d3d1d)

pZGVfZm9yZXZlcg==

Ahora que tenemos todos vamos a sacar el final

# MANSION FINAL

Juntamos todos y haber que sacamos

RlRQIHVzZXI6IGh1bnRlciwgRlRQIHBhc3M6IHlvdV9jYW50X2hpZGVfZm9yZXZlcg==

Sacamos : FTP user: hunter, FTP pass: you_cant_hide_forever 

Seguimos

# THE GUARD HOUSE

Después de conseguir el acceso del FTP vamos a ver que encontramos

```
ftp <IP>
```

![image](https://github.com/user-attachments/assets/febbcb17-3168-401d-825d-41b7dd3791c8)

Vamos a leer y descargarnos imagenes porque seguramente necesitemos el exitfool o alguna herramienta de estas

![image](https://github.com/user-attachments/assets/78fccbb6-cb1c-4f58-b46b-1825f052c72c)

Y como vemos para ser una imagen ocupan mucho

![image](https://github.com/user-attachments/assets/bef75d88-4bfb-4327-a067-be6ac5c0d108)

Nos dice que la llave esta dentro del fichero de texto, pero necesitamos desencriptar y que vayamos al directorio /hidden_closet/ pero esta cerrada

![image](https://github.com/user-attachments/assets/df9729d8-380e-47bd-9880-8b56c3f696ec)



