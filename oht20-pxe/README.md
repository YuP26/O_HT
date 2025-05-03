### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №20 - Настройка PXE сервера для автоматической установки**  
**Цель** - Отработать навыки установки и настройки DHCP, TFTP, PXE загрузчика и автоматической загрузки.

**Задание:**  
1) Настроить загрузку по сети дистрибутива Ubuntu 24
2) Установка должна проходить из HTTP-репозитория.
3) Настроить автоматическую установку c помощью файла user-data
4) Задания со звёздочкой* : Настроить автоматическую загрузку по сети дистрибутива Ubuntu 24 c использованием UEFI


****
#### **Описание реализации:**  
Реализация выполнена согласно описанным в методическом указании шагам: [[[https://docs.google.com/document/d/1jTq4l4UD1CF9C_VFqGXZYunXA2RUap70CfKm_6OXZBU/edit?tab=t.0](https://docs.google.com/document/d/1Xz7dCWSzaM8Q0VzBt78K3emh7zlNX3C-Q27B6UuVexI/edit?tab=t.0#heading=h.csr8pmcyj3iq)](https://docs.google.com/document/d/1wXZLFDG7NSsrmeSmL0qqec6H9CFAYIolDfiFbDa2WBU/edit?tab=t.0)](https://docs.google.com/document/d/1f5I8vbWAk8ah9IFpAQWN3dcWDHMqXzGb/edit?tab=t.0) \
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
##### Запуск playbook.
После запуска виртуальной машины запускаем плэйбук (он настроит PXE сервер):
```
$ ansible-playbook -i hosts pxe.yml
```
***
##### Проверка загрузки клиента.
**Legacy:**\
![Получение образа](https://github.com/YuP26/O_HT/blob/main/oht20-pxe/legacy-1.png)\
![Процесс установки](https://github.com/YuP26/O_HT/blob/main/oht20-pxe/legacy-2.png)\
![Установленная система](https://github.com/YuP26/O_HT/blob/main/oht20-pxe/legacy-2.png)\
\
**UEFI:**\
Добавлены конфиги в /srv/tftp/amd64/grub/grub.cfg. \
Пришлось увеличивать объем ОЗУ до 8ГБ, иначе не зависает на разных этапах.\
![GRUB](https://github.com/YuP26/O_HT/blob/main/oht20-pxe/uefi-1.png)\
![Процесс установки](https://github.com/YuP26/O_HT/blob/main/oht20-pxe/uefi-2.png)\
![Установленная система](https://github.com/YuP26/O_HT/blob/main/oht20-pxe/uefi-3.png)\
