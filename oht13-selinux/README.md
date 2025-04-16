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

****
#### **Описание работы над заданием 2:**  

***
##### Запуск стенда


***
##### Описание шагов и команд
