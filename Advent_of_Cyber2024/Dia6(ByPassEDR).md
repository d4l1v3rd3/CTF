En este Dia probraremos segun lo que pone un Malware creado en una Sandbox

# Objetivos de aprendizaje

- Analizar malware utilizando herramientas de sandbox
- Explorar como usar las reglas de YARA y detectar patrones maliciosos
- Aprender sobre varias técnicas de evasión de Malware
- Implementar tecnicas de evasion para bypassear reglas de detección YARA

# Detectar Sandboxes

Una SandBox (Caja de arena) se utiliza para ejecutar códigos maliciosos sin afectar dentro del sistema. Aveces, multiples herramientas se intalan en el monitor, grabador y analizar código entre otras.

Mayor Malware sabe antes de ejectuar el malware, si necesita checkear si esta dentro de la Sanbox.


Para hacer esto hay mas de una tecnica, primero chekearemos si el directorio es C:\Program Files representando con el registro 

```
HKLM\\Software\\Microsoft\\Windows\\CurrentVersion
```

Una veztengamos el valor visitaremos el editor de registro

![image](https://github.com/user-attachments/assets/5b3856a3-dc9f-4238-9482-76c1f165804f)

```
regedit
```

Este directorio aveces no esta para sanboxes o entornos virtualizados, indicando que podría estar en una sandbox

Aqui tenemos una herramienta en C

```
void registryCheck() {
    const char *registryPath = "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion";
    const char *valueName = "ProgramFilesDir";
    
    // Prepare the command string for reg.exe
    char command[512];
    snprintf(command, sizeof(command), "reg query \"%s\" /v %s", registryPath, valueName);
    // Run the command
    int result = system(command);
    // Check for successful execution
    if (result == 0) {
        printf("Registry query executed successfully.\n");
    } else {
        fprintf(stderr, "Failed to execute registry query.\n");
    }
}
int main() {
    const char *flag = "[REDACTED]";
    registryCheck();
        return 0;

} 
```

No te proecupes si no entiendes cada detalle del codigo. Todo lo que necesitamos saber es que hace la funcion y diseñada para chekear el registro de sistema para una dirección especifica. 

La presencia o ausencia de esta ruta ayuda al malware a determinar si se está ejecutando en un entorno típico o virtualizado, como un sandbox.

# Puede YARA hacerlo

YARA es una herramienta utilizada para identificar y clasificar malware basado en código.  Escrito con unas reglas, los analisis definen las caracteristicas a seguir, como cabeceras o comportamientos, Yara también escanea archivos y procesa correlaciones.

Para esto se escribe un pequeño scrip para ejectuar las reglas cada vez que se ñaade un nuevo evento

```
rule SANDBOXDETECTED
{
    meta:
        description = "Detects the sandbox by querying the registry key for Program Path"
        author = "TryHackMe"
        date = "2024-10-08"
        version = "1.1"

    strings:
        
    $cmd= "Software\\Microsoft\\Windows\\CurrentVersion\" /v ProgramFilesDir" nocase

    

    condition:
        $cmd
}
```

Vamos a entender:

- En las "strings", tenemso definidor las variables qe incluten el valor para $cmd
- En la sección de condicoines, definimos las reglas que queremos que escanee. En este caso, si cualquier string esta presente.

Para testearlo, nos iremos a

```
C:\Tools\YaraMatches.txt
```

Abriremos una powershell y nos iremos a C:\Tools

La herramienta ejectura un system y continuamente genera logs de evneto. Esto alerta la actividad y indica el registro mencionado

```
.\JingleBells.ps1

C:\Tools\Malware

MeeryChrismas.exe
```

![image](https://github.com/user-attachments/assets/0abece5c-9811-4ec9-ba00-9ce8d327a1fb)

![image](https://github.com/user-attachments/assets/36727082-61c8-48d7-ae1e-4aaa0d65f5a1)

Sacamos una flag

# Añadir mas evasiones de técnicas

Com ovemos Yara puede deectar. No nos preocupemos porque vamos a hacer que nuestro malwore sea mejor introduciendo ofuscación

```
void registryCheck() {
// Encoded PowerShell command to query the registry
    const char *encodedCommand = "RwBlAHQALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQAgAC0AUABhAHQAaAAgACIASABLAEwATQA6AFwAUwBvAGYAdAB3AGEAcgBlAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzAFwAQwB1AHIAcgBlAG4AdABWAGUAcgBzAGkAbwBuACIAIAAtAE4AYQBtAGUAIABQAHIAbwBnAHIAYQBtAEYAaQBsAGUAcwBEAGkAcgA=";
    // Prepare the PowerShell execution command
    char command[512];
    snprintf(command, sizeof(command), "powershell -EncodedCommand %s", encodedCommand);

    // Run the command
    int result = system(command);

    // Check for successful execution
    if (result == 0) {
        printf("Registry query executed successfully.\n");
    } else {
        fprintf(stderr, "Failed to execute registry query.\n");
    }  
}
```

## Explicación de codigo

El codigo anteiror es tal que manda una consulta con el mismo "registry key" para obtener información sobre "Program Data" La unica diference es que lo hace codificado usando base64, el codigo lo usa para ejectuar el PowerShell.

Vamos a pasar eso por ejemplo por CyberChief

```
RwBlAHQALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQAgAC0AUABhAHQAaAAgACIASABLAEwATQA6AFwAUwBvAGYAdAB3AGEAcgBlAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzAFwAQwB1AHIAcgBlAG4AdABWAGUAcgBzAGkAbwBuACIAIAAtAE4AYQBtAGUAIABQAHIAbwBnAHIAYQBtAEYAaQBsAGUAcwBEAGkAcgA
```

```
Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion" -Name ProgramFilesDir
```

![image](https://github.com/user-attachments/assets/53ec9623-750f-46a9-9cea-2d1f785af80f)

# Cuidado

Mientras la ofuscación nos ayuda, necesitamos herramientas disponibles para luego extraer la ofusacción del malware. Herramientas como "Floss" tiene funciones similares com oLinux pero optimizado para analisis de malware

```
floss.exe C:\Tools\Malware\MerryChristmas.exe |Out-file C:\tools\malstrings.txt
```

Comando para ver los strings del binario del archivo, el simbolo | simplemente redirecta el output a un txt

Una vez hecho podemos buscar el string "THM" con CTRL + F

# Usar YARA Regar en Sysmon Log

Si queremos que el malware sea indetectable, necesaitamos buscar las reglas de YARA y como pararlas. Por ejemplo, si buscamos o preguntamos als reglas vemos que chekea los logs de Sysmon de cualquier artefacoto que peuda dejar el malware. 

Sysmon, es una herramientas de la Suite de Sysinternals, monitorea y los logs del sistema y acitivada alrededor de los reinicios. Estos servicios proveen con detales y eventos, creaciones, conexiones a red, y carga de archivos. 

La regla por ejemplo con eventos sería

```
event id 1: Process created
```

Hay muchas entradas en el log de Symon para hacer mas fácil encontrar eventos, podemos aplicar filtros customizados usando "EventRecordID" podemos verlo por ejemplo en el log YaraMatches.txt localizado en C:\Tools

Abriremos la PowerSHell

```
get-content C:\Tools\YaraMatches.txt
```

![image](https://github.com/user-attachments/assets/47b12b0c-866e-4d62-b688-4fc8d9001ce4)

Debajo de "Event Record Id" vemos el valor usamos este valor para crar filtro

Podemos abrir el event viewer de windows y clicar dentro para navegar

```
Applications and Services Logs -> Microsoft -> Windows -> Sysmon -> Operational
```

![image](https://github.com/user-attachments/assets/677d4dd9-caf6-468c-a49d-658f4d9a8941)

Navegaremos a XML y tickaremos la checkbos para editar queris manualmente y clickaremos sobre si

```
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-Sysmon/Operational">
    <Select Path="Microsoft-Windows-Sysmon/Operational">
      *[System[(EventRecordID="INSERT_EVENT_record_ID_HERE")]]
    </Select>
  </Query>
</QueryList>
```

Remplazaremos el evento Record por un valor que recordemos antes. Aplicaremos el filtro y veremos detalles.

# Preguntas

Cual es la bandera descubierta en el windows después de utilizar el EDR?

```
THM{GlitchWasHere}
```

Cual es la bandera que encontramos en malstring.txt despues de ejecutar floss.exe, y abriremos el editor de texto

```
THM{HiddenClue}
```


