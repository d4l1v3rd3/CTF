# KENOBI

# INTRODUCCIÓN

En esta máquina nos enfrentaremos a una máquina Linux vulnerable. Enumerando "Samba", manipulando vesiones vulnerables de "Proftpd" y escalando privilegios maninupalndo rutas.

# ENUMERACIÓN

Test conectividad

```
ping -c 3 ip
```

Escaner puertos

```
sudo nmap -sCV -T4 --min-rate 4000 -p- ip
```

![image](https://github.com/user-attachments/assets/84d926b6-8531-46f5-90f0-45e88c26ed16)

![image](https://github.com/user-attachments/assets/81d44512-7d6a-4fc7-b776-6f099e028b19)

![image](https://github.com/user-attachments/assets/9fb22a0b-ba0f-424f-a861-30879e8aaee9)

Como vemos tenemos bastantes puertos abiertos cuales iremos enumerando poco a poco

# ENUMERAR SAMBA

Samba es un estadar de Windows, interopera con linux y Unix. Los usuarios tienen acesso a usar archivos, impresoras y compartir recrusos en internet o intranet. 

Samba esta basada en cliente/servidor por SMB (Server Message block) Desarrollado por Windows, sin samba otras plataformas no podrian comunicarse con otros sistemas operativos.

Formas de enumerar samba:

```
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.73.189
```
![image](https://github.com/user-attachments/assets/aa13d35f-0f51-4327-925d-fb54050530cf)

SMB tiene dos puertos el 445 y el 139

Como vemos hemos encontrado tres acciones en saba "IPC, anonymous print"

Vamos a probar a conectarnos

```
smbclient //10.10.73.189/anonymous
```

![image](https://github.com/user-attachments/assets/11446a94-34c8-4b84-bdff-1e35f2f0cccc)

Podemos recursivamentes i queremos desacargar archivos des amba. Poniendo el usuario y contraseña (en este caso da igual)

```
smbget -R smb://10.10.73.189/anonymous
```

![image](https://github.com/user-attachments/assets/700a2c72-0e0f-4306-85a7-264928ced659)

El archivo tiene información bastante importante, si querrmos podemos leerlo porque hay rutas o demás.

Vamos a enumerar el puerto ftp (21) 

Antes descubrimos el puerto "111" funcionando el servicio "rcpbind" Simplemente es un sevridor que convierte RPC dentro de una dirección universal. Cuando este servicio esta funcionando, dice al rpcbind la dirección en escucha

```
nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.73.189
```

![image](https://github.com/user-attachments/assets/e7493a55-cdde-4f0c-a145-f60679173930)

Como vemos encontramos bastantes rutas y un mount "/var"

# GANAR ACCESO CON PROFTPD

Vamos a enumerar FTP con ProFtpd en la versión 1.3.5

Si utilizamos "searchsploit" podemos buscar si hay versiones vulnerables.

![image](https://github.com/user-attachments/assets/e9197576-23cc-4108-85d8-b5bc76e3d876)

En este caso utilizaremos el "mod_copy" modulo implementando SITE CPFT y SITE CPTO commands, lo usaremos para copiar directorios de un lugar del servidor y identifciarnos sin necesidad


![image](https://github.com/user-attachments/assets/421ba226-9d77-4367-a6c6-361a23fa2348)

Ahora sabemos que en el directorio /var que es un mount cosa que podemos ver esta la private key.

Vamos a montar dicha cosa

```
mkdir /mnt/kenobiNFS
mount 10.10.73.189:/var /mnt/kenobiNFS
ls -la /mnt/kenobiNFS
```

![image](https://github.com/user-attachments/assets/6e95f1be-bb15-405b-a19e-f940a6640435)

Como vemos ahora podemos meternos dentro de dicha máquina con la clave ssh

![image](https://github.com/user-attachments/assets/10d42ee0-1011-447a-b5e0-42d47699293f)

Gran comando el

```
cp ruta .
```

![image](https://github.com/user-attachments/assets/95816326-d71e-4b9a-8775-efc836d1ca8a)

Estamos dentro!

# ESCALAR PRIVILEGIOS

![image](https://github.com/user-attachments/assets/70f5fa11-1563-45d8-b8ac-2c1165771179)

Vamos a buscar arhicovs del sistema que corran SUID

```
find / -perm -u=s -type f 2>/dev/null
```

![image](https://github.com/user-attachments/assets/3f946c61-a492-4a8e-8c1a-cc96c96d372b)

Encontramos un particular servicio

Como vemos hacen comandos particulares como un curl un uname o un ifconfig

Si vemos el binario es lo que corre

Como vemos el progama corre con usuarios de root, vamos a manipularlo para ganar una shell de root

![image](https://github.com/user-attachments/assets/c997b484-e2e7-4634-99f5-ddf6ef336bfc)

GG!!!!


Hemos copiado la shell /bin/Sh le hemos pasado al curl, dando los corrector permisos.



