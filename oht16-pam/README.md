### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №16 - Vagrant-стенд c PAM**  
**Цель** - Научиться создавать пользователей и добавлять им ограничения.

**Задание:**
1) Запретить всем пользователям кроме группы admin логин в выходные (суббота и воскресенье), без учета праздников.
2) *Дать конкретному пользователю права работать с докером и возможность перезапускать докер сервис.

****
#### **Описание реализации:**  
Реализация выполнена согласно описанным в методическом указании шагам: [[https://docs.google.com/document/d/1jTq4l4UD1CF9C_VFqGXZYunXA2RUap70CfKm_6OXZBU/edit?tab=t.0](https://docs.google.com/document/d/1Xz7dCWSzaM8Q0VzBt78K3emh7zlNX3C-Q27B6UuVexI/edit?tab=t.0#heading=h.csr8pmcyj3iq)](https://docs.google.com/document/d/1lOFe3rv0QcnvOTNfQm0OMHbNQ0Cet6AR/edit?tab=t.0) \
Дз выполнено через ansible и проверено вручную. \

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
##### Запуск стенда. Проверка.
Ansible-playbook запускается в провижине при включении виртуальной машины.\
Результат выполнения в файле prov_res.txt\

Пытаемся безуспешно залогиниться по ssh по пользователем otus:
```

```

Теперь успешно через otusadm:
```

```
Теперь безуспешно пробуем перезапустить докер и выполнить команды через docker-cli через otusadm:
```

```
Теперь успешно через пользователя otus:
```

```
