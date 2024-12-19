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

Para que no haya tantos eventos en estos tres dias, podemos filtrar por ejemplo el final del dia 1, y filtrar el usuario "service_admin" y la ip "10.0.11.11"

Una vez hecho esto podemos ir filtrando mas cosas, vamos a filtrar solo por "authentication" y que no sea la ip "10.0.11.11"

Después de aplicar dichos filtros podremos encontrar otras cosas chulas

![image](https://github.com/user-attachments/assets/12e4e1d9-d01f-439b-8744-a67c4f86de40)

Una vez aplicados los filtros veremos otra ip

Si vamos abajo veremos un monton de intentos de login fallidos. Parece ser que esta es la IP mala acabada en .255.1 diferente a la que llevamos viendo otros dia. En alnalista debera investigar el script y las credenciales que se han perdido. Sin embargo, primero de todo cambiaremos las credenciales ya enocntraremos el script

Vamos a quitar el "source.ip" y vamos a centrarnos en los eventos de autenticación. 

Vemos que ha intentado un ataque por fuerza bruta

El resultado que vmos es que posteirormente lo ha conseguido y ha ejecutado comandos de PowerShell una vez dentro

Otra cosa importante es que todos los comandos han sido ofuscados o encriptados, sería interesante ver lo que hacian realmente

![image](https://github.com/user-attachments/assets/b9b2d163-dafc-4c3e-8a24-44f723baeb65)

Bueno luego nos cuenta una historia si os interesa pues pa lante

Preguntas:

¿Cual es el nombre de la cuenta de los intentos fallidos?

```
service_admin
```

¿CUantos intentos de logueo ha habido?

```
6791
```

¿Cual es la IP de Glitch?

```
10.0.255.1
```

¿CUando Glitch inicio sesión?

```
Dec 1, 2024 08:54:39.000
```

¿Que comando decodificado utilizo Glith para arreglar los sistemas?

```
Install-WindowsUpdate -AcceptAll -AutoReboot
```


