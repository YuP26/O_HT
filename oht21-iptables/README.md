### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №21 - Сценарии iptables**  
**Цель** - Написать сценарии iptables.

**Задание:**  
1) Реализовать knocking port: centralRouter может попасть на ssh inetrRouter через knock скрипт
2) Добавить inetRouter2, который виден(маршрутизируется (host-only тип сети для виртуалки)) с хоста или форвардится порт через локалхост.
3) Запустить nginx на centralServer.
4) Пробросить 80й порт на inetRouter2 8080.
5) Дефолт в инет оставить через inetRouter.


****
#### **Описание реализации:**  

Дз выполнено через ansible и проверено вручную \
Реализация выполнена на основе стенда oht19-network, но без office-сегментов. \
К centralRouter (192.168.255.13) добавлено подключение inetRouter2 (192.168.255.14, 10.10.10.2, 192.168.56.13).


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
Current machine states:

inetRouter                running (virtualbox)
inetRouter2               running (virtualbox)
centralRouter             running (virtualbox)
centralServer             running (virtualbox)
office1Router             running (virtualbox)
office1Server             running (virtualbox)
office2Router             running (virtualbox)
office2Server             running (virtualbox)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```
Запускаем плэйбук:
```
$ ansible-playbook -i hosts iptables.yml 
```
***
##### Проверка.

