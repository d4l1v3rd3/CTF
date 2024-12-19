# Monitorizar en un entorno AWS

Care4Wares' es una infraestructura que funciona en cloud, ellos escogieron AWS como proveedor de servicios en la nube (CSP). Una vez ejecutar un trabajo la máquina fisica. Ellos ejecutan instancias virtualizadas en la nube.

Estas instancias en (AWS) llamadas EC2 instancias (Amazon Elastic Compude Cloud). 

Muchos miebmors de SOC no saben usar el analis de log de la nube, y con cambiar el entorno empiezar a cambiar las herramientas y servicios que se necesitas. 

Su tarea esta vez es ayudar a Care4Wares a descubrir qué ha sucedido con los fondos de la organización benéfica; para ello, necesitarán aprender sobre un servicio de AWS llamado CloudWatch.

## CloudWatch

AWD CloudWatch es un monitor y plataforma para observar dando una gran conocimiento dentro del entorno AWS para monitorizar apliaciones multi nivel. CloudWatch da funcionalidades como monitorizar el sistema y metricas de la aplicacion y configuracion de alarmas en caso de esas metricas, vamos a centrarnos especificamente en CloudWatch logs. Ejecutando la aplicacón en un entorno cloud dando diferentes servicios.

- Eventos Log
- Steam Logs
- Groups Logs

## CloudTrail

CloudWatch puede trackear la infraestructura y aplicacion, pero si quieres monitorizar acciones del mismo AWS? Necesitaremos otro servicios llamado AWS CloludTrail. Acciones que puede el rol usuario o servicios AWS o eventos del Cloud

- Siempre activo
- Formato JSON
- Evenetos historicos
- Trails
- Entregable (un solo acceso para varios codigos)

CloudTrail ayuda a capturar acciones. Estas acciones son interacciones con un numero o servicio. Por ejemplo el servicio S3 (Amazon SImple Storage Service) y IAM (Identity and access management) se usan para asegurar accesos al entorno AWS con la creacion de entidad y asigancion de permisos estac acciones el mismo servicio las graba. 

# Intro to JQ

## Que es JQ

JSON-Formatted. Cuando investigamos largos volumenes, la en "machine-readable" formato extrae y expecialmente lo hace para analisis de log. 

## Como se usa?

Ahora vamos a ver como usamos JQ para transformar datos JSON. eelos guardan las listas en formato JSON

```
[

{ "book_title": "Wares Wally", "genre": "children", "page_count": 20 },

{ "book_title": "Charlottes Web Crawler", "genre": "young_ware", "page_count": 120 },

{ "book_title": "Charlie and the 8 Bit Factory", "genre": "young_ware", "page_count": 108 },

{ "book_title": "The Princess and the Pcap", "genre": "children", "page_count": 48 },

{ "book_title": "The Lion, the Glitch and the Wardrobe", "genre": "young_ware", "page_count": 218 }

]
```

JQ coge dos inputs : El filtro que quieres usar, seguimos el input del fichero. Empezamos a filtrara JQ con un . Luego querremos acceder a nuestras arrays o valores guardados de nuestro JSON con [] por ejemplo este comando

```
jq '.[]' book_list.json
```

```
{
  "book_title": "Wares Wally",
  "genre": "children",
  "page_count": 20
}
{
  "book_title": "Charlottes Web Crawler",
  "genre": "young_ware",
  "page_count": 120
}
{
  "book_title": "Charlie and the 8 Bit Factory",
  "genre": "young_ware",
  "page_count": 108
}
{
  "book_title": "The Princess and the Pcap",
  "genre": "children",
  "page_count": 48
}
{
  "book_title": "The Lion, the Glitch and the Wardrobe",
  "genre": "young_ware",
  "page_count": 218
}
```

Una vez accedamos a nuestra array, podemos agarrar elementos directamente al valor

```
jq  '.[] | .book_title' book_list.json
```

## El caso peculiar de Care4Wares

Ahora que tenemos un minimo conocimiento de como funciona.

