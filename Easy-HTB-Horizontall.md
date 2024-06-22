Muy buenas a todos hoy traere la máquina Easy de HTB llamada Horizontall

# SOBRE HORIZONTALL

Es una máquina Linux fácil, en los que encontraremos dos servicios expuestos "HHTP" y "SSH", deberemos enumerar la página y ver sobre que framework esta construida.

Nos fijaremos en el codigo fuente, el CMS que utiliza la CVE que utilizaremos, etc. Hasta encontrar Root.

# INICIO

Para empezar siempre se hacen dos cosas básicas si queremos tres.
1- Identificar el sistema operativo al que nos enfrentamos (en este caso Linux)
2- Comprobar que hay conectividad entre ambas máquinas
3- Hacer un escaneo de puertos.

Todo comprobado utilizaremos el comando que siempre suelo utilizar para escanear puertos.

```
sudo nmap -sCV -T4 --min-rate 1000 IP
```
Como vemos nos encontramos los dos típicos puertos 22 - ssh y 80 - http

