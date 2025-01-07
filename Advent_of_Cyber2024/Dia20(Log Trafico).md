# Objetivos de Aprendizaje

- Investigar tráfico de red usando Wireshark
- Identificar indicadores de compromiso capturando tráfico de red
- Entender como funcionan los servidores C2 operan y comunican con sistemas comprometidos

# Cazar

Vamosa a abrir el archivo que tenemos en el escritorio "C2_Traffic_Analysis" automaticamente se nos abrirá en Wireshark

Sospechamos que está máquina esta comprometida. Vamos a listar por ejemplo por la máquina de Marya 

```
ip.src === 10.10.229.217
```

Veremos bastantes paquetes vamos a ir bajando a ver si encontramos paquetes importantes

Por ejemplo un POST

# Mensaje recibido

Si vemos los detalles del paquete y la IP destino 10.10.123.224 podemos ver mas detalles

![image](https://github.com/user-attachments/assets/2bd18ca7-7fbd-4dc0-bd95-7943246d3534)

![image](https://github.com/user-attachments/assets/e64df739-135e-44a1-9e78-137a5d077516)

Si seleccioanmos seguir diho paquete de tráfico

![image](https://github.com/user-attachments/assets/9aa14b07-c68a-4c06-a81b-a95c1a46f67d)

Esto es muy bueno para ver todas las consultas que ha hecho el cliente y servidor.

NO vamos a parar aquí vcamos a per el http GET a ver que pasa

# Práctica

Que mensaje dice Mayor Malware al C2

```
I am in Mayor!
```

Cuál es la IP del servidor C2

```
10.10.123.224
```

Cual fue el comando que mando al servidor C2 de la máquina target

```
whoami
```

Que mensaje secreto dejo encriptado en el c2

```
THM_Secret_101
```

GG

