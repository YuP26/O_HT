### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №13 - Практика с SELinux**  
**Цель** - работать с SELinux: диагностировать проблемы и модифицировать политики SELinux для корректной работы приложений, если это требуется;

**Задание:**
Что нужно сделать?
1) Запустить nginx на нестандартном порту 3-мя разными способами:\
   переключатели setsebool;\
   добавление нестандартного порта в имеющийся тип;\
   формирование и установка модуля SELinux.\
К сдаче:\
README с описанием каждого решения (скриншоты и демонстрация приветствуются).\
\
2) Обеспечить работоспособность приложения при включенном selinux:\
   развернуть приложенный стенд https://github.com/mbfx/otus-linux-adm/tree/master/selinux_dns_problems ; \
   выяснить причину неработоспособности механизма обновления зоны (см. README);\
   предложить решение (или решения) для данной проблемы;\
   выбрать одно из решений для реализации, предварительно обосновав выбор;\
   реализовать выбранное решение и продемонстрировать его работоспособность.\
К сдаче:\
README с анализом причины неработоспособности, возможными способами решения и обоснованием выбора одного из них;\
исправленный стенд или демонстрация работоспособной системы скриншотами и описанием.\

**Критерии:**  
Статус "Принято" ставится при выполнении следующих условий:
1) для задания 1 описаны, реализованы и продемонстрированы все 3 способа решения;
2) для задания 2 описана причина неработоспособности механизма обновления зоны;
3) для задания 2 реализован и продемонстрирован один из способов решения.
\
Опционально для выполнения:
1) для задания 2 предложено более одного способа решения;
2) для задания 2 обоснованно(!) выбран один из способов решения.

