# Objetivos de aprendizaje

- Windows forense
- Conocimientos báscios de kerberos
- Evasión de AV
- Applocker

## Bypass Applocker

HAy muchas maneras de bypasear Applocker

Si applocker ha sido configurado con las reglas predeterminadas, podemos bypasear poniendo un ejecutable en esta ruta
C:\Windows\System32\spool\drivers\color


Como Linux bash, Windows Powershell guarda los comandos anteriores de la consola. Esto esta en:

%userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt

flag : flag{a12a41b5f8111327690f836e9b302f0b}

## Kerberos

Es importante entender como funcoina kerberos

Kerberos es el sistema de autentifiación de windows y las redes de AD: Hay muchas formas de hacer ataques a kerberos.

Vamos a ejecutar setspn

```
setspn -T medin -Q */*
```

Extraeremos todas las cuentas SPN

![image](https://github.com/user-attachments/assets/667570b1-d6ba-4f2d-8c11-dd542be5fd37)

Encontramos al HOST fela@corp.local

Ahora que sabemos el usuario, podemos invocar a kerberos y coger el ticket

```

