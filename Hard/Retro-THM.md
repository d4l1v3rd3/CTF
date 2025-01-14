Después de mucho tiempo vuelvo a los CTF y vuelvo con uno dificil vamos a ello

Nos comentan que no va a responder a paquetes ICMP ping osea que no vamos a comprobar conectividad vamos a ir directamente a nmap con paquetes arp y ale (Aunque ya nos digan que hay un servidor web) pero vamos a hacerlo como si fuera real :)

```
nmap -sCV -T4 --min-rate 4000 ip
```

```
sudo nmap -sCV -T4 --min-rate 4000 10.10.220.137
Starting Nmap 7.80 ( https://nmap.org ) at 2025-01-14 15:04 GMT
Nmap scan report for 10.10.220.137
Host is up (0.00053s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: RETROWEB
|   NetBIOS_Domain_Name: RETROWEB
|   NetBIOS_Computer_Name: RETROWEB
|   DNS_Domain_Name: RetroWeb
|   DNS_Computer_Name: RetroWeb
|   Product_Version: 10.0.14393
|_  System_Time: 2025-01-14T15:04:58+00:00
| ssl-cert: Subject: commonName=RetroWeb
| Not valid before: 2025-01-13T15:03:15
|_Not valid after:  2025-07-15T15:03:15
|_ssl-date: 2025-01-14T15:04:58+00:00; 0s from scanner time.
MAC Address: 02:0C:2D:F5:AC:5B (Unknown)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.75 seconds
```

Como podemos ver es un sistema Windows, con el puerto 80 y 3389 abierto (HTTP) y (RDP)

![image](https://github.com/user-attachments/assets/c7b26b88-5d0f-466b-95e2-b899d68e013a)

Una página totalmente default parece ser, vamos a meterle un ffuf o un dirbuster

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.220.137/FUZZ

retro                   [Status: 301, Size: 150, Words: 9, Lines: 2]
Retro
```

![image](https://github.com/user-attachments/assets/92b0688a-8da8-41e6-9ece-e3b31c45f3b7)

Haciendo un poco de enumeración encontramos que es un Wordpress

![image](https://github.com/user-attachments/assets/9c0b0be0-6440-4e46-8b66-468eb8092334)

![image](https://github.com/user-attachments/assets/6cb89dbc-742f-4dd8-af0b-45e364c094fb)

Si seguimos enumerando encontramos información importante

Usuario: Wade le encanta parzibal

Vamos a probar esa combinación en wordpress no perdemos nada

Estamos dentro

![image](https://github.com/user-attachments/assets/367667f8-afb0-454e-be5e-58fdcea9b1d9)

Además de todo esto si nos acordamos anteriormente teniamos un RDP, vamos a probar a ver si las credenciales son las correctas.

También podriamos intentar subir una rev shell que probablemente sea por donde tiremos

![image](https://github.com/user-attachments/assets/dce0973e-fc8a-43f9-bcc6-d3400257896f)

Parece ser que esto no es una opción, nos hecha a la hora de hacer la rev shell igual con una un poco más estable se podría llegar a conseguir, simplemente he cambiado el archivo 404.php para hacerlo por una rev shell

Vamos a rdp

```
apt install freerdp2-x11
```

```
xfreerdp /u:wade /p:parzival /v:ip
```

Estamos dentro

![image](https://github.com/user-attachments/assets/80aaa7a2-92a1-42a6-beff-54da10973a1a)

Ya podemos sacara la primera flag de usuario

Ahora nos toca enumerar Windows

En el historial de google encontramos información bastante relevante

![image](https://github.com/user-attachments/assets/0d2e53d2-4b05-4b0f-95ed-15ba1b2079be)


Una breve búsqueda en Google nos informa que CVE-2019–1388 implica manipular un proceso del sistema para iniciar una página web, creando un diálogo de archivo. Aprovechando esto, podemos abrir un símbolo del sistema como System. Aunque pueda parecer complicado, este método es efectivo.

Restablecemos la papelera

![image](https://github.com/user-attachments/assets/3dea99f4-93b3-4790-8176-569955862dd7)

Pasos:

1) find a program that can trigger the UAC prompt screen

2) select "Show more details"

3) select "Show information about the publisher's certificate"

4) click on the "Issued by" URL link it will prompt a browser interface.

![image](https://github.com/user-attachments/assets/a0197b34-cdb6-4d89-a8a2-82e9f5693e4c)

5) wait for the site to be fully loaded & select "save as" to prompt a explorer window for "save as".

6) on the explorer window address path, enter the cmd.exe full path:
C:\WINDOWS\system32\cmd.exe

7) now you'll have an escalated privileges command prompt.

![image](https://github.com/user-attachments/assets/4159f237-7889-4e5d-8aae-4493dff27567)


GG !!!!





