# HackPark

Nos encontramos con una máquina que en su descripción pone:

Fuerza bruta de logins en web con hydra, identificar y usar exploit publicos para escalar privilegios en una máquina Windows!

# Introducción

Ejecuta la máquina y accede al servidor web.

![image](https://github.com/user-attachments/assets/7146f828-eb02-4854-8ed6-4da39522496f)

En la web nos encontramos con una imagen de un payaso, en la cuál la podemos descargar o hacer una "reverse search" 

Haciendo la reverse search (yo he utilizado esta página https://tineye.com)

Nos damos cuenta que es Pennywise!!

## Hydra

Ahora necesitaremos encontrar la pagina de logeo y identificar la consulta que hacemos al servidor web. Normalmente las consultas tienen don tipos, GET Y POST.

Podemos ver las consultar haciendo click por ejemplo en el formulario, inspeccionando el eleento y leer los valores. Pudiendo identificar con BurpSuite si se puede llegar a interceptar tráfico.

¿Que tipo de consulta utiliza windows para enviar la consulta? POST

Ahora que sabemos el tipo de consulta y la URL, podemos hacer un ataque de fuerza bruta

