# Objetivos de aprendizaje

- Entender la estructura de un archivo binario
- La difernecia entre desambleado y decompilación
- Familiarizarse sobre binarios multi-stage
- Practicas binario reverso

# Introducción a la Ingenieria Reversa

Es el proceso para de romper algo para entender como funciona. En ciber seguridad es usar o analizar como las aplicaciones o binarios funcionan. Esto se puede determinar si una aplicación es maliciosa o no.

Por ejemplo

![image](https://github.com/user-attachments/assets/00010885-58ab-46c0-b57a-62aa6f9fa098)

Los actores maliciosos distribuyen aplicaciones maliciosan a los atacantes para entender atributos e indicadores de los binarios con los atacantes para ganar defensa de ellos. El mas famoso es el ransomware WannaCry. La aplicacion no corria si un dominio estaba registrado o disponible

Marcus rgistro el dominio, y paro el ataque de WannaCry entero. Esto es de los casos mas famosos de ingeniera reversa usada para defensa

# Binarios

En ordenadores, binarios y ficheros compilados de codigo fuente. Por ejemplo, tu ejecutaste un binario cuando lanzaste un archivo ejecutable en el rodenador. Esta aplicacion se programa en C# por ejemplo y se compila y esa compilacion se traduce para que el ordenador entienda las instrucciones

Especifican la estructura de como el sistema operativo tiene que ejectuarse.

- Una sección de codigo
- Una sección de datos
- Tables importadas y exportadas

# Desambleado vs Decompilado

Cuando hacemos ingeniera reversa, tenemos dos técnicas principales. La primera es desamblear y decompilar

Desamblear es vewer el bajo nivel que la máquina va aejecutar el binario. Porque el output se traduce a instrucciones de la máquina y podemos ver como e lbinario interactura con el sistema en cada caso como Ghidra o tros

![image](https://github.com/user-attachments/assets/4a49abf3-a5c6-4789-b745-8618cb1613ee)

Decompilar, sin embargo, convierte el binario en alto codigo, como C++ o C# haciendo mucho más fácil de leer. Sin embargo, estas traducciones se pierde información o nombres de variables. Este metodo es util pero si quieres entender la aplicación

![image](https://github.com/user-attachments/assets/4aa3c603-0bc8-491c-8ee1-cc515e014607)

# Multi-Stage Binarios

Estos ataques usabn multiples binarios en diferentes acciones en un ataque

1- Paso 1: Dropper: El binario normalmente tiene unas acciones que enumerar el sistema operativo y comrpueban si el payload funciona. Una vez todas las codiciones han sido verificadas, el binario descragar otro código malicioso que ataca
2- Paso 2: Payload: EL binario es la carne y los huevos del ataque, por ejemplo es lo que encripta y filtra los datos de un ransomware

![image](https://github.com/user-attachments/assets/dac4d04c-ce78-4f02-9b02-fd1402391799)

# Jingle .NET

Por hoy vamos a usar el decompilador ILSpy y haremos un walthrough de igeniera reversa del nombre demo.exe

antes de analizar deberemos identificar el binario original, modificarlo y ver como es en la practica

![image](https://github.com/user-attachments/assets/31f8a437-8502-483b-b404-fc43c8f177cc)

Abrimos PeStudio y abrimos el archivo demo.exe

![image](https://github.com/user-attachments/assets/23698fd5-8743-43f2-9726-d1bff68d9eea)

Como vemos nos da información relevante, como el hash por ejemplo en Sha-256 cada cosa que cambiemos cambiara esto

Luego las secciones representas el espacio en memoria con un contenido difernete a un ejecutable de Windows. Podemos calcultar el hash que identifica las secciones. Vamos a centrarnos en dos hsahes, uno en .text

![image](https://github.com/user-attachments/assets/33c366a1-eb8b-4836-8c7b-bd0e71af9c3e)

y el otro en indicators

![image](https://github.com/user-attachments/assets/6021f87f-6828-451d-bd5b-6fd6878bc490)

Ahora que tenemos información sobre el archivo vamos a investigar. Vamos a intentar entender el ejecutable y lo que hace. Vamos a intentar entender el flow. SI intentamos leer con el archivo abierto, no podemos ver el formato binario 

Utilizaremos ILSpy para la decompilación esta herramienta decompila y nos dara información

![image](https://github.com/user-attachments/assets/6a23c795-ef47-4cf0-bc2c-27adf17a2c4a)

Como podemos ver el codigo 

Nos da un Hello THM luego un sleep de 5 segundos

Asigna un valor con dos variales addres y text accediendo a un archivio png luego lo mete al desktop de 

Cuando intenta conectarse a la URL la vairalbes adress y cuarda el contenido del archivo en el desktop usando el webcleint, luego el ejecutable descargarga una ruta asignada al variable texto y empieza el metodo

Finalmente printea el mensae bye bye y espera otros 5 segundos antes de cerrarse

![image](https://github.com/user-attachments/assets/163874fa-5ad6-4892-bcc0-66fea3e40178)

Después de ejectuar el archivo observamos que hace exacatamente eso. Para resolver las preguntas lo haremos con WarevilleApp.exe






