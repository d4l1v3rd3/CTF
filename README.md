<p align="center"><img height=100px width=100px src="https://github.com/user-attachments/assets/28eba669-a8dd-418a-bc8d-cc7c8e147edc"></p>

<h1 align="center">Capture The Flag</h1>

<p align="center"><img src="https://github.com/user-attachments/assets/33e80c90-ca9f-4ff4-8cae-3a9d26ec154a"></p>

# INTRODUCCIÓN

Explicare el procedimiento y teoría del aprendizaje y uso para capturar las banderas en las diferentes máquinas de HTB y de Tryhackme

Este repositorio no es un WriteUP es la explicación del proceso, con respectivos comandos y aplicaciones que haran que podamos conseguir la máquina.

Máquinas | Descripción | Dificultad | Plataforma | Sistema Operativo | 
--- | --- | ---- | --- | ---- |
[Fowsniff CTF](https://github.com/d4l1v3rd3/CTF/blob/main/easy/Fowsniff%20CTF-Thackme.md) | SSH - Hydra - POP/IMAP - Exploit Kernel | FÁCIL | THM | LINUX |
[BluePrint](https://github.com/d4l1v3rd3/CTF/blob/main/easy/Blueprint-Thackme.md) | oscommerce - metasploit - RCE - NTLM Hash - RevShell | FÁCIL | THM | WINDOWS |
[LazyAdmin](https://github.com/d4l1v3rd3/CTF/blob/main/easy/LazyAdmin-Thackme.md) | FFUF - CMS SweetRice - LFI - RevShell | FÁCIL | THM | LINUX |
[Toolbox](https://github.com/D4l1-web/HTB/blob/main/easy/Toolbox-HTB.md)  | Docker - ftp - DNS - BurpSuite - sqlmap - shell - id_rsa | FÁCIL | HTB | LINUX | <img height=65 width=65 src=">
[Perfection](https://github.com/D4l1-web/HTB/blob/main/easy/Perfection-HTB.md) | WEBrick 1.7.0 - BurpSuite - SSTI - bypassRuby - revShell  - sqlite  - maskattack | FÁCIL | HTB | LINUX |
[Love](https://github.com/D4l1-web/HTB/blob/main/easy/Love-HTB.md) | SSRF - DNS - LFI | FÁCIL | HTB | WINDOWS |
[Knife](https://github.com/D4l1-web/HTB/blob/main/easy/Knife-HTB.md) | FFUF - PHP - knife | FÁCIL | HTB | LINUX |
[ScriptKiddie](https://github.com/D4l1-web/HTB/blob/main/easy/ScriptKiddie-HTB.md) | msfvenom - cve-2020-7384 - ssh - logs - revShell | FÁCIL | HTB | LINUX |
[Backdoor](https://github.com/D4l1-web/HTB-Maquinas/blob/main/easy/Backdoor-HTB.md) | Wordpress - wp-config.php - P (1337) - Fuerza bruta - gdbaster - RCE | FÁCIL | HTB | LINUX |
[Cap](https://github.com/D4l1-web/HTB-Maquinas/blob/main/easy/CAP-HTB.md) | FTP | FÁCIL | HTB | LINUX |
[Horizontall](https://github.com/D4l1-web/HTB-Maquinas/blob/main/easy/HTB-Horizontall.md) | HHTP - SSH - CMS - CVE | FÁCIL | HTB | LINUX |
[Node_Blog](https://github.com/D4l1-web/HTB-Maquinas/blob/main/easy/NodeBlog-HTB.md) | NOSQL - BURPSUITE - PS AUX | FÁCIL | HTB | LINUX | 
[Pandora](https://github.com/D4l1-web/HTB-Maquinas/blob/main/easy/Pandora-HTB(sin%20terminar).md) | DNS - SNMP - Movimiento Lateral - VirtualHost - ssh sqlmap | FÁCIL | HTB | LINUX |
[Armageddon](https://github.com/D4l1-web/HTB/blob/main/easy/Armageddon-HTB.md) | Drupal - git - mysql - snapd | FÁCIL | HTB | LINUX |
[Spectra](https://github.com/D4l1-web/HTB/blob/main/easy/Spectra-HTB.md) | DNS - SQL - WORDPRESS - SSH - GRUPOS | FÁCIL | HTB | LINUX | 
[Delivery](https://github.com/D4l1-web/HTB/blob/main/easy/HTB-Delivery.md) | FFUF - SSH - LFI - SQL - JOHN | FÁCIL | HTB | LINUX |
[Ignite](https://github.com/d4l1v3rd3/CTF/blob/main/easy/IGNITE-THackme.md) | FUELCMS - RCE - SHELL - PHP | FÁCIL | THM | LINUX |
[Kenobi](https://github.com/d4l1v3rd3/CTF/blob/main/easy/Kenobi-THM.md) | Samba - FTP - Path Variable Manipulation | FÁCIL | THM | LINUX |
[SteelMountain](https://github.com/d4l1v3rd3/CTF/blob/main/easy/SteelMountain-THM.md) | Metasploit - Powershell - HttpFile | FÁCIL | THM | WINDOWS |
[Anthem](https://github.com/d4l1v3rd3/CTF/blob/main/easy/Anthem-THM.md) | RDP - Código Fuente - FFUF | FÁCIL | THM | WINDOWS |
[OverPass](https://github.com/d4l1v3rd3/CTF/blob/main/easy/Overpass-THM.md) | ssh2john - linpeas - python server - rev shell | Fácil | THM | LINUX |
[Expose](https://github.com/d4l1v3rd3/CTF/blob/main/easy/Expose-THM.md) | LFI - SqlMap - RevSHell - Find escala privilegios - Nano - /etc/passwd | FÁCIL | THM | LINUX | 
[Services](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/Services-THM.md) | Kerberos - Hashcat - EvilWinRm - Escala por servicios | MEDIO | THM | WINDOWS | 
[Builder](https://github.com/D4l1-web/HTB/blob/main/Medium/Builder-HTB.md) | Docker - Jenkins - john - ssh | MEDIO | HTB | LINUX |
[Ultratech](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/UltraTech-THB.md) | Docker - ssh - FUZZ - CrackHash - RCE - RevShell | MEDIO | THM | LINUX |
[Biohazard](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/Biohazard-THM.md) | Tar - Gzip - Exiftool - Steghide - Walk - SSH - FTP | MEDIO | THM | LINUX |
[StuxCTF](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/StuxCTF-THM.md) | Python - Decoding - Crypto - RevShell - LFI - Sudo - PHP | MEDIO | THM | LINUX |
[GoldenEye](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/GoldenEye-THM.md) | Decoding - RevShell - Joomla | MEDIO | THM | LINUX |
[CMesS](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/CMesS-THM.md) | Fuzzing Subdominios - RevShell - Cmess - Tar Escala de privilegios | MEDIO | THM | LINUX |
[Atakktive](https://github.com/d4l1v3rd3/CTF/blob/main/Medium/Attacktive_Directory-THM.md) | ActiveDirectory - EvilWin - NTLM - Kerberos - Hash - SMB | MEDIO | THM | WINDOWS |

