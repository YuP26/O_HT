### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №24 - Настраиваем split-dns**  
**Цель** - Создать домашнюю сетевую лабораторию; Изучить основы DNS; Научиться работать с технологией Split-DNS в Linux-based системах.

**Задание:**  
Что нужно сделать?

    взять стенд https://github.com/erlong15/vagrant-bind

    добавить еще один сервер client2

    завести в зоне dns.lab

    имена

    web1 - смотрит на клиент1

    web2 смотрит на клиент2

    завести еще одну зону newdns.lab

    завести в ней запись

    www - смотрит на обоих клиентов

    настроить split-dns

    клиент1 - видит обе зоны, но в зоне dns.lab только web1

    клиент2 видит только dns.lab


****
#### **Описание реализации:**  
Реализация выполнена согласно описанным в методическом указании шагам: https://docs.google.com/document/d/13kjusaFEzv6Ip_9soeDj2Ry-6WK8IDX7/edit?tab=t.0 \
Дз выполнено через ansible и проверено вручную \

***
##### Подготовка стенда.
```
$ ansible --version
ansible [core 2.16.3]
  config file = None
  configured module search path = ['/home/yup/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/yup/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True

$ vagrant -v
Vagrant 2.4.3
```
Vagrantfile - generic/ubuntu2204\
Предварительно создаем файл *hosts*. \

***
##### Запуск стенда. Запуск локального скрипта и playbook.
```
$ vagrant status

```
##### Проверка:
Client:
```

```
Client2:
```
[vagrant@client2 ~]$ ping www.newdns.lab
ping: www.newdns.lab: Name or service not known
[vagrant@client2 ~]$ ping www.newdns.lab
ping: www.newdns.lab: Name or service not known
[vagrant@client2 ~]$ ping web1.dns.lab
PING web1.dns.lab (192.168.50.15) 56(84) bytes of data.
64 bytes from 192.168.50.15 (192.168.50.15): icmp_seq=1 ttl=64 time=0.712 ms
64 bytes from 192.168.50.15 (192.168.50.15): icmp_seq=2 ttl=64 time=1.63 ms
64 bytes from 192.168.50.15 (192.168.50.15): icmp_seq=3 ttl=64 time=1.78 ms
^C
--- web1.dns.lab ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/mdev = 0.712/1.373/1.776/0.471 ms
[vagrant@client2 ~]$  ping web2.dns.lab
PING web2.dns.lab (192.168.50.16) 56(84) bytes of data.
64 bytes from client2 (192.168.50.16): icmp_seq=1 ttl=64 time=0.033 ms
64 bytes from client2 (192.168.50.16): icmp_seq=2 ttl=64 time=0.109 ms
^C
--- web2.dns.lab ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.033/0.071/0.109/0.038 ms
[vagrant@client2 ~]$ 
```
