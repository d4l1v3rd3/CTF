<h1 align="center"> Attacktive Directory </h1>

# SETUP

Esta CTF no pide que tenemos que tener la posiblidad de hacer comandos con python
```
python comando
```
Posteriormente cogernos el repositorio de impacket

```
git clone https://github.com/SecureAuthCorp/impacket.git /opt/impacket
```

Después de cloran el repositorio instalar 

```
pip3 install -r /opt/impacket/requirements.txt
cd /opt/impacket/ && python3 ./setup.py install
```

## INSTALAR BLOODHOUND Y NEo4j

Son otras herramientas que se utilizan para atacar AD. Escepecificamente este

```
apt install bloodhound neo4j
apt update && apt upgrade
```

# ENUMERACIÓN

Test de conectividad

![image](https://github.com/user-attachments/assets/dc3bb957-d6f0-413f-866b-936e935531d2)

Escáner de puertos

![image](https://github.com/user-attachments/assets/fd0d79d8-48fe-4eb9-ad88-8611c0a909f0)

Encontramos bastante información relevante y muchos puertos abiertos, nosotros nos centraremos en los puertos 139/445 enumeramemos dichos puertos con 

"enum4linux"

```
enum4linux -a ip
```

Sacamos información relevante.

![image](https://github.com/user-attachments/assets/356b89c9-b25b-45a9-b66a-34687c9beae1)

Sacamos el nombre del dominio : THM-AD

## ENUMERAR USUARIOS CON KERBEROS

Muchos host utilizan otors servicios, como Kerberos, Kerberos es un servicio de autenticación con AD, con el puerto abierto, podemos utilizar "Kerbrute" para descubrir usuarios, contraseñas etc.

Para esta CTF en especial nos dan una lista de usuario y contraseñas y para que nos descarguemos la herramienta vamos a ello.







