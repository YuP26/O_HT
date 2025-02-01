### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №1 - Подготовка рабочего места.**  
**Цель** - настроить рабочее место.  

**Критерии:**  
1) После настройки рабочего места у вас не должно возникать проблем с функциональными требованиями для выполнения домашних работ.  
***
#### **Описание реализации:**  
Рабочее место представляет собой ноутбук со следующими характеристиками: CPU - i5-1235U, RAM - 16GB DDR4, NVMe - 512GB PCIx4_gen3, OS - Ubuntu 24.04.1 LTS.  
Настройка производилась через Ansible с временно созданной виртуальной машины. На хост вручную установлен ssh, настроен доступ к ограниченным ресурсам Hashicorp. 

Playbook обновляет систему и устанавливает следующее ПО на рабочее место:    
***traceroute net-tools tcpdump curl wget git Visual Studio Code virtualbox virtualbox-ext-pack ansible vagrant***  

Для подключения к хосту был создан файл inventory.ini следующего содержания:  
```
[myhost]  
192.168.0.122
```

Для запуска playbook использвалась следующая команда:\
`ansible-playbook -i inventory.ini o_ht-1.yml -u user --ask-pass --ask-become-pass | tee o_ht-1_result.txt`

Ниже представлен вывод команды:\
`ansible-playbook -i inventory.ini otus_1.yml -u yup --ask-pass --ask-become-pass | tee otus_1_result.txt`

