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