El 28 de noviembre enviamos un enlace a todos los miembros de nuestra red que lleva a un folleto con los datos de nuestra organización benéfica. Los datos incluyen el número de cuenta para recibir donaciones. Recibimos muchas donaciones el primer día después de enviar el enlace, pero no hubo ninguna a partir del segundo día. Hablé con varias personas que afirmaban haber donado una suma respetable. Uno mostró su transacción y noté que el número de cuenta era incorrecto. Revisé el enlace y seguía siendo el mismo. Abrí el enlace y el folleto digital era el mismo, excepto por el número de cuenta.

McSkidy recuerda haber colocado el folleto digital, wareville-bank-account-qr.png, en un depósito de Amazon AWS S3 llamado wareville-care4wares. Ayudemos a McSkidy y comencemos por averiguar más sobre ese enlace. Antes de eso, revisemos primero la información que tenemos actualmente para comenzar la investigación:

- El dia de despues de que se enviara todo funcionaba
- El segundo dia las donaciones pararon
- Un danador dijo que hizo una 3 dias después y el numero de cuenta era incorrecto
- McSkidy lo pusto dentro de un AWS S· llamado "wareville-bank-account-qr.png" dentro del "cubo" "wareville-care4wares"
- El link no ha sido alterado

# Glich hizo esto

Vamos a examinar los logs de Cloudtrail para ver el "cubo" por ejemplo un log de s3 Se vería a sí.

```
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O5Y2GLD4ZG",
    "arn": "arn:aws:iam::518371450717:user/wareville_collector",
    "accountId": "518371450717",
    "accessKeyId": "AKIAXRMKYT5OZCZPGNZ7",
    "userName": "wareville_collector"
  },
  "eventTime": "2024-10-21T22:13:24Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "ListObjects",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "34.247.218.56",
  "userAgent": "[aws-sdk-go/0.24.0 (go1.22.6; linux; amd64)]",
  "requestParameters": {
    "bucketName": "aoc-cloudtrail-wareville",
    "Host": "aoc-cloudtrail-wareville.s3.ap-southeast-1.amazonaws.com",
    "prefix": ""
  },
  "responseElements": null,
  "additionalEventData": {
    "SignatureVersion": "SigV4",
    "CipherSuite": "TLS_AES_128_GCM_SHA256",
    "bytesTransferredIn": 0,
    "AuthenticationMethod": "AuthHeader",
    "x-amz-id-2": "yqniVtqBrL0jNyGlvnYeR3BvJJPlXdgxvjAwwWhTt9dLMbhgZugkhlH8H21Oo5kNLiq8vg5vLoj3BNl9LPEAqN5iHpKpZ1hVynQi7qrIDk0=",
    "bytesTransferredOut": 236375
  },
  "requestID": "YKEKJP7QX32B4NZB",
  "eventID": "fd80529f-d0af-4f44-8034-743d8d92bdcf",
  "readOnly": true,
  "resources": [
    {
      "type": "AWS::S3::Object",
      "ARNPrefix": "arn:aws:s3:::aoc-cloudtrail-wareville/"
    },
    {
      "accountId": "518371450717",
      "type": "AWS::S3::Bucket",
      "ARN": "arn:aws:s3:::aoc-cloudtrail-wareville"
    }
  ],
  "eventType": "AwsApiCall",
  "managementEvent": false,
  "recipientAccountId": "518371450717",
  "eventCategory": "Data",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "aoc-cloudtrail-wareville.s3.ap-southeast-1.amazonaws.com"
  }
}
```

Puede resultar abrumador ver la gran cantidad de información contenida en un solo evento, pero hay algunos elementos en los que podemos centrarnos para nuestra investigación:

