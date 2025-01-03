# Objetivos de aprendizaje

- Entender como funciona y como se ejecutan las API
- Interceptar y modifical API internas usando Frida
- Hackear un juego con la ayuda de Frida.

# Game Hacking

Mientras los penetration tester se volvian populares, los hackers de videojuegos solo tenian una puqueña porción de ciberseguridad. En 2023 aproximadamente el $183.9 billones, de la industria de los videojuegos fueron atacados. Gracias a activiadaes maliciosos, juegos para activar ilegitamente, automatizar con vots, logica de videojuegos

# Ejecutables y Librerias

Los archivos ejectuables como aplicaciones generalmente tienen archivos binarios que ocntienen condigo de como se va a ejecutar. Mientras las aplicaciones contienen todo el codigo que necesitan ejectuar, muchas apliacciones normalmente necesitan codigo externo de librerias

Las librerias contienen colecciones de funciones que muchas aplciaciones reusan. Como aplicaciones, directamente se ejecutan. La libreria ejectua la fucniona y la ejecución es llamada.

![image](https://github.com/user-attachments/assets/21210a8f-34bc-4a17-8663-e186d82ba46b)

Cuando la aplicación confia en la libreria la consulta puede ser cogia y la funcion cambiada.

# Hackeando con Frida

Frida es una herramienta de instrumentación en la que podemos analizar, modificar y interactuar con las aplicaciones. Como es est? Frida crea un proceso de targeteo ejecutando los códigos de bootstrap. Esta interacción, sabe que es el agente, permitiendo injectar código JS, controlado la aplicación en tiempo real. Uno de la funcionalidad mas imporantes es el interceptor. Esta funcioanlidad altera las funciones.

![image](https://github.com/user-attachments/assets/890e8a7b-bf81-43ea-b0ec-67ccd8d3e9ef)

Vamos a ver un ejemplo hypotetico

```
./main
Hello, 1!
Hello, 1!
Hello, 1!
Hello, 1!
Hello, 1!
Hello, 1!
Hello, 1!
Hello, 1!
```

Antes de proceder vamos a ejecutar "frida-trace" para la primera vez crea handlers para cada funcion de librear usando el juego. Editando archivos, podemos decir a frida que interactue y llame a las funciones para ver los valores

```
frida-trace .main -i '*'
```

Ahora podremos ver los __handlers__ directory, conteniendo archivos Javascripts diciendonos las funciones que llaman a las librerias. Estas funciones se llaman por ejemplo "say_hello()" y con su correspondiente ruta.

Ahora deberemos entender que hace dicho archivo

- onEnter : esta funciona, es muy interesatne por la variable args.
- onLeave: Interesante por la variable rretval

```
// Frida JavaScript script to intercept `say_hello` 
Interceptor.attach(Module.getExportByName(null, "say_hello"), { 
    onEnter: function (log, args, state) { }, 
    onLeave: function (log, retval, state) { } 
});
```

Tenemos pointers y variables porque si se cambiar cualquier valor, es permanente, podemos modificar un valor copiado, para que no persista

Devolviendo el objetivo, queremos que el parametro con 1337 remplaze los argumentos de la array

Frida tiene una funcion llamda ptr() es exactamente lo uqe necestiamos

```
// say_hello.js
// Hook the say_hello function from libhello.so

// Attach to the running process of "main"
Interceptor.attach(Module.findExportByName(null, "say_hello"), {
    onEnter: function (args) {
        // Intercept the original argument (args[0] is the first argument)
        var originalArgument = args[0].toInt32();
        console.log("Original argument: " + originalArgument);
        // Replace the original value with 1337
        args[0] = ptr(1337);
        log('say_hello()');
    }
});
```

Cuando ejecutamos y ponemos la funciona 1337

```
frida-trace ./main -i 'say*'
Hello, 1337!
Original argument: 1
/* TID 0x5ec9 */
11 ms  say_hello()
Hello, 1337!
Original argument: 1
```

Ahora que lo entendemos mejor vamos a ello




