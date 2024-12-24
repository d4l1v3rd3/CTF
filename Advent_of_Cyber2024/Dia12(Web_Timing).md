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

![image](https://github.com/user-attachments/assets/8dd6db74-fe44-48f9-86a3-1c0540af8429)

# Tiempo de ataques tipicos

Dividido en dos categorías:

- Divulgación de información: Aprovechando la diferencias de los tiempos, un actor maligno puede descubrir información a la que no debería tener acceso. Por ejemplo, utilizada para enumerar los nombres de usuario.
- Condiciones de carrera: Igual que los flujos un actor maligno puede causar acciones malintencionadas, sin embargo el problema es como va a funcionar la aplicacion, haciendo posible condiciones, mandando el mismo cupon por ejemplo mil veces simultaneamente


Cuando el usuario manda su codigo, el codigo actual de la aplicacion lo checkea y si es valido lo usa para despues. Nosotros aplicamos el descuento, Una vez se actualiza y te dice que es usado. Por ejemplo entre el checkeo y la validaciones hay una actualizacion, esos milisegundos donde se aplica el cupon. Es algo muy pequeño pero podrias llegar a mandar una consulta que se cerrara en el momento, antes de actualizar la consulta 1 y la consulta 2, mandando muchisimas consultas de aplicar dicho cupon

# Ganando la carrera

Ahora que entendemos los conecptos básicos de las condiciones de carrera, vamos a explorar esta vulnerabilidad que podria encontrarse en un escenario real. Para esto, vamos a coger el ejemplo de la cuenta de Warville 

# Interceptar las consultas

Antes de empezar con las consultas, vamos a configurar el entorno con el Burp Suite 

# Escaneo de aplicación

Como penetration tester, vamos a identificar las funciones de validaciones que envuelnven las multiples transaciones o operaciones que haces para interactuar con recursos compartidos, o transferencias entre cuentas, leer y escribir la base de datos o actualizar balances.

![image](https://github.com/user-attachments/assets/1c07bbc9-d098-46b6-ad01-d12a885e5c41)

Tenemos dos funcionalidades como vemos "logout" y la siguiente es "transfer"


# Verificas la funcionalidad de transferir

Vamos al navegador y vamos a generar multiples consultas GET y POST si por ejemplo 

![image](https://github.com/user-attachments/assets/0d568f3a-46eb-4533-b5f3-cae15883c1d3)

Vamos a coger la consulta

![image](https://github.com/user-attachments/assets/77a5ae83-176b-4796-9e0a-7f68e344a93d)

Vemos el /transer aceptando la consulta del POST con los parametros

```
account_number y amount
```

Con el repeater podemos mandar multiples consultas. Vamos a duplicar la consulta y lo enviaremos al repeater

Con Ctrl + R aumentaremos las consultas

![image](https://github.com/user-attachments/assets/e548dab6-68ae-4438-adea-4521a2c0c4bf)

Vamosa  crear un grupo para mandar bastantes consultas jeje

![image](https://github.com/user-attachments/assets/fb910902-45c0-4236-be93-587b242f9090)

![image](https://github.com/user-attachments/assets/521f9e1a-ae2b-4747-81c8-f86cdd40788c)

![image](https://github.com/user-attachments/assets/fbd27508-a5d3-4947-a1f5-21572370fbfa)

Elegiremos mandar en paralelo

![image](https://github.com/user-attachments/assets/c39a4493-a245-4e2a-a201-262293d8af0b)

Como vemos estamos en negativo vaya

# Verificar el código

Supongamos que somos penetration testers.

```
 if user['balance'] >= amount:
        conn.execute('UPDATE users SET balance = balance + ? WHERE account_number = ?', 
                     (amount, target_account_number))
        conn.commit()

        conn.execute('UPDATE users SET balance = balance - ? WHERE account_number = ?', 
                     (amount, session['user']))
        conn.commit()
```

En el código si el balance es igual o mayor a la cantidad se actualiza el saldo del destinatario con el comando UPDATE y luego seguido se confirma. Luego s eactualiza el saldo del remitente actualizando el balance y luego confirma nuevamente. Dado que las actualizacione se confirman por separado y no formas parte de una única trasacción. 


# Tiempo por acción

Ahora vamos a entender la vulnerabilidad, asistiendo en validad usando la cuenta del glitch 101:glitch para trasnferir 2000 a la cuenta 111





