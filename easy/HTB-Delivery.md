#by d4l1

<p align="center"><img src="https://github.com/user-attachments/assets/f9990bea-bf1f-4946-adfe-15d92d104bd7"></p>
<h1 align="center">Delivery</h1>

# ÍNDICE

# INICIO

Hoy nos enfrentamos a la máquina "Delivery" vamos a hacer una enumeración de información

- Test de conectividad:

  ![image](https://github.com/user-attachments/assets/a18e0202-b5a5-45f8-8835-a1630e185ada)

- Escaner de puertos:

 ![image](https://github.com/user-attachments/assets/9414c415-c8e5-41d3-9ea8-504601a31926)
 
 Aquí solo encontramos 2 puertos TCP 22 (ssh) y el 80 (http)
 
 ![image](https://github.com/user-attachments/assets/78e659db-43ef-470e-b199-264895b3fa68)
 
Nos falta por aquí el puerto (8065) que no sabemos nada de el 
 
- Sistema Operativo:

  ![image](https://github.com/user-attachments/assets/3a957d2c-25da-485e-a591-bddda8c0593e)

Linux

## ENUMERACIÓN

Empezamos enumerando los servicios y a ver si podemos hacer algo con ellos.

Con un escaner más fuerte al puerto que no sabiamos anda nos encontramos un dominio (cdn.rudderlabs.com) en la que tenemos una página web. 

![image](https://github.com/user-attachments/assets/5aec8b4f-fa65-45c4-8ea4-b389046c7f99)

Encontramos en ese puerto un /login pero en el puero 80 encontramos una página normal

![image](https://github.com/user-attachments/assets/d7d05ca8-2e60-434b-b12f-54664223fcee)

Después de ver por la página no encontramos nada importante, lo que haremos ahora será hacer un escaner de subdirectorios dentro del dominio @delivery.htb

Probemos con ffuf


