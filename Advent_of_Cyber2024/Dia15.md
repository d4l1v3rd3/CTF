# Objetivos de aprendizaje

- Aprender sobre estructuras de AD
- Aprender sobre ataques comunes de AD
- Ivestigar brechas sobre AD

# Introducción a AD

Antes de meternos a AD, deberemos entender como funciona la red y la estructura de un AD.

Tipicalmente llamado Servicios de directorio, como una mapa que da acceso a la red sus recrusos de la organización. El LDAP es el core de los servicios de directorio. Dando mecanismos de acceso y mapeo de directorio de datos buscandoy devolviendo informacion sobre usuarios, ordenadores y grupos.

- Usuarios
- Grupos
- Ordenadores
- Impresoras y otros recursos

Arquitectura de AD

- Dominios: Grupos logicos de red en los que hay recursos como usuarios, ordenadores y servicios. Estos servicios son configurados por el administrador de dominio y identificados por los componentes de dominio y controladores de dominio.
- Unidades Organizativas (OUs): Son contenedores con el dominio ayudando a agrupas objetos como departamentos, localizaciones y funciones faciles de mantenet.
- Bosques: Una coleccion de uno o mas dominios como si fuera un esqueda. configuraciones y catalogos globales
- Relaciones de confianza: Dominios con bosques y alrededor de ellos que entablan relaciones de confianza para compartir recursos de su dominio.

DN=CN=Mayor Malware
OU=Management
DC=Wareville
DC=thm


# Componentes importantes 

Active Directory contiene componentes clave para dependiendo el rango de los servicios.

- Controladores de dominio
- Catalogos globales
- LDAP
- Autentificación Kerberos

# Politicas grupales

Uno de las características mas importantes de AD, este tipo de politicas aplican a usuarios y ordenadores como contraseñas, software, firewall, etc.

Las GPOs contienes este tip ode politicas, dentro de una OU

Para ir:

1. Ejecutando Windows, abrir el el GPOs con "gpmc.msc"
2. Click derecho y "crear una GPO en este dominio"

![image](https://github.com/user-attachments/assets/6ce4e411-60c6-44d1-b214-4dcd858328b2)

3. Editaremos la politicas

![image](https://github.com/user-attachments/assets/a7947053-61a3-4765-adbc-8260796bd5d9)

4. Configuraremos a sí:

- Minimo rango de contraseñas 12 caracteres
- Historial de contraseñas 10 contraseñas
- Maximo tiempo de contraseñas 90 dias
- Debe tener requerimientos de complejidad

![image](https://github.com/user-attachments/assets/c39d00ef-12dc-42be-8fe2-baef89a1e213)

# Ataques al AD comunes

## Ticket Golden

Etos ataques explotan el protocolo kerberon y cuentas de AD siguiente el TGT (Ticket Grating Tikcet) Comprometiendo la cuenta "krbtgt" y usando la contraseña hasheada, el atacante complemta el ocntrol y se manda a forzar un ticket

## Pass-The-Hash

Este tipo de ataques roban el hash de las contraseñas y se usan para autentificar en servicios que no necesitan la contraseña actual. Es posible porque el protocolo NTL autentica en base a los hashes

# Kerberoasting

Este ataque manda consultas al servicio de los tickets, extrae el ticket y los hashes, los crackea y consigue las contraseñas en texto plano

## Pass-The-Ticket

Los atacantes roban tickets de Kerberon de una máquina comprometica y lo usan para autentificarse como usuario o un servicio

## Malicios GpoS

Gracias a esto se puede crear persistencia, accesos a lugares sin privilegios o ejecutar malware configurando politicas de sofwtre alrededor de l dominio

## Skeleton Key attack

Los atacantes instalan un malware backdoor para loguearse en cualqueir cuenta unsando una contraseña maestra. La contraseña legitima para la cuenta.

# Investigar una brecha de AD

## Politicas de grupo

```
Get-GPO -All
```

Esto nos da una pieza de los GPO. Podemos exportarlo si queremos para que sea más fácil de leer

```
Get-GPOReport -Name "SetWallpaper" -ReportType HTML -Path ".\SetWallpaper.html"
```

- Cuando l GPO ha sido creada y modificada
- Cuando los dispostivos o usuarios
- Permisos
- Usuarios y ordenadores

![image](https://github.com/user-attachments/assets/8060ec98-c0c7-40d9-b271-7b587b55a829)

Dominios son naturalmente tiene que tener GPOs. Nosotros usamos lo mismo "Get-GPO" en PowerShell recientemente modificados.

```
Get-GPO -All | Where-Object { $_.ModificationTime } | Select-Object DisplayName, ModificationTime
```

# Viewer de eventos

Todos los paquetes normalmente se pueden ver en el Event Viewer. Este repositorio guarda todas las actividades, incluido los eventos de seguridad, servicios y etc.

Por ejemplo, dentro de "Security" podemos ver el historias de logs, logsoff etc

![image](https://github.com/user-attachments/assets/9e3744da-10ce-4666-a7dd-ed5d0e98fb1c)

# Auditar Usuario

Las cuentas de usuario se evaluan. Podemos usar el event viewer para ver eventos desde el power shell

```
Get-ADUser -Filter * -Properties MemberOf | Select-Object Name, SamAccountName, @{Name="Groups";Expression={$_.MemberOf}}
```




