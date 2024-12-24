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

