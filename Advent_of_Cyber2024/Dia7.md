# Monitorizar en un entorno AWS

Care4Wares' es una infraestructura que funciona en cloud, ellos escogieron AWS como proveedor de servicios en la nube (CSP). Una vez ejecutar un trabajo la máquina fisica. Ellos ejecutan instancias virtualizadas en la nube.

Estas instancias en (AWS) llamadas EC2 instancias (Amazon Elastic Compude Cloud). 

Muchos miebmors de SOC no saben usar el analis de log de la nube, y con cambiar el entorno empiezar a cambiar las herramientas y servicios que se necesitas. 

Su tarea esta vez es ayudar a Care4Wares a descubrir qué ha sucedido con los fondos de la organización benéfica; para ello, necesitarán aprender sobre un servicio de AWS llamado CloudWatch.

## CloudWatch

AWD CloudWatch es un monitor y plataforma para observar dando una gran conocimiento dentro del entorno AWS para monitorizar apliaciones multi nivel. CloudWatch da funcionalidades como monitorizar el sistema y metricas de la aplicacion y configuracion de alarmas en caso de esas metricas, vamos a centrarnos especificamente en CloudWatch logs. Ejecutando la aplicacón en un entorno cloud dando diferentes servicios.

- Eventos Log
- Steam Logs
- Groups Logs

## CloudTrail

CloudWatch puede trackear la infraestructura y aplicacion, pero si quieres monitorizar acciones del mismo AWS? Necesitaremos otro servicios llamado AWS CloludTrail. Acciones que puede el rol usuario o servicios AWS o eventos del Cloud

- Siempre activo
- Formato JSON
- Evenetos historicos
- Trails
- Entregable (un solo acceso para varios codigos)

CloudTrail ayuda a capturar acciones. Estas acciones son interacciones con un numero o servicio. Por ejemplo el servicio S3 (Amazon SImple Storage Service) y IAM (Identity and access management) se usan para asegurar accesos al entorno AWS con la creacion de entidad y asigancion de permisos estac acciones el mismo servicio las graba. 

# Intro to JQ

## Que es JQ

JSON-Formatted. Cuando investigamos largos volumenes, la en "machine-readable" formato extrae y expecialmente lo hace para analisis de log. 

## Como se usa?

Ahora vamos a ver como usamos JQ para transformar datos JSON. eelos guardan las listas en formato JSON

```
[

{ "book_title": "Wares Wally", "genre": "children", "page_count": 20 },

{ "book_title": "Charlottes Web Crawler", "genre": "young_ware", "page_count": 120 },

{ "book_title": "Charlie and the 8 Bit Factory", "genre": "young_ware", "page_count": 108 },

{ "book_title": "The Princess and the Pcap", "genre": "children", "page_count": 48 },

{ "book_title": "The Lion, the Glitch and the Wardrobe", "genre": "young_ware", "page_count": 218 }

]
```

JQ coge dos inputs : El filtro que quieres usar, seguimos el input del fichero. Empezamos a filtrara JQ con un . 
