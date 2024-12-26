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

EL proceso de adquirir un certificado con una CA es largo, deberemos crear un certificado y posteriormente enviarlo a una CA y que te lo firme. Si no tienes herramientas que automaticen esto, este proceso puede tardar semanas. 

- Navegadores normalmente no tienen certificados auto firmados porque no tienen verificacion de terceras partes. El navegador no conoce si el certificado es autentico y tiene malos propositos
- Los certificados de entidades, van de otra mano, si una CA te verifica, confirma la entidad de la web

# Preparacion

Primero de todo añadiremos al dns dicha maquina

```
echo "ip dominio" >> etc/hosts
```

Para verificar si queremos 

```
cat /etc/hosts
```

Vamos a la web

![image](https://github.com/user-attachments/assets/241af33e-8ed9-4135-bef8-72d433750063)

Podemos ver el certificado y aprender más, posteriormente entrar a la web

![image](https://github.com/user-attachments/assets/9d658a75-978f-4369-803a-16b8bf6f8b17)

Si queremos sniffear el tráfico deberemos utilizar el proxy de burp, siendo nosotro sel medio entre townspeope y Gift Scheduler.

Abrimos BurpSuite

![image](https://github.com/user-attachments/assets/3c508e7e-ab57-4280-a4e1-3face5daf3f4)

Configuramos un proxy de escucha apuntando a nuestra IP

![image](https://github.com/user-attachments/assets/2906393e-92e8-408e-94e6-61d9ecd84a35)

Agregamos ahora el siguiente dominio:

```
echo "10.10.103.13 wareville-gw" >> /etc/hosts
```

![image](https://github.com/user-attachments/assets/fb4aeaca-1963-4c65-8446-2e0edb7d8c74)

![image](https://github.com/user-attachments/assets/48f7f6c1-cda7-43cf-a122-79cfbb117f60)

Lo que estamos haciendo es ser nosotros el la puerta de enlace teniendo que pasar primero por nosotros.





