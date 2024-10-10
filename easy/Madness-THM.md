# Madness

Test de conectividad

![image](https://github.com/user-attachments/assets/e55371af-fab6-4647-a9ca-3af6b323e4c5)

Escaner de puertos

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.130.40

Starting Nmap 7.60 ( https://nmap.org ) at 2024-10-10 11:59 BST
Nmap scan report for ip-10-10-130-40.eu-west-1.compute.internal (10.10.130.40)
Host is up (0.00027s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ac:f9:85:10:52:65:6e:17:f5:1c:34:e7:d8:64:67:b1 (RSA)
|   256 dd:8e:5a:ec:b1:95:cd:dc:4d:01:b3:fe:5f:4e:12:c1 (ECDSA)
|_  256 e9:ed:e3:eb:58:77:3b:00:5e:3a:f5:24:d8:58:34:8e (EdDSA)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:EA:F9:E9:B6:B1 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.95 seconds
```

Nos encontramos un ssh por el puerto 22 y el 80 

Voy a hacer un escaner un poco mas exaustivo para encontrar mas puertos o vulnerabilidades

Después de estar un rato buscando, encontramos en el código fuente un

![image](https://github.com/user-attachments/assets/5972be11-cc06-4973-b37b-315033d26b3a)

Parece ser que hay algo oculto en la imagen "thm.jpg"

Vamos a descargarla

```
wget http://10.10.130.40/thm.jpg
--2024-10-10 12:23:37--  http://10.10.130.40/thm.jpg
Connecting to 10.10.130.40:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22210 (22K) [image/jpeg]
Saving to: \u2018thm.jpg\u2019

thm.jpg             100%[===================>]  21.69K  --.-KB/s    in 0s      

2024-10-10 12:23:37 (309 MB/s) - \u2018thm.jpg\u2019 saved [22210/22210]
```

Si le hacemos un exiftool para ver los metadatos:

```
exiftool thm.jpg 
ExifTool Version Number         : 10.80
File Name                       : thm.jpg
Directory                       : .
File Size                       : 22 kB
File Modification Date/Time     : 2020:01:06 10:34:26+00:00
File Access Date/Time           : 2024:10:10 12:23:37+01:00
File Inode Change Date/Time     : 2024:10:10 12:23:37+01:00
File Permissions                : rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Warning                         : PNG image did not start with IHDR
```

Nos encontramos que la imagen PNG no empieza con un IHDR

Esto es de la primera vez que me encuentro esto en un CTF con lo cuál voy a tener que entederlo, vamos a utilizar hexedit

```
hexedit thm.jpg
```

![image](https://github.com/user-attachments/assets/1b383ea7-9720-4683-9439-885d59cecef7)

![image](https://github.com/user-attachments/assets/d5aed2b7-d841-47ef-a6c5-6ff10b0f49ce)

Cambiando estos parametros vemos que la imagen va correctamente y encontramos un directorio oculto

![image](https://github.com/user-attachments/assets/d3dace40-8c0d-4fac-a31c-1549c2c047f4)

Vamos a ver que encontramos

![image](https://github.com/user-attachments/assets/08f181e0-be94-4979-8d1a-c2874f761d1a)

En este caso ya me dirás como se llega esto, pero en la Url podemos meter el "secreto"

![image](https://github.com/user-attachments/assets/558060db-6d25-4f07-b5b1-57834ceda4d6)

Esto es un simple programa que haga ?secret= de 0-99

```
package main
import (
    "log"
	"net/http"
	"io/ioutil"
	"strconv"
	"strings"
)
func main() {
	base := "http://10.10.130.40/th1s_1s_h1dd3n/?secret="
	for i := 0; i <100; i++ {
		url := base + strconv.Itoa(i)
		MakeRequest(url)
	}
}
func MakeRequest(url string) {
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalln(err)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}
	if (strings.Contains(string(body), "That is wrong!")) {
	} else {
		log.Println(string(body))
	}
}
```
"Escrito en go"

```
<head>
  <title>Hidden Directory</title>
  <link href="stylesheet.css" rel="stylesheet" type="text/css">
</head>
<body>
  <div class="main">
<h2>Welcome! I have been expecting you!</h2>
<p>To obtain my identity you need to guess my secret! </p>
<!-- It's between 0-99 but I don't think anyone will look here-->

<p>Secret Entered: 73</p>

<p>Urgh, you got it right! But I won't tell you who I am! y2RPJ4QaPF!B</p>

</div>
</body>
</html>
```

Ya tenemos el numero y sacamos parece ser un hash "y2RPJ4QaPF!B"

He probado deshasearlo pero buscando he encontrado que realmente esto no tiene nada que ver tenemos que irnos a la imagen anterior y hacer esteganografia :)

![image](https://github.com/user-attachments/assets/8780bc2e-8c79-41c3-bd5c-1fd203efd9ff) 

"wbxre"

![image](https://github.com/user-attachments/assets/90de3eda-487a-48d8-8bb2-aa76d69f1c04)

Posteriormente, nos descargamos la imagen que hay en la misma CTF, (Esta CTF esta siendo muy rara)

Sacamos la pass con el stefghide

*axA&GF8dP

![image](https://github.com/user-attachments/assets/6045dbc2-faea-4f9b-ae22-2bc5ac9db77d)

Sacamos la primera flag de usuario

https://github.com/calebstewart/pwncat

# Escala de privilegios

EMpezamos lo que de verdad me gusta, primero todo o podemos utilizar privesc o ir haciendo enumeraciones de servicios a ver que encontramos

![image](https://github.com/user-attachments/assets/1f466369-f4ea-4d01-a6bc-f3e4da598d61)

Nos encontramos dos directorios que no son muy normales "screen"

![image](https://github.com/user-attachments/assets/99bc57a8-f157-44e1-af85-0ff8db60c234)

Encontramos exploit de screen-4.5.0 https://www.exploit-db.com/exploits/41154

GG

![image](https://github.com/user-attachments/assets/85e6c2b2-e743-4590-ad09-734284bd6675)




