#by d4l1

<p align="center"><img src="https://github.com/user-attachments/assets/2e74501b-e6df-4d0b-89e3-1f6bd4194b76"></p>
<h1 align="center">BUILDER</h1>

# ÍNDICE

- [INICIO]
- [ENUMERACION]
- 

# INICIO

Nos encontramos con la máquina Builder, una máquina de dificultad media, en la que encontrarmemos una vulnerabilidad con el CVE-2024-23897 sobre desautentificación de usuarios y leeremos archivos arbitrariosdel sistema para tomar el control. Deberemos xtraer el usuario y contraseña del usuario "Jennifer". Usar esas crendeciales, coger una SSH key y obtener acceso root al sistema

## HABILIDADES REQUERIDAS

- Enumeracion
- Docker

## HABILIDADES QUE APRENDEREMOS

- Explotar CVE-2024-23897
- Estructura de directorio Jenkins
- Criptografia Jenkins

# ENUMERACION

Como siempre haremos un test de conectividad:

![image](https://github.com/user-attachments/assets/904ac6e8-847a-402a-8145-2276c2de6db4)

ttl = 63 (Linux)

Posteriormente escaneo de puertos:

![image](https://github.com/user-attachments/assets/b7f7816e-2c67-4d7c-9ea0-03690942f7c1)

Nos encontramos con:

- Puerto 22 abierto (SSH) Ubuntu
- Puerto 8080 abierto (HTTP) Jetty 10.0.18

![image](https://github.com/user-attachments/assets/5ff9d0bf-a66e-4c5f-91fd-0f04756b071d)

Nos encontramos con una página web con Jenkins 2.441 vamos a explorar.

Vamos a buscar una vulnerabilidad de "Jenkins 2.441"

Nos encontramos con : [CVE-2024-23897-Jenkins-Arbitrary-Read-File-Vulnerability](https://github.com/vulhub/vulhub/tree/master/jenkins/CVE-2024-23897?source=post_page-----143ad7fde347--------------------------------)

Nos explican un poco sobre Jenkins, es un server automatico de código abierto. Ayuda a automatizar partes del software para los desarolladores haciendo testing, construición, implementaciones, etc.

Esta vulnerabilidad nos deja leer archivos del sistema

```
python3 script.py -u http://10.10.11.10:8080/ -f /etc/passwd

```
# INTRODUCCIÓN AL SISTEMA

Una vez que confirmamos que el exploit funciona, vamos a enumerar los elementos de la instalación de Jenkins en la ruta "/proc/self/environ"
```
HOSTNAME=0f52c222a4cc<SNIP>HOME=/var/jenkins_home<SNIP>
```
Leyendo estas variables, encontramos que el directorio home esta en "/var/jenkins_home"

![image](https://github.com/user-attachments/assets/524d632a-4c1e-48bf-af25-593fdbf63169)

Tenemos la user.txt

Si nos damos cuenta 



