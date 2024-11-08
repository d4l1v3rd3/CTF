# Daily Bugle 

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.17.253

Starting Nmap 7.60 ( https://nmap.org ) at 2024-11-08 12:17 GMT
Nmap scan report for ip-10-10-17-253.eu-west-1.compute.internal (10.10.17.253)
Host is up (0.00041s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 68:ed:7b:19:7f:ed:14:e6:18:98:6d:c5:88:30:aa:e9 (RSA)
|   256 5c:d6:82:da:b2:19:e3:37:99:fb:96:82:08:70:ee:9d (ECDSA)
|_  256 d2:a9:75:cf:2f:1e:f5:44:4f:0b:13:c2:0f:d7:37:cc (EdDSA)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.6.40)
|_http-generator: Joomla! - Open Source Content Management
| http-robots.txt: 15 disallowed entries 
| /joomla/administrator/ /administrator/ /bin/ /cache/ 
| /cli/ /components/ /includes/ /installation/ /language/ 
|_/layouts/ /libraries/ /logs/ /modules/ /plugins/ /tmp/
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.6.40
|_http-title: Home
3306/tcp open  mysql   MariaDB (unauthorized)
MAC Address: 02:DF:DB:D2:6E:2B (Unknown)
```

Vaya vaya, una base de datos ;)

y una web en el que vemos que tenemos el /robots.txt que esta quitando bastantes entries pero veremos a ver

Parece ser jajaj que el puto spider-man a robado un banco!!

![image](https://github.com/user-attachments/assets/0ee6da09-1446-4b84-8ad1-aadb4ceb8359)

También podemos ver un logeo vamos a enumerar subdominios a ver que encontramos

Encontramos la página de logeo de Joomla en /administrator

![image](https://github.com/user-attachments/assets/96bd96f1-c06b-4f88-80a5-c97ef47999bd)

Podriamos enumerar de mil formas para sacar la versión

De las formas de enumerar Joomla tenemos el /robots.txt y el /README.txt 

Sacamos la versión de Joomla: 3.7.0

![image](https://github.com/user-attachments/assets/6bcdeebb-773d-4e05-866d-c4f3e0112ff8)

Vaya vaya que casualidad justo.. un SQL injection

![image](https://github.com/user-attachments/assets/9bd6c5eb-adc8-4f38-9ae8-8fb28635efef)

Nos comenta que la url vulnerable es esta:

```
http://localhost/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml%27
```

En mi caso utilizare SQLmap:

```
sqlmap -u "http://localhost/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering]
```

También tenemos un python que lo hace automaticamente y no nos tenemos que meter con sqlMap para otras personas:

https://github.com/XiphosResearch/exploits/tree/master/Joomblah

![image](https://github.com/user-attachments/assets/33138513-3a22-4e86-be3a-6819636401ad)

Sacamos el hash 

Vamos a identificar el hash y posteriormente deshasearlo como vemos que empeiza con $2 podemos ir identificando

Después de unos minutos con john sacamos la contraseña: spiderman123

Vamos a probar a meternos al joomla

```
jonah:spiderman123
```

![image](https://github.com/user-attachments/assets/a5058f07-1c56-40d2-86c2-935f0f9ca6b6)

Estamos dentro. 

Como ya sabemos joomla suele tener problemas con los templates pudiendo cambiar su configuracion, vamos a crear una rev shell y vamos a probar en un archivo php por ejemplo el index.php que es el que carga la página y cambiarlo por una 

![image](https://github.com/user-attachments/assets/351fdcba-7e7c-4f9c-a44b-03c8e848c822)

Simplemente reiniciamos la página y veremos como nos conecta

![image](https://github.com/user-attachments/assets/0dcb7701-f085-4f44-a58f-8fc4322cfeb8)

No tenemos permisos para coger la flag del usuario o meternos a su directorio

![image](https://github.com/user-attachments/assets/15d655ec-231e-4d7c-835d-4d808636a2f6)

Enumerando el sistema nos encontramos en el directorio /var/www/html/configuration.php esto:

![image](https://github.com/user-attachments/assets/64258ba4-f995-4c18-9ff2-8d79d9b3e5fe)

nv5uz9r3ZEDzVjNu

![image](https://github.com/user-attachments/assets/097d1d76-2657-4c6e-9c60-b4b1b0f6a9cd)

Estamos dentro, voy a upgradear la shell porque da pena

Con esto ya tenemos la primera flag:

![image](https://github.com/user-attachments/assets/f5ef3fdd-29d3-4968-b508-002e60f3ce25)

Vamos a enumerar que privilegios tenemos

![image](https://github.com/user-attachments/assets/68b07506-c1c7-41fb-a1ea-06edf446660d)

![image](https://github.com/user-attachments/assets/c68adeec-d4b7-42f9-bf8e-4f3e22c37329)

Esto lo hemos sacado de gtfobins yum

https://gtfobins.github.io/gtfobins/yum/

GGGGG SOMOS ROOT HAPPY HACKINGGG
