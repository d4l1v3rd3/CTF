# Objetivos de aprendizaje

- Auto firmarse certificaciones
- Ataques man in the middle
- Usar Burp Suite para interceptar tráfico

# Certificados

- Clave Publica: Es el core, un certificado que contiene la clave publica, parte de las claves criptograficas y claves publicas y privadas. Las claves publicas estan disponibles para todo e lmundo y usadas para encriptar datos.
- Clave Privada: La clave privada tiene el secreto y usado en la web para encriptar los datos del servidor
- Metadatos: Alrededor de las claves, se incluyen metadatos dando información adicional sobre el certificado del web y la certificación. Normalmente buscamos información sobre la Autoridad certificadora. cA

# Firma Aquí, Confía en mi

Que es una CA?

Es una entidad en la que nos fiamos, por ejemplo GlobalSign, Policia Nacional.

- Handshake: Tu navegador consulta a una conexión segura, y la web responde mandando el certificado, en este caso solo requerimos de la clave publica y los metadatos.
- Verificacion: Tu navegador checkea si el certificado es valido y si puedes checekar si la CA es valida. Si la certificacion no esta expirada o es buena, pasa y el navegador dice que si
- Key Exchange: EL navegador usa la llave publica para encriptar la sesion, todas las comunicacion son encriptadas desde el lado usuario y servidor
- Decryptation: El sevidor usa la llave privada para desencriptar la sesion,.

## Certificados autofirmados vs Certificados con CA