Результат работы playbook'а:
```
PLAY [Set up work station] *****************************************************

TASK [Gathering Facts] *********************************************************
ok: [192.168.0.122]

TASK [update&upgrade] **********************************************************
ok: [192.168.0.122]

TASK [Available packages installation] *****************************************
changed: [192.168.0.122]

TASK [VS-Code installation] ****************************************************
changed: [192.168.0.122]

TASK [Add key Virtualbox repo] *************************************************
changed: [192.168.0.122]

TASK [Add Virtualbox repo] *****************************************************
changed: [192.168.0.122]

TASK [Virtual Box installation] ************************************************
changed: [192.168.0.122]

TASK [Download VirtualBox Extension Pack] **************************************
changed: [192.168.0.122]

TASK [Install VirtualBox Extension Pack] ***************************************
changed: [192.168.0.122]

TASK [Add key for Hashicorp repo] **********************************************
changed: [192.168.0.122]

TASK [Add Hashicorp repo] ******************************************************
changed: [192.168.0.122]

TASK [Vagrant installation] ****************************************************
changed: [192.168.0.122]

TASK [Collecting result] *******************************************************
changed: [192.168.0.122]

TASK [Show result] *************************************************************
ok: [192.168.0.122] => {
    "msg": [
        "WGET VERSION:",
        "GNU Wget 1.21.4 built on linux-gnu.",
        "",
        "-cares +digest -gpgme +https +ipv6 +iri +large-file -metalink +nls ",
        "+ntlm +opie +psl +ssl/openssl ",
        "",
        "Wgetrc: ",
        "    /etc/wgetrc (system)",
        "Locale: ",
        "    /usr/share/locale ",
        "Compile: ",
        "    gcc -DHAVE_CONFIG_H -DSYSTEM_WGETRC=\"/etc/wgetrc\" ",
        "    -DLOCALEDIR=\"/usr/share/locale\" -I. -I../../src -I../lib ",
        "    -I../../lib -Wdate-time -D_FORTIFY_SOURCE=3 -DHAVE_LIBSSL -DNDEBUG ",
        "    -g -O2 -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer ",
        "    -ffile-prefix-map=/build/wget-LWnKWI/wget-1.21.4=. -flto=auto ",
        "    -ffat-lto-objects -fstack-protector-strong -fstack-clash-protection ",
        "    -Wformat -Werror=format-security -fcf-protection ",
        "    -fdebug-prefix-map=/build/wget-LWnKWI/wget-1.21.4=/usr/src/wget-1.21.4-1ubuntu4.1 ",
        "    -DNO_SSLv2 -D_FILE_OFFSET_BITS=64 -g -Wall ",
        "Link: ",
        "    gcc -DHAVE_LIBSSL -DNDEBUG -g -O2 -fno-omit-frame-pointer ",
        "    -mno-omit-leaf-frame-pointer ",
        "    -ffile-prefix-map=/build/wget-LWnKWI/wget-1.21.4=. -flto=auto ",
        "    -ffat-lto-objects -fstack-protector-strong -fstack-clash-protection ",
        "    -Wformat -Werror=format-security -fcf-protection ",
        "    -fdebug-prefix-map=/build/wget-LWnKWI/wget-1.21.4=/usr/src/wget-1.21.4-1ubuntu4.1 ",
        "    -DNO_SSLv2 -D_FILE_OFFSET_BITS=64 -g -Wall -Wl,-Bsymbolic-functions ",
        "    -flto=auto -ffat-lto-objects -Wl,-z,relro -Wl,-z,now -lpcre2-8 ",
        "    -luuid -lidn2 -lssl -lcrypto -lz -lpsl ../lib/libgnu.a ",
        "",
        "Copyright (C) 2015 Free Software Foundation, Inc.",
        "License GPLv3+: GNU GPL version 3 or later",
        "<http://www.gnu.org/licenses/gpl.html>.",
        "This is free software: you are free to change and redistribute it.",
        "There is NO WARRANTY, to the extent permitted by law.",
        "",
        "Originally written by Hrvoje Niksic <hniksic@xemacs.org>.",
        "Please send bug reports and questions to <bug-wget@gnu.org>.",
        "",
        "-----",
        "TRACEROUTE VERSION:",
        "",
        "-----",
        "CHECKING NET-TOOLS VIA ROUTE COMMAND:",
        "Kernel IP routing table",
        "Destination     Gateway         Genmask         Flags Metric Ref    Use Iface",
        "default         _gateway        0.0.0.0         UG    600    0        0 wlp0s20f3",
        "10.8.0.0        0.0.0.0         255.255.255.0   U     0      0        0 otus",
        "192.168.0.0     0.0.0.0         255.255.255.0   U     600    0        0 wlp0s20f3",
        "",
        "-----",
        "TCPDUMP VERSION:",
        "tcpdump version 4.99.4",
        "libpcap version 1.10.4 (with TPACKET_V3)",
        "OpenSSL 3.0.13 30 Jan 2024",
        "",
        "-----",
        "CURL VERSION:",
        "curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.7",
        "Release-Date: 2023-12-06, security patched: 8.5.0-2ubuntu10.6",
        "Protocols: dict file ftp ftps gopher gophers http https imap imaps ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp",
        "Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd",
        "",
        "-----",
        "GIT VERSION:",
        "git version 2.43.0",
        "",
        "-----",
        "ANSIBLE VERSION:",
        "ansible [core 2.16.3]",
        "  config file = None",
        "  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']",
        "  ansible python module location = /usr/lib/python3/dist-packages/ansible",
        "  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections",
        "  executable location = /usr/bin/ansible",
        "  python version = 3.12.3 (main, Nov  6 2024, 18:32:19) [GCC 13.2.0] (/usr/bin/python3)",
        "  jinja version = 3.1.2",
        "  libyaml = True",
        "",
        "-----",
        "VIRTUALBOX VERSION:",
        "7.0.22r165102",
        "",
        "-----",
        "CHECKING VB EXT-PACK:",
        "Extension Packs: 1",
        "Pack no. 0:   Oracle VM VirtualBox Extension Pack",
        "Version:        7.0.22",
        "Revision:       165102",
        "Edition:        ",
        "Description:    Oracle Cloud Infrastructure integration, Host Webcam, VirtualBox RDP, PXE ROM, Disk Encryption, NVMe, full VM encryption.",
        "VRDE Module:    VBoxVRDP",
        "Crypto Module:  VBoxPuelCrypto",
        "Usable:         true",
        "Why unusable:   ",
        "",
        "-----",
        "VAGRANT VERSION:",
        "Installed Version: 2.4.3",
        "Latest Version: 2.4.3",
        " ",
        "You're running an up-to-date version of Vagrant!",
        "",
        "-----",
        "VS-CODE VERSION:",
        "1.96.4",
        "cd4ee3b1c348a13bafd8f9ad8060705f6d4b9cba",
        "x64"
    ]
}

PLAY RECAP *********************************************************************
192.168.0.122              : ok=14   changed=11   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


