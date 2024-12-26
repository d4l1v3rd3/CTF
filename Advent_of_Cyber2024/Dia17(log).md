# Objetivos de aprendizaje

- Aprender como extraer archivos personalizados en Splunk
- Aprender como crear un parser para logs personalizados
- Filtrar y buscar resultados usando SPL (Search Processing Language)
- Como investigar en Splunk

# Tiempo de investigación

Es momento de lenvantar Splunk, donde los datos vamos a inestigar el incidente

![image](https://github.com/user-attachments/assets/04727f31-391f-4391-86e4-15ddfee772c7)

Una vez en la siguiente pagina, en el navegador "index=#" en el buscador veremos todos los logs. Vamosa  tener que seleccionar todo el tiempo

![image](https://github.com/user-attachments/assets/66b8cd50-aac1-4ec3-924a-4f58618c0886)

![image](https://github.com/user-attachments/assets/df1a297d-bbac-48ec-add7-a34d819f717c)

Despues de ejecutar la consulta veremos y podremos investigar

si vamos a los tipos de source veremos dos "datasets"

- web_logs
- cctv_logs

- Vamosa  exploirar y investigar como han atacado los servicios CCTV

## Examinar Logs CCTV

Empezaremos en la consulta solo filtrando eso

```
index=* sourcetype=cctv_logs
```

# Entender el problema

Despues de exmaniar los logs

- Splunk no analiza bien los registros
- Splunk no considera el tiempo actual como evento

# Arreglar el problema

Antes de analizar e investigar los logs, vamos a extraer archivos relevantes ajustando el tiempo

## Extraer un nuevo archivo

![image](https://github.com/user-attachments/assets/9ebbc0c7-08c4-43c7-83e6-cdc253903c76)

![image](https://github.com/user-attachments/assets/a6400980-2e52-4914-b83d-4060040b1b23)

Seleccionamos el primer evento

## Seleccionar un archivo

Ahora seleccionaremos el archivo de logs que quermeos extraer, simplemente necesitaremos un log

![image](https://github.com/user-attachments/assets/a8d06528-f6e0-4278-aa64-bb9ae47d9d4b)

## Validar

## Guardar

![image](https://github.com/user-attachments/assets/1c7dab89-7f70-439f-80ce-1febc99ada0d)

regular expresion

```
^(?P<timestamp>\d+\-\d+\-\d+\s+\d+:\d+:\d+)\s+(?P<Event>(Login\s\w+|\w+))\s+(?P<user_id>\d+)?\s?(?P<UserName>\w+)\s+.*?(?P<Session_id>\w+)$
```





