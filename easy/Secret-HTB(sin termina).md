![image](https://github.com/user-attachments/assets/4cf518da-10f6-4338-8c14-e476f61c478e)#by d41l

<p align="center"><img src=""></p>

<h1 align="center">Secret</h1>

# ÍNDICE

# INTRODUCCION

Test De Conectividad

![image](https://github.com/user-attachments/assets/9de539dc-3e69-4b62-b5d8-a50edea200c2)

ttl 63 = Linux

Escaner de puertos

![image](https://github.com/user-attachments/assets/d70a209c-4f2f-4c19-8e8f-0a404b35d703)

- 22 ssh Abierto
- 80 HTTP abierto nginx 1.18.0
- 3000 Node.js http

Nos intentamos conectar por web y necesitamos tender dentro de nuestro dns "editorial.htb"

```
echo "10.10.11.120 editorial.htb" | sudo tee -a /etc/hosts
```
![image](https://github.com/user-attachments/assets/a56ef1b7-8c6a-4f8c-8c9c-b6bf59c5e5c6)

Tenemos la posibilidad de descargar el código de la aplicación 

![image](https://github.com/user-attachments/assets/89e55247-6dab-470f-8aca-8a0c4230d00f)

Si hacemos un "ls -la" encontramos un archivo oculto ".git"

![image](https://github.com/user-attachments/assets/0c722d48-ac0e-41d7-8066-1679cfff3ea2)

Si dentro de el hacemos un "git log" 

![image](https://github.com/user-attachments/assets/d78a0045-e9f7-40f1-8f74-f93dac1ef34f)

Encontramos que en el segundo commit nos dice que removieron ".env" por razones de seguridad. Veamos que es.

![image](https://github.com/user-attachments/assets/f1ad2336-bc13-4743-b834-2e959e09b056)




