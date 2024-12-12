En esta room aprenderemos como el equipo de SOC encuentra lo que esta pasando y como el Glitch ha conseguido acceso a la web

# Objetivos de aprendizaje

- Aprender sobre analisis de log con herramientas como "ELK"
- Aprendes sobre KQL y como se usa para investigar usando "ELK"
- Aprender sobre RCE, y como se hace via subida de archivos

# Analisis de Log y Introducción a ELK

El analisis de log es crucial para los equipos de blue team.

Los analisis de log pueden ser abrumadores, especialmente si hay multiples dispositivos y servicios. ELK o ElasticSearch, Logstash y Kibana, combina el analisis de datos y procesa herramientas para hacer el log mucho mas manejable. 

# Usar ELK

Abriremos la URL dispuesta http://ip:5601/ 

Nos iremos arriba a la izquierda - Discover

![image](https://github.com/user-attachments/assets/7363c472-9424-49ba-af78-9dba13469025)

Deberemos selccionar la colección que queremos utilizar. Esta collección es el grupo de logs. Deberemos recoger "wareville-rails" colecction. Para seleccionarla nos iremos arriba a la izquierda

![image](https://github.com/user-attachments/assets/1746755e-1983-4c40-b0f8-2405d7ae8793)

Una vez hecho esto, veremos que la pantalla se nos agranda pero nos sale "No results match you search criteria" esto es porque los logs solo estan seleccionados como los ultimos 15 minutos.

Cambiaremos los datos, y clickaremos sobre "absolute" para cambiar la fecha elegiremos

```
October 1 2024 00:00:00 hasta October 1 23:30:00
```

![image](https://github.com/user-attachments/assets/6afc8036-f346-470d-a61c-672513075eb4)

Ahora veremos todas las entries

![image](https://github.com/user-attachments/assets/52421a29-c12a-4aba-bc26-d755a2ffb2a1)

# Kibana Query Language (KQL)

Es muy simple de usar por ejemplo 

```
ip.address: "10.10.10.10"
```

![image](https://github.com/user-attachments/assets/0b45730b-2154-4430-b66d-728fd3d5f1ae)

# Investigar el ataque a la web con ELK

Primero de todo filtraremos solo por las IP "10.13.27.115"

![image](https://github.com/user-attachments/assets/5ff24bdf-d6b8-4c2b-9ade-462f2f09afe9)

Y también quitaremos las respuestas 404 que son las que no han llegado a dicho recurso

![image](https://github.com/user-attachments/assets/a21f88c9-d709-43d5-977f-c756a2fd8ced)

En esta investigación, veremos la actividad de la IP "10.9.98.230" clickamos en "clientip" y la seleccionamos

Si queremos ver alguna especficación en particular simplementea la abrimos

Encontramos buscando en diferentes IP un "shell.php" si en el filtrados ponemos tal que "message. "shell.php"" nos saldran

![image](https://github.com/user-attachments/assets/1cd9fe9f-0974-41a9-bd25-f1bf65027e2c)

# Operacion Roja

En esta sección veremos la parte del red team. 

## Porque las websites te dejan subir archivos

La subida de archivos esta en todas las web, or una buena razon. Subida de imagenes, noticias, documentos, cuentas, etc. 

## Vulnerabilidades de subida de archivos

- RCE
- XSS

## Porque no poner restricciones es peligroso

Bueno simplemente por lo que vamos a ver ahora jaja

# Practica

Una vez tenemos todo entendido vamos a por ello primero añadiremos a nuestro DNS el dominio en cuestion

![image](https://github.com/user-attachments/assets/722df8c0-0058-4aa7-b0dc-9e6255de49d2)

Elegimos "frostpines-resorts" entre las 11:30 y 12:00 del 3 de octubre de 2024

Así encontraremos todo

# Preguntas

Donde se ha subido la sehll?

/media/images/rooms/shell.php

Cual es la Ip utilizada para la shell

10.11.83.34

Cual es el contenido de la flag

THM{Gl1tch_Was_H3r3}

GG !!