****
#### **Описание работы над заданием 1:**  
Реализация выполнена согласно описанным в методическом указании шагам: [https://docs.google.com/document/d/1jTq4l4UD1CF9C_VFqGXZYunXA2RUap70CfKm_6OXZBU/edit?tab=t.0](https://docs.google.com/document/d/1QwyccIn8jijBKdaoNR4DCtTULEqb5MKK/edit?tab=t.0).  \
Сначала все описанные шаги в методичке были проведены вручную, затем переведены в ansible-playbook.\
Ansible-playbook разбит на 3 блока с меткой, каждый из которых демонстрирует свой способ. Для запуска использовать следующие команды:
```
ansible-playbook -i hosts selinux_1.yml --tags=setsebool
ansible-playbook -i hosts selinux_1.yml --tags=semanage
ansible-playbook -i hosts selinux_1.yml --tags=semodule
ansible-playbook -i hosts selinux_1.yml # для запуска всего плейбука целиком
```

***
##### Запуск стенда
```
OS - Almalinux/9 (версия 9.4.20240805)
ansible [core 2.16.3]
python version = 3.12.3
jinja version = 3.1.2
Vagrant 2.4.3
VirtualBox v.7.0.26 r168464
```

Включаем стенд стандартными средствами, но наблюдаем ошибку запуска nginx:
```
$ vagrant up
Bringing machine 'selinux' up with 'virtualbox' provider...
==> selinux: Box 'almalinux/9' could not be found. Attempting to find and install...
    selinux: Box Provider: virtualbox
    selinux: Box Version: 9.4.20240805
==> selinux: Loading metadata for box 'almalinux/9'
...
selinux: Job for nginx.service failed because the control process exited with error code.
    selinux: See "systemctl status nginx.service" and "journalctl -xeu nginx.service" for details.
    selinux: × nginx.service - The nginx HTTP and reverse proxy server
    selinux:      Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; preset: disabled)
    selinux:      Active: failed (Result: exit-code) since Wed 2025-04-16 10:30:56 UTC; 8ms ago
    selinux:     Process: 6681 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
    selinux:     Process: 6692 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=1/FAILURE)
    selinux:         CPU: 9ms
    selinux: 
    selinux: Apr 16 10:30:56 selinux systemd[1]: Starting The nginx HTTP and reverse proxy server...
    selinux: Apr 16 10:30:56 selinux nginx[6692]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    selinux: Apr 16 10:30:56 selinux nginx[6692]: nginx: [emerg] bind() to 0.0.0.0:4881 failed (13: Permission denied)
    selinux: Apr 16 10:30:56 selinux nginx[6692]: nginx: configuration file /etc/nginx/nginx.conf test failed
    selinux: Apr 16 10:30:56 selinux systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
    selinux: Apr 16 10:30:56 selinux systemd[1]: nginx.service: Failed with result 'exit-code'.
    selinux: Apr 16 10:30:56 selinux systemd[1]: Failed to start The nginx HTTP and reverse proxy server.
The SSH command responded with a non-zero exit status. Vagrant
assumes that this means the command failed. The output for this command
should be in the log above. Please read the output to determine what
went wrong.
```

***
##### Описание шагов и команд
0 - В самом начале проверяем статус nginx, firewalld. Затем проверяем nginx-конфиг, режим работы selinux.
```
systemctl status nginx # проверяем статус nginx
systemctl status firewalld # проверяем статус firewalld для исключение влияния
nginx -t #данная команда проверяет на наличие ошибок
getenforce # проверяем режим работы SELinux - EnForcing - Блокирует все действия, нарушающие политики.
```
\
1 - Разрешим в SELinux работу nginx на порту TCP 4881 c помощью переключателей setsebool. \
Данный способ разрешает сервисам в контексте httpd_t привязываться к портам типа unreserved_port_t, каким является порт 4881.\
Для данного способа были использованы следующие команды: 
```
grep nginx /var/log/audit/audit.log  | audit2why # смотрим указанные логи, связанные c nginx и декодируем их при помощи audit2why - утилиты для анализа и интерпретации записей логов SELinux 
setsebool -P nis_enabled on #разрешаем службам, работающим под управлением SELinux, взаимодействовать с NIS (Network Information Service)
getsebool -a | grep nis_enabled #смотрим состояние данного параметра 
```
\
2 - Теперь разрешим в SELinux работу nginx на порту TCP 4881 c помощью добавления нестандартного порта в имеющийся тип.\
Здесь мы явно указываем тот нестандартный порт, который хотим разрешить:
```
semanage port -l | grep http # смотрим список портов, относящихся к http
semanage port -a -t http_port_t -p tcp 4881 # добавляем требуемый порт
semanage port -d -t http_port_t -p tcp 4881 # удаляем требуемый порт
```
\
3 - Разрешим в SELinux работу nginx на порту TCP 4881 c помощью формирования и установки модуля SELinux.\
Данный способ при помощи утилиты audit2allow анализирует ошибки и генерирует модуль политики SELinux - nginx.pp, которые ранее блокировали работу nginx.
```
grep nginx /var/log/audit/audit.log | audit2allow -M nginx # утилитой audit2allow анализируем лог, связанный с nginx bи генерируем модуль
semodule -i nginx.p # применяем предложенный модуль
semodule -l | grep nginx # из всего списка модулей ищем связанные с nginx
semodule -r nginx # удаляем этот модуль
```
\
****
#### **Описание работы над заданием 2:**  
Реализация выполнена согласно описанным в методическом указании шагам: [https://docs.google.com/document/d/1jTq4l4UD1CF9C_VFqGXZYunXA2RUap70CfKm_6OXZBU/edit?tab=t.0](https://docs.google.com/document/d/1QwyccIn8jijBKdaoNR4DCtTULEqb5MKK/edit?tab=t.0).  \
Сначала все описанные шаги в методичке были проведены вручную, затем переведены в ansible-playbook.\
\
***
##### Запуск стенда
Клонируем предложенный репозиторий https://github.com/Nickmob/vagrant_selinux_dns_problems.git и запускаем стенды:
```
$ git clone https://github.com/Nickmob/vagrant_selinux_dns_problems.git
Cloning into 'vagrant_selinux_dns_problems'...
remote: Enumerating objects: 32, done.
remote: Counting objects: 100% (32/32), done.
remote: Compressing objects: 100% (21/21), done.
remote: Total 32 (delta 9), reused 29 (delta 9), pack-reused 0 (from 0)
Receiving objects: 100% (32/32), 7.23 KiB | 1.81 MiB/s, done.
Resolving deltas: 100% (9/9), done.
$ cd vagrant_selinux_dns_problems/
$ vagrant up
Bringing machine 'ns01' up with 'virtualbox' provider...
Bringing machine 'client' up with 'virtualbox' provider...
==> ns01: Importing base box 'almalinux/9'...
==> ns01: Matching MAC address for NAT networking...
==> ns01: Checking if box 'almalinux/9' version '9.4.20240805' is up to date...
...
TASK [copy transferkey to client] **********************************************
changed: [client]

PLAY RECAP *********************************************************************
client                     : ok=7    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
$ vagrant status
Current machine states:

ns01                      running (virtualbox)
client                    running (virtualbox)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```


***
##### Описание шагов и команд
На VM-client пытаемся внести изменения в зону и проверяем dns-запрос:
```
[vagrant@client ~]$ nsupdate -k /etc/named.zonetransfer.key 
> server 192.168.50.10
> zone ddns.lab
> update add www.ddns.lab 60 A 192.168.50.15
> send
update failed: SERVFAIL
> quit

[vagrant@client ~]$ dig www.ddns.lab

; <<>> DiG 9.16.23-RH <<>> www.ddns.lab
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 53062
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 3c1ad85d1c17295e0100000067ffeb14a110426b9d7c06a1 (good)
;; QUESTION SECTION:
;www.ddns.lab.			IN	A

;; AUTHORITY SECTION:
ddns.lab.		600	IN	SOA	ns01.dns.lab. root.dns.lab. 2711201407 3600 600 86400 600

;; Query time: 3 msec
;; SERVER: 192.168.50.10#53(192.168.50.10)
;; WHEN: Wed Apr 16 17:38:28 UTC 2025
;; MSG SIZE  rcvd: 122
```
Смотрим, есть ли ошибки на клиенте, связанные с SELinux:
```
[vagrant@client ~]$ sudo -i
[root@client ~]# grep named /var/log/audit/audit.log | audit2why
Nothing to do
```
Т.к. ошибок нет, то переходим на сервер. VM-client не отключаем.\
\
Смотрим, есть ли ошибки на сервере, связанные с SELinux:
```
$ vagrant ssh ns01
Last login: Wed Apr 16 17:26:27 2025 from 10.0.2.2
[vagrant@ns01 ~]$ sudo -i
[root@ns01 ~]# grep named /var/log/audit/audit.log | audit2why
type=AVC msg=audit(1744824641.068:1755): avc:  denied  { write } for  pid=7280 comm="isc-net-0001" name="dynamic" dev="sda4" ino=34041089 scontext=system_u:system_r:named_t:s0 tcontext=unconfined_u:object_r:named_conf_t:s0 tclass=dir permissive=0

	Was caused by:
		Missing type enforcement (TE) allow rule.

		You can use audit2allow to generate a loadable module to allow this access.
```
Видим, что проблема связана с отклонением записи контекста named_conf_t. Проверим существующую зону:
```
[root@ns01 ~]# ls -laZ /etc/named
total 28
drw-rwx---.  3 root named system_u:object_r:named_conf_t:s0      121 Apr 16 17:26 .
drwxr-xr-x. 85 root root  system_u:object_r:etc_t:s0            8192 Apr 16 17:26 ..
drw-rwx---.  2 root named unconfined_u:object_r:named_conf_t:s0   56 Apr 16 17:26 dynamic
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      784 Apr 16 17:26 named.50.168.192.rev
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      610 Apr 16 17:26 named.dns.lab
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      609 Apr 16 17:26 named.dns.lab.view1
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      657 Apr 16 17:26 named.newdns.lab
[root@ns01 ~]# ls -laZ /etc/named/dynamic/
total 8
drw-rwx---. 2 root  named unconfined_u:object_r:named_conf_t:s0  56 Apr 16 17:26 .
drw-rwx---. 3 root  named system_u:object_r:named_conf_t:s0     121 Apr 16 17:26 ..
-rw-rw----. 1 named named system_u:object_r:named_conf_t:s0     509 Apr 16 17:26 named.ddns.lab
-rw-rw----. 1 named named system_u:object_r:named_conf_t:s0     509 Apr 16 17:26 named.ddns.lab.view1
```

Видим, что зона dynamic имеет контекст named_conf_t , но т.к. это зона, то контекст должен быть named_zone_t. Исправляем это: 
```
[root@ns01 ~]# chcon -t named_zone_t /etc/named/dynamic/
[root@ns01 ~]# ls -laZ /etc/named/
total 28
drw-rwx---.  3 root named system_u:object_r:named_conf_t:s0      121 Apr 16 17:26 .
drwxr-xr-x. 85 root root  system_u:object_r:etc_t:s0            8192 Apr 16 17:26 ..
drw-rwx---.  2 root named unconfined_u:object_r:named_zone_t:s0   56 Apr 16 17:26 dynamic
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      784 Apr 16 17:26 named.50.168.192.rev
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      610 Apr 16 17:26 named.dns.lab
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      609 Apr 16 17:26 named.dns.lab.view1
-rw-rw----.  1 root named system_u:object_r:named_conf_t:s0      657 Apr 16 17:26 named.newdns.lab
[root@ns01 ~]# ls -laZ /etc/named/dynamic/
total 8
drw-rwx---. 2 root  named unconfined_u:object_r:named_zone_t:s0  56 Apr 16 17:26 .
drw-rwx---. 3 root  named system_u:object_r:named_conf_t:s0     121 Apr 16 17:26 ..
-rw-rw----. 1 named named system_u:object_r:named_conf_t:s0     509 Apr 16 17:26 named.ddns.lab
-rw-rw----. 1 named named system_u:object_r:named_conf_t:s0     509 Apr 16 17:26 named.ddns.lab.view1
```
Снова подключаемся на клиента и делаем те же действия:
```
[vagrant@client ~]$ nsupdate -k /etc/named.zonetransfer.key
> server 192.168.50.10
> zone ddns.lab
> update add www.ddns.lab. 60 A 192.168.50.15
> send
> quit
[vagrant@client ~]$ dig www.ddns.lab

; <<>> DiG 9.16.23-RH <<>> www.ddns.lab
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2776
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 2cac187d946b2b4e0100000067ffeba4d8206ab400d3ad52 (good)
;; QUESTION SECTION:
;www.ddns.lab.			IN	A

;; ANSWER SECTION:
www.ddns.lab.		60	IN	A	192.168.50.15

;; Query time: 3 msec
;; SERVER: 192.168.50.10#53(192.168.50.10)
;; WHEN: Wed Apr 16 17:40:52 UTC 2025
;; MSG SIZE  rcvd: 85
```

***
##### Описание шагов и команд дополнительного способа решения
Данный способ заключается в содании дополнительного модуля политик, разрешающих объектам с контекстам named_conf_t запись. Реализация аналогично первому заданию способу 3:
```
[root@ns01 ~]# grep named /var/log/audit/audit.log | audit2allow


#============= named_t ==============
allow named_t named_conf_t:dir write;
[root@ns01 ~]# grep named /var/log/audit/audit.log | audit2allow -M conf_to_write
******************** IMPORTANT ***********************
To make this policy package active, execute:

semodule -i conf_to_write.pp

[root@ns01 ~]# semodule -i conf_to_write.pp
```
