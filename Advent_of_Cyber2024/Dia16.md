# Objetivos de aprendizaje

- Aprender sobre Azure y como usarlo y porque
- Aprender sobre sus servicios como "Azure Key Vault" y "Microsoft Entra ID"
- Aprender como interactuar con Azure usando una Cloud Shell

# Introducción a Azure

Antes de entender al atacante, vamos a introducir algunos conceptos clave durante el proceso. Vamos a empezar introduciendo con Azure. 

Azure es un CSP (Cloud Service Provider) y como CSPs como Google Cloud y AWS dan recursos de computo como poder o dependiendo de la demanda. 

Azure da muchos beneficios como costes de optimización. Azure acede a los servicios de cloud y se identifica para configura r o mantener, estos serivicios se pueden usar para construir, deployar y configurar dentro de la infraestrucutra.

## Azure Key Vault

Azure Key Vault es un servicio que da segurdad y acesos recretos. Con API keys, certficados de contraseñas, llaves criptograficas y mas. Esencialmente, tood lo que quieras guardar.

## Microsoft Entra ID

Es una solución de Azure. Es una forma de identificar el acceso, esta información necesitamos para el usuario/aplicacion para acceder a X recurso

# Asumiendo una brecha de escenario

Cuando ya estemos dentro de Azure vamos:

## Azure Cloud Shell

Es un navegador basado en linea de comandos para los profesionales de IT

## Azure CLI

Es la interfaz de comandos, para ver y configurar recursos de Azure

![image](https://github.com/user-attachments/assets/c1389e06-5537-4d2e-9acc-7abf7eb230f5)

Una vez estemos dentro podemos ejecutar comandos arbitrarios

```
az ad signed-in-user show
```

![image](https://github.com/user-attachments/assets/ab3e6621-fc8e-4ded-8998-9d9e8213ebd1)


## Enumearcio Entra ID

```
az ad user list
```
Después de ver todos los usuarios con los numeros y cuentas listadas podemos filtrar por nombe

```
az ad user list --filter "startsWith('wvusr-', displayName)"
```

Listar grupos

```
az ad group list
```

Listar grupos específicos

```
az ad group member list --group "Secret Recovery Group"
```

Vamos a limpiar la sesióne iniciar sesión con una cuenta nueva

```
usr-xxxxxxxx [ ~ ]$ az account clear
usr-xxxxxxxx [ ~ ]$ az login -u EMAIL -p PASSWORD
```

## Asignar roles en Azure

Define el recuros usuario o grupo que tiene dicho acceso

```
az role assignment list --assignee REPLACE_WITH_SECRET_RECOVERY_GROUP_ID --all
```

## Azure Key Vault

```
az keyvault list
```

Nombre específico

```
az keyvault secret list --vault-name warevillesecrets
```

Nombre y rol especifico

```
az keyvault secret show --vault-name warevillesecrets --name REDACTED
```








