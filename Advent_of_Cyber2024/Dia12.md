# Objetivos de aprendizaje

- Entender el concepto de vulnerabilidad en condición de carrera
- Identificar los gaps e introducción a HTTP2
- Explotar condiciones de carreta en entornos controlados
- Aprender como se arregla una carrera

# Tiempo de Web y Condiciones de carrerra

Las aplicaciones web convencionales normalmente son faciles de entender, identificar y explotar. Si hay algun error en el codigo de la aplicacion web, podemos forzar a ala aplicacción a hacer acciones que no estaban especificadas. Esto es muy fácil de entender porque normalmente estamos relacionados con ello.

Si ponemos un mal output no mandaran datos, indicando una vulnerabilidad. Pero que pasa si encunetras vulnerabilidades con buenos datos? O que ahy datos pero no puedes enviarlos? Aqui es donde entra el tiempo de web y la condicion de carrera.

Es una forma simple, un "web timing" nos da información de la aplicación web diciendo cuanto tarda el proceso de nuestra consulta. 