![image](https://github.com/user-attachments/assets/7fe37663-1547-43b1-a69d-42f09c4bf697)

Siguiendo la guia:

- El usuario IAM, wareville_collector, lista todos los objetos del S3 llamado "aoc-cloudtrail-wareville"
- La dirección IP se origina en 34.247.218.56
- El usuario agente indica que la consulta se hace desde AWS SDK tool for go

Ahora que sabemos esto, vamos a utilizar los filtros de JQ para ver eventos rentables. Los logs estan guardados en

```
~/wareville_logs
```

![image](https://github.com/user-attachments/assets/79f2b7e4-7a8a-4b34-a032-670b3910febc)

```
jq -r '.Records[] | select(.eventSource == "s3.amazonaws.com" and .requestParameters.bucketName=="wareville-care4wares")' cloudtrail_log.json
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O7SKYSEJBQ",
    "arn": "arn:aws:iam::518371450717:user/glitch",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5O5PVWAX4S",
    "userName": "glitch",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:21:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:22:23Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "ListObjects",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]",
  "requestParameters": {
    "list-type": "2",
    "bucketName": "wareville-care4wares",
    "encoding-type": "url",
    "max-keys": "300",
    "fetch-owner": "true",
    "prefix": "",
    "delimiter": "/",
    "Host": "s3.ap-southeast-1.amazonaws.com"
  },
  "responseElements": null,
  "additionalEventData": {
    "SignatureVersion": "SigV4",
    "CipherSuite": "TLS_AES_128_GCM_SHA256",
    "bytesTransferredIn": 0,
    "AuthenticationMethod": "AuthHeader",
    "x-amz-id-2": "F6risIBf9y7Ns4EgnmcfUDATYHw6hIyhxT9fSwKnVLLsg7Vyf8XJbY14V26VcvrOTY8cmguI0Dc=",
    "bytesTransferredOut": 369
  },
  "requestID": "WSCGTNEDD4JYW4HK",
  "eventID": "e743f48d-1ed1-4dec-8b8d-da37afde14cb",
  "readOnly": true,
  "resources": [
    {
      "type": "AWS::S3::Object",
      "ARNPrefix": "arn:aws:s3:::wareville-care4wares/"
    },
    {
      "accountId": "518371450717",
      "type": "AWS::S3::Bucket",
      "ARN": "arn:aws:s3:::wareville-care4wares"
    }
  ],
  "eventType": "AwsApiCall",
  "managementEvent": false,
  "recipientAccountId": "518371450717",
  "vpcEndpointId": "vpce-c94096a0",
  "eventCategory": "Data",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "s3.ap-southeast-1.amazonaws.com"
  }
}
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O7SKYSEJBQ",
    "arn": "arn:aws:iam::518371450717:user/glitch",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5O5PVWAX4S",
    "userName": "glitch",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:21:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:22:25Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "ListObjects",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]",
  "requestParameters": {
    "list-type": "2",
    "bucketName": "wareville-care4wares",
    "encoding-type": "url",
    "max-keys": "300",
    "fetch-owner": "true",
    "prefix": "bank-details/",
    "delimiter": "/",
    "Host": "s3.ap-southeast-1.amazonaws.com"
  },
  "responseElements": null,
  "additionalEventData": {
    "SignatureVersion": "SigV4",
    "CipherSuite": "TLS_AES_128_GCM_SHA256",
    "bytesTransferredIn": 0,
    "AuthenticationMethod": "AuthHeader",
    "x-amz-id-2": "Nhj5PXPd7ZFHJX4oVdJEyJIZCdgv5aqUnoffBmy9P1YqePRbNp6tVpGN+Syr2vg/Rp3HKoI/w9A=",
    "bytesTransferredOut": 1006
  },
  "requestID": "DJN1FAZ92V4EQ07J",
  "eventID": "bcb2593b-2d7b-4a25-891a-496f16ecd2f6",
  "readOnly": true,
  "resources": [
    {
      "type": "AWS::S3::Object",
      "ARNPrefix": "arn:aws:s3:::wareville-care4wares/bank-details/"
    },
    {
      "accountId": "518371450717",
      "type": "AWS::S3::Bucket",
      "ARN": "arn:aws:s3:::wareville-care4wares"
    }
  ],
  "eventType": "AwsApiCall",
  "managementEvent": false,
  "recipientAccountId": "518371450717",
  "vpcEndpointId": "vpce-c94096a0",
  "eventCategory": "Data",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "s3.ap-southeast-1.amazonaws.com"
  }
}
{
  "eventVersion": "1.09",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O7SKYSEJBQ",
    "arn": "arn:aws:iam::518371450717:user/glitch",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5OWSCGRHHI",
    "userName": "glitch",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:21:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:22:39Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "PutObject",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36]",
  "requestParameters": {
    "X-Amz-Date": "20241022T152239Z",
    "bucketName": "wareville-care4wares",
    "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
    "x-amz-acl": "bucket-owner-full-control",
    "X-Amz-SignedHeaders": "content-md5;content-type;host;x-amz-acl;x-amz-storage-class",
    "Host": "wareville-care4wares.s3.ap-southeast-1.amazonaws.com",
    "X-Amz-Expires": "300",
    "key": "bank-details/wareville-bank-account-qr.png",
    "x-amz-storage-class": "STANDARD"
  },
  "responseElements": {
    "x-amz-server-side-encryption": "AES256"
  },
  "additionalEventData": {
    "SignatureVersion": "SigV4",
    "CipherSuite": "TLS_AES_128_GCM_SHA256",
    "bytesTransferredIn": 83,
    "SSEApplied": "Default_SSE_S3",
    "AuthenticationMethod": "QueryString",
    "x-amz-id-2": "DJGJVr6MP4Z6kL/mzCdFv1EwLyBmWEhO38EX5QPzwIAEw2BrIW39YX3uU5wNcWWwqxzgsls7Z8hrQrOGAClN2boPBLnDLBIHkH8i4a90Snk=",
    "bytesTransferredOut": 0
  },
  "requestID": "K5FH04G883381FE1",
  "eventID": "b461aefe-7c3d-4056-a28b-3673d5a06dd9",
  "readOnly": false,
  "resources": [
    {
      "type": "AWS::S3::Object",
      "ARN": "arn:aws:s3:::wareville-care4wares/bank-details/wareville-bank-account-qr.png"
    },
    {
      "accountId": "518371450717",
      "type": "AWS::S3::Bucket",
      "ARN": "arn:aws:s3:::wareville-care4wares"
    }
  ],
  "eventType": "AwsApiCall",
  "managementEvent": false,
  "recipientAccountId": "518371450717",
  "eventCategory": "Data",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "wareville-care4wares.s3.ap-southeast-1.amazonaws.com"
  }
}
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "AWSAccount",
    "principalId": "",
    "accountId": "anonymous"
  },
  "eventTime": "2024-11-28T15:22:39Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "PreflightRequest",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "[Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36]",
  "requestParameters": {
    "X-Amz-Date": "20241022T152239Z",
    "bucketName": "wareville-care4wares",
    "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
    "X-Amz-SignedHeaders": "content-md5;content-type;host;x-amz-acl;x-amz-storage-class",
    "Host": "wareville-care4wares.s3.ap-southeast-1.amazonaws.com",
    "X-Amz-Expires": "300",
    "key": "bank-details/wareville-bank-account-qr.png"
  },
  "responseElements": null,
  "additionalEventData": {
    "CipherSuite": "TLS_AES_128_GCM_SHA256",
    "bytesTransferredIn": 0,
    "x-amz-id-2": "q3GB0M0k+FjraWLlkK0O47wuEHC5eNaTQoEeTyd/gNOx8quze7sgHmiRoI3IRTsi6LC/AXRPh6ssOOAGncsbSTrtGUxgrxLgVZUf01LiOv4=",
    "bytesTransferredOut": 0
  },
  "requestID": "K5FWSE708GZHVRRS",
  "eventID": "b3374aaf-7c06-4d23-a11c-abaffc7a3634",
  "readOnly": true,
  "resources": [
    {
      "type": "AWS::S3::Object",
      "ARN": "arn:aws:s3:::wareville-care4wares/bank-details/wareville-bank-account-qr.png"
    },
    {
      "accountId": "518371450717",
      "type": "AWS::S3::Bucket",
      "ARN": "arn:aws:s3:::wareville-care4wares"
    }
  ],
  "eventType": "AwsApiCall",
  "managementEvent": false,
  "recipientAccountId": "518371450717",
  "sharedEventID": "65422b38-403f-4c16-ae22-4a7612562756",
  "eventCategory": "Data",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "wareville-care4wares.s3.ap-southeast-1.amazonaws.com"
  }
}
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O7SKYSEJBQ",
    "arn": "arn:aws:iam::518371450717:user/glitch",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5O5PVWAX4S",
    "userName": "glitch",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:21:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:22:44Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "ListObjects",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-193.880.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]",
  "requestParameters": {
    "list-type": "2",
    "bucketName": "wareville-care4wares",
    "encoding-type": "url",
    "max-keys": "300",
    "fetch-owner": "true",
    "prefix": "bank-details/",
    "delimiter": "/",
    "Host": "s3.ap-southeast-1.amazonaws.com"
  },
  "responseElements": null,
  "additionalEventData": {
    "SignatureVersion": "SigV4",
    "CipherSuite": "TLS_AES_128_GCM_SHA256",
    "bytesTransferredIn": 0,
    "AuthenticationMethod": "AuthHeader",
    "x-amz-id-2": "k7uSA1NUwuziE9acgnrgsSwxSYOB3SnE7QNM19jiS7dzn/c71vJW3QG/zzBPHYHbF9xdbcdhnFE=",
    "bytesTransferredOut": 1006
  },
  "requestID": "5VVAF01CH0NPNC9P",
  "eventID": "9e56ef0f-9e21-4acd-af71-05d1e889aafd",
  "readOnly": true,
  "resources": [
    {
      "type": "AWS::S3::Object",
      "ARNPrefix": "arn:aws:s3:::wareville-care4wares/bank-details/"
    },
    {
      "accountId": "518371450717",
      "type": "AWS::S3::Bucket",
      "ARN": "arn:aws:s3:::wareville-care4wares"
    }
  ],
  "eventType": "AwsApiCall",
  "managementEvent": false,
  "recipientAccountId": "518371450717",
  "vpcEndpointId": "vpce-c94096a0",
  "eventCategory": "Data",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "s3.ap-southeast-1.amazonaws.com"
  }
}
```

```
jq -r '["Event_Time", "Event_Name", "User_Name", "Bucket_Name", "Key", "Source_IP"],(.Records[] | select(.eventSource == "s3.amazonaws.com" and .requestParameters.bucketName=="wareville-care4wares") | [.eventTime, .eventName, .userIdentity.userName // "N/A",.requestParameters.bucketName // "N/A", .requestParameters.key // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t
```

Si observamos el nuevo comando define mas brackets y columnas especifican filtros combinados, seleccionamos arrays, el proceso y los filt

- Cuantos logs tenemos en el bucket?
- Que usuario a intentado logearse
- Que ccion ha echo con el archivo "eventName"
- Que archivos especificos se han editado
- Cual es el tiempo entre logs
- Cual es la IP de los logs

Al observar los resultados, 5 eventos registrados parecen estar relacionados con el depósito wareville-care4wares, y casi todos están relacionados con el usuario glitch. Además de enumerar los objetos dentro del depósito (evento ListOBject), el detalle más notable es que el usuario glitch cargó el archivo wareville-bank-account-qr.png el 28 de noviembre. Esto parece coincidir con la información que recibimos sobre que no se habían realizado donaciones 2 días después de que se envió el enlace.

McSkidy está seguro de que no había ningún usuario glitch en el sistema antes. Tampoco hay nadie en el ayuntamiento con ese nombre. La única persona que McSkidy conoce con ese nombre es el hacker que se mantiene en secreto. McSkidy sugiere que investiguemos a este usuario anómalo.

# McSkidy nos ha engañado?

McSkidy quiere ver la anomalia de la cuenta del usuario, cuand ose creo, como

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "Source_IP"],(.Records[] | select(.userIdentity.userName == "glitch") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
Event_Time            Event_Source                         Event_Name                           User_Name  Source_IP
2024-11-28T15:22:12Z  s3.amazonaws.com                     HeadBucket                           glitch     53.94.201.69
2024-11-28T15:22:23Z  s3.amazonaws.com                     ListObjects                          glitch     53.94.201.69
2024-11-28T15:22:25Z  s3.amazonaws.com                     ListObjects                          glitch     53.94.201.69
2024-11-28T15:22:39Z  s3.amazonaws.com                     PutObject                            glitch     53.94.201.69
2024-11-28T15:22:44Z  s3.amazonaws.com                     ListObjects                          glitch     53.94.201.69
2024-11-28T15:21:54Z  signin.amazonaws.com                 ConsoleLogin                         glitch     53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage                      glitch     53.94.201.69
2024-11-28T15:21:57Z  cost-optimization-hub.amazonaws.com  ListEnrollmentStatuses               glitch     53.94.201.69
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates              glitch     53.94.201.69
2024-11-28T15:22:12Z  s3.amazonaws.com                     ListBuckets                          glitch     53.94.201.69
2024-11-28T15:22:14Z  s3.amazonaws.com                     GetStorageLensConfiguration          glitch     AWS Internal
2024-11-28T15:22:14Z  s3.amazonaws.com                     GetStorageLensDashboardDataInternal  glitch     AWS Internal
2024-11-28T15:22:13Z  s3.amazonaws.com                     GetStorageLensDashboardDataInternal  glitch     AWS Internal
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates              glitch     53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage                      glitch     53.94.201.69
```

El resultado vemos que el usuario Glitch targeteo el s3. El evento notable de "consolelogin" nos dice que la cuenta se uso para acceder a AWS

Necesitamos mas información como herramientas y consultas usadas vamos a ver el "userAgent"

```
jq -r '["Event_Time", "Event_type", "Event_Name", "User_Name", "Source_IP", "User_Agent"],(.Records[] | select(.userIdentity.userName == "glitch") | [.eventTime,.eventType, .eventName, .userIdentity.userName //"N/A",.sourceIPAddress //"N/A", .userAgent //"N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
Event_Time            Event_type        Event_Name                           User_Name  Source_IP     User_Agent
2024-11-28T15:22:12Z  AwsApiCall        HeadBucket                           glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:23Z  AwsApiCall        ListObjects                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:25Z  AwsApiCall        ListObjects                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-192.879.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:39Z  AwsApiCall        PutObject                            glitch     53.94.201.69  [Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36]
2024-11-28T15:22:44Z  AwsApiCall        ListObjects                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-193.880.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:21:54Z  AwsConsoleSignIn  ConsoleLogin                         glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        GetCostAndUsage                      glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        ListEnrollmentStatuses               glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        DescribeEventAggregates              glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:22:12Z  AwsApiCall        ListBuckets                          glitch     53.94.201.69  [S3Console/0.4, aws-internal/3 aws-sdk-java/1.12.750 Linux/5.10.226-193.880.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.412-b09 java/1.8.0_412 vendor/Oracle_Corporation cfg/retry-mode/standard]
2024-11-28T15:22:14Z  AwsApiCall        GetStorageLensConfiguration          glitch     AWS Internal  AWS Internal
2024-11-28T15:22:14Z  AwsApiCall        GetStorageLensDashboardDataInternal  glitch     AWS Internal  AWS Internal
2024-11-28T15:22:13Z  AwsApiCall        GetStorageLensDashboardDataInternal  glitch     AWS Internal  AWS Internal
2024-11-28T15:21:57Z  AwsApiCall        DescribeEventAggregates              glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
2024-11-28T15:21:57Z  AwsApiCall        GetCostAndUsage                      glitch     53.94.201.69  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
```

Un atacante experimentado puede cambiar estos valores, pero no borrar la información. Vamos a ver los logs del mismo usuario

```
.eventSource == "iam.amazonaws.com"
```

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "Source_IP"], (.Records[] | select(.eventSource == "iam.amazonaws.com") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
Event_Time            Event_Source       Event_Name          User_Name  Source_IP
2024-11-28T15:21:26Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:29Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:25Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com  GetPolicy           mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com  CreateLoginProfile  mcskidy    53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com  AttachUserPolicy    mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com  ListPolicies        mcskidy    53.94.201.69
2024-11-28T15:21:44Z  iam.amazonaws.com  ListUsers           mcskidy    53.94.201.69
2024-11-28T15:21:35Z  iam.amazonaws.com  CreateUser          mcskidy    53.94.201.69
```

Basado en resultados vemos muchas listas de politicas ignorando eventos, vemos una gran actividad envolviendo la creación de usuario, atacando una politica y listando usuarios con la ip

Vamos a ver mas detalles de creación de usuario

```
jq '.Records[] |select(.eventSource=="iam.amazonaws.com" and .eventName== "CreateUser")' cloudtrail_log.json
{
  "eventVersion": "1.10",
  "userIdentity": {
    "type": "IAMUser",
    "principalId": "AIDAXRMKYT5O6Z6AZBXU6",
    "arn": "arn:aws:iam::518371450717:user/mcskidy",
    "accountId": "518371450717",
    "accessKeyId": "ASIAXRMKYT5OVOMUJU3P",
    "userName": "mcskidy",
    "sessionContext": {
      "attributes": {
        "creationDate": "2024-11-28T15:20:54Z",
        "mfaAuthenticated": "false"
      }
    }
  },
  "eventTime": "2024-11-28T15:21:35Z",
  "eventSource": "iam.amazonaws.com",
  "eventName": "CreateUser",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "53.94.201.69",
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
  "requestParameters": {
    "userName": "glitch"
  },
  "responseElements": {
    "user": {
      "path": "/",
      "userName": "glitch",
      "userId": "AIDAXRMKYT5O7SKYSEJBQ",
      "arn": "arn:aws:iam::518371450717:user/glitch",
      "createDate": "Oct 22, 2024 3:21:35 PM"
    }
  },
  "requestID": "415e0a96-f1b6-429a-9cac-1c921c0b85f5",
  "eventID": "64dd59fc-c1b1-4f2d-b15c-b005911f1de4",
  "readOnly": false,
  "eventType": "AwsApiCall",
  "managementEvent": true,
  "recipientAccountId": "518371450717",
  "eventCategory": "Management",
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_128_GCM_SHA256",
    "clientProvidedHostHeader": "iam.amazonaws.com"
  },
  "sessionCredentialFromConsole": "true"
}
```

## Logs nunca mueres

Ahora vamos a buscar mas por ip

```
jq -r '["Event_Time", "Event_Source", "Event_Name", "User_Name", "Source_IP"], (.Records[] | select(.sourceIPAddress=="53.94.201.69") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A", .sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
Event_Time            Event_Source                         Event_Name               User_Name      Source_IP
2024-11-28T15:20:38Z  s3.amazonaws.com                     HeadBucket               mayor_malware  53.94.201.69
2024-11-28T15:22:12Z  s3.amazonaws.com                     HeadBucket               glitch         53.94.201.69
2024-11-28T15:22:23Z  s3.amazonaws.com                     ListObjects              glitch         53.94.201.69
2024-11-28T15:22:25Z  s3.amazonaws.com                     ListObjects              glitch         53.94.201.69
2024-11-28T15:22:39Z  s3.amazonaws.com                     PutObject                glitch         53.94.201.69
2024-11-28T15:22:39Z  s3.amazonaws.com                     PreflightRequest         N/A            53.94.201.69
2024-11-28T15:22:44Z  s3.amazonaws.com                     ListObjects              glitch         53.94.201.69
2024-11-28T15:18:37Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-28T15:20:54Z  signin.amazonaws.com                 ConsoleLogin             mcskidy        53.94.201.69
2024-11-28T15:21:54Z  signin.amazonaws.com                 ConsoleLogin             glitch         53.94.201.69
2024-11-28T15:21:26Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:29Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:30Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:25Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:31Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:33Z  iam.amazonaws.com                    GetPolicy                mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com                    CreateLoginProfile       mcskidy        53.94.201.69
2024-11-28T15:21:36Z  iam.amazonaws.com                    AttachUserPolicy         mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:32Z  iam.amazonaws.com                    ListPolicies             mcskidy        53.94.201.69
2024-11-28T15:21:44Z  iam.amazonaws.com                    ListUsers                mcskidy        53.94.201.69
2024-11-28T15:21:35Z  iam.amazonaws.com                    CreateUser               mcskidy        53.94.201.69
2024-11-28T15:21:45Z  organizations.amazonaws.com          DescribeOrganization     mcskidy        53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage          glitch         53.94.201.69
2024-11-28T15:21:57Z  cost-optimization-hub.amazonaws.com  ListEnrollmentStatuses   glitch         53.94.201.69
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates  glitch         53.94.201.69
2024-11-28T15:22:12Z  s3.amazonaws.com                     ListBuckets              glitch         53.94.201.69
2024-11-28T15:21:57Z  health.amazonaws.com                 DescribeEventAggregates  glitch         53.94.201.69
2024-11-28T15:21:57Z  ce.amazonaws.com                     GetCostAndUsage          glitch         53.94.201.69
2024-11-22T11:08:03Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-23T07:19:01Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-24T02:28:17Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-25T21:48:22Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
2024-11-26T22:55:51Z  signin.amazonaws.com                 ConsoleLogin             mayor_malware  53.94.201.69
```

Basados en comandos hay tres usuarios (mayor_malware, glitch y mcskidy) accediendo desde la misma ip. 

Vamos a centrarnos en un usuario si todos van con la misma ip 

```
jq -r '["Event_Time","Event_Source","Event_Name", "User_Name","User_Agent","Source_IP"],(.Records[] | select(.userIdentity.userName=="PLACEHOLDER") | [.eventTime, .eventSource, .eventName, .userIdentity.userName // "N/A",.userAgent // "N/A",.sourceIPAddress // "N/A"]) | @tsv' cloudtrail_log.json | column -t -s $'\t'
```

Cambiamos "PLACEHOLDER" por el usuario

- Que ip se usa normalmente para loguea AWS
- Que navegador se usa
- Que similitudes hay y diferencias entre ip y SO

- El incidente empieza con el usuario mcskidy de la ip 53.94.201.69
- Despues se crea una cuenta llamada "glitch"
- Glich se asigna con permisos de administrador
- La cuenta de glich accede al "cubo" S· y lo llama "wareville-care4wares" y cambia el arcivo. La IP es la misma en el acceso de las 3 cuentas
- El UserAgent y la IP del usuario mcskidy son diferentes

# Evidencias definitivas
McSkidy propone buscar mas fuente y pillar el incidente, vamos a cooperar con "amazon Relational Database Service (RDS)" 

```
~/wareville_logs/rds.log
```

```
grep INSERT rds.log
```

Veremos INSERTS y demás de dicho usuario

![image](https://github.com/user-attachments/assets/7d85bea8-f2ee-408b-85ea-be67bd991bcd)

# Preguntas

Que otra actividad ha echo el usuario glich dentro de ListObject Action?

```
PutObject
```

Cual es la IP usada por los cubos S3 actividades por glitch

```
53.94.201.69
```

Basado en el archivo eventSource,q que servicio de AWS a generado una consola de evento?

```
signin.amazonaws.com
```

Cuando se hizo el evento ConsoleLogin

```
2024-11-28T15:21:54Z
```

Cual es el suaurio creado por mcsikdy?

```
glitch
```

Que tipo de privilegio se dio el usuario?

```
AdministratorAccess
```

Que Ip utiliza normalmente Mayor Malware para iniciar sesión

```
53.94.201.69
```

Cual es la IP actual de McSkidy

```
31.210.15.79
```

Cual es la cuenta de banco de Mayor Malware

```
2394 6912 7723 1294
```




