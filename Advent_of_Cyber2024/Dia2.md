# Dia 2

# Introducción

Es el momento mas chulo del año, pero tambien es un momento extresante para los SOC team, no es el momento de despistarse y generar nuevas alertas. Queremos dejar la red totalmente segura

Sin embargo los analistas de SOC estan quemados antes de navidad, muchos casos pendientes y alertas similares se repiten con falsos positivos

Vamos a ver si podemos ayudar al SOC team para analizar y determinar que rumores son verdad

## Verdad o falsos positivos

Los eventos de SOC vienen con diferentes dispositivos SIEM, con un codigo donde toda la información, dependiendo de las reglas se define e identifica actividad maliciosa. Si un trigger salta y alerta el analista debe identificar la alerta y decir si es true o falso. 

## Tomar una decision

Mientras no haya diferencia entre los falsos o verdad es crucial elegir lo cierto  y en caso no supere a un ataque

## Utilizar el Superpoder del SOC

# Inicio 

Una vez que tengamos la máquina activa nos conectaremos a la URL y nos loguearemos

Una vez logueados nos iremos al menu de la izquierda y pulsaremos sobre "discover"

![image](https://github.com/user-attachments/assets/47ce6614-5cd2-449e-ab6d-8f71654cf89d)

Según lo que nos dice la room la actividad ocurrio el 1 de diciembre 2024 entre las 0900 y 0930 osea que ya sabeis a poner esa fecha

![image](https://github.com/user-attachments/assets/1e76e832-6484-41cb-9c17-d297be3daa47)

No son fáciles de leer vamos a añadir el panel de columnas que sera importante

Como vemos son procesos de poweshell

![image](https://github.com/user-attachments/assets/a300ec22-030a-4fe3-ab59-71da6d944494)

Como vemos la actividad que observamos en la máquina, es muy diferente entre el login a los comandos muy rpecisos. Estas practicas es muy sospechoso y si ya ponemos la IP es raro de cojones

Hay un tiempo de diferencia entre cada uno

Tenemos el parametro source.ip para ver la IP

![image](https://github.com/user-attachments/assets/3d41e38a-e2d3-4647-a300-2b1d7c3fc1e6)

Como vemos esta ip esta relacionada a los eventos de autenticación, nosotros podemos filtrar a ver si hay alguna correlación, podemos quitar la categoria de evento y filtrar por el valor solo de autentificación, 

![image](https://github.com/user-attachments/assets/d88915a8-bd95-466f-84fc-39f85e0d7f86)

Como resultado vemos todos los ouputs de los eventos de autenticación. Ahora debemos expandir todo para entender el contexto del usuario y porque ha echo esto. y bajar al dia 29 de noviembre hasta el 1 de diciembre

Para que no haya tantos 

