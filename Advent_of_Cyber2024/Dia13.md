# Objetivos de aprendizaje

- Aprender sobre WebSockets y las vulnerabilidades
- Aprender como manipular mensajes de WebSocket

# Introducción a WebSocket

Da al navegador y al servidor una constante linea de ocmunicación. COmo en la escuela cuando preguntabas a alguiente, el te daba una respuesta y tenías que levantar las manos, es como una linea de movil que solo funciona cuando lo necesitas.

Sirve para chats, juegos en tiempo real, datos en vivo o actualizaciones

# Consultas HTTP tradicionales vs WebSocket

Cuando una consulta HTTP, el navegador manda una consulta al sevidor y el servidor responde, entonces la conexión se cierra. Necesitamos dichos datgos para mandar la consulta.

Cogemos una aplicación de chats, tu navegador te pregunta ningún mensaje nuevo? despues de segunos. Este metodo, no es eficiente. El navegador y el servidor acaban de trabjar inecesariamente.

WebSocket es diferente. Una vez la conexión se establece, se abre, el servidor mete una update cuando llega algo nuevo. Es como dejar la puerta abierta y dejar cerrar


# Vulnerabilidades WebSocket

Mientras el coste de performace, teenmos problemas de seguridad necesidad de monitorizar. Mientras La conexion esta estable y activa, podemos coger vulnerabilidades

- Mala autentificacion y autorizacion
- Manipulación de mensajes: EN bajo flow de datos los atacantes pueden interceptar y cambiar los mensajes si no hay encriptación
- Cross-Site WebSOcket Hijacking
- Dos

# Que es el Websocket message manipulation?

Cuando un atacante intercepta y cambia los mensajes entre la aplicacion web y el servidor. 

No es como una consulta HTTP regular, WebSOcket deja la conexión abierta, habiendo una conexión constante.

En este tipo de ataques, un hacket interceta y retuerce estos mensajes que se estan enviando. 

Este tipo de manipulacion puede llegar a dejar insertar comandos maliciosos

Este tip ode ataque sson muy peligrosos si no hay una protección, como Encriptación, con AES o RSA 

# Explotación

Vamos a abrir Burp para coger las consultas, configuramos para interceptar consultas a la hora de clickar mensajes, con lo cual trackearemos los vehiculos

![image](https://github.com/user-attachments/assets/d517b421-d5ee-4a7e-8308-f7ccdd03695a)







