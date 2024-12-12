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
