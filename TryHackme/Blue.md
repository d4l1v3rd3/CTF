# BLUE

## RECONOCIMIENTO

Escanearemos y aprenderemos como explotar esta máquina vulnerable. Primero de todo haremos un test de conectividad para asegurarnos que tenemos conexion con la máquina.

Test: 

![image](https://github.com/user-attachments/assets/2c3ab456-02dd-486a-bf3f-798c2b413f3e)

Escaneo de puertos:

![image](https://github.com/user-attachments/assets/fce27436-a393-495e-8fec-c7e1f92c1a3c)


Encontramos la vulnerabilidad "ms17-010" sobre Microsoft Windows SMB server pudiendo ejecución remota

## GANAR ACCESO

Iniciamos metasploit

```
msfconsole
```

![image](https://github.com/user-attachments/assets/470fc14d-459a-402b-a542-ddeb9f1b1fda)

![image](https://github.com/user-attachments/assets/726ef427-b904-40be-9926-b971850b79e2)

```
run
```

El payload es automatico

Ctrl +z para ponerla en background

## ESCALAR PRIVILEGIOS

Ahora para empezar ya con el meterpreter detrás necesitaremos upgradear la shell con "post/multi/manage/shell_to_meterpreter"

![image](https://github.com/user-attachments/assets/df0bd309-a461-488d-9991-95140ffcdcee)

Seleccionamos la session en la que tenemos ya iniciado

```
sessions o show sessions
set session 1
run
```

![image](https://github.com/user-attachments/assets/175c4765-4903-44ab-baf2-4d04eb0a280b)

Ahora con "ps" vemos todos los procesos y buscamos uno que sea ejecutado por "NT AUTHORITY\SYSTEM\

![image](https://github.com/user-attachments/assets/6c169338-20ad-40c9-93dd-f5e0c1b88c86)

migramos 

![image](https://github.com/user-attachments/assets/e42aecd1-b4ea-457d-8a64-d77779da2e87)

![image](https://github.com/user-attachments/assets/c6f1cbab-215e-41bf-8979-25bb32a56065)

Cogemos credenciales

![image](https://github.com/user-attachments/assets/7e898124-1454-4282-b392-68fbb9520ef7)

![image](https://github.com/user-attachments/assets/49b92de4-f6a3-49e8-aa71-853a6894dee3)

Para acabar nos encontraremos las flags en rutar importantes

- C:\Users
- C:\Windows\System32\config
- C:\Users\Jon\Documents

  GG

