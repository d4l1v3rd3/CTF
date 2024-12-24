# Objetivos de aprendizaje

- Entender el concepto de vulnerabilidad en condición de carrera
- Identificar los gaps e introducción a HTTP2
- Explotar condiciones de carreta en entornos controlados
- Aprender como se arregla una carrera

# Tiempo de Web y Condiciones de carrerra

Las aplicaciones web convencionales normalmente son faciles de entender, identificar y explotar. Si hay algun error en el codigo de la aplicacion web, podemos forzar a ala aplicacción a hacer acciones que no estaban especificadas. Esto es muy fácil de entender porque normalmente estamos relacionados con ello.

Si ponemos un mal output no mandaran datos, indicando una vulnerabilidad. Pero que pasa si encunetras vulnerabilidades con buenos datos? O que ahy datos pero no puedes enviarlos? Aqui es donde entra el tiempo de web y la condicion de carrera.

Es una forma simple, un "web timing" nos da información de la aplicación web diciendo cuanto tarda el proceso de nuestra consulta. 

Este tipo de vulnerabilidades normalmente son subceptibles. la diferencia de respuesta de 1300ms a 5ns haciendo ataques por paso. Porque es algo sutilmente natural, pero es bastante dificil de detectar, necesitando tecnicas de rango. Sin embargo, con la adopción de HTTP/2 es mas fácil encontrarlo y explotarlo

# El ascenso de HTTP/2 

HTTP/2 fue creado y actualizado por la actualización HTTP, el protocolo usa aplicaciones web. Mientras la mayoria de aplicaciones siguen usando HTTP/1.1 pero se eestan incrementando el HTTP/2 siendo más rápido, mejor para la web y quitando limitaciones del anteiror. Pero si se implementa mal puede dar a vectores de explotación.

La diferencia es la llave en un ataque por tiempo de web soporta lo llamado paquetes simples o multi consultas. Latencia de red, y la coantidad que tarda en consultar o haciendo dificil identificar estos fallos de web. 
