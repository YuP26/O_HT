### **Otus - Administrator Linux. Professional.**  
#### **Проект - Динамическое веб-приложение по созданию заметок**  
**Цель:** 
Закрепить и продемонстрировать полученные знания и навыки;\
Создать веб-проект;\
Подготовить портфолио для работодателя;

**Задание:**  
Веб проект (не статический html) с развертыванием нескольких виртуальных машин должен отвечать следующим требованиям:

1) включен https;
2) основная инфраструктура в DMZ зоне (желательно);
3) файрволл на входе (доступен только тот сервис, который планируеся использоваться клиентами);
4) сбор метрик и настроенный алертинг;
5) база данных с репликацией (master-slave)
6) организован централизованный сбор логов;
7) организован backup;
8) демонстрация аварийного восстановления любого сбойного узла с помощью оркестратора.

****
#### **Описание реализации:**
Состав проекта:
| VM | IP | Назначание |
|-------------|-------------|-------------|
| nginx | 192.168.56.10  | Веб-сервер с доступом к приложению |
| backend | 192.168.56.20  | бэкенд приложения на Django  |
| masterdb | 192.168.56.30  | мастер БД mariadb для работы с приложением |
| slavedb | 192.168.56.31  | слейв БД для репликаций мастера |
| monitorint | 192.168.56.40  | grafana+rsyslog  |
| backup | 192.168.56.50  | borgbackup для бэкапа VMs|

Состав плэйбука:
1) start - поочередно перебирает все плейбуки для полного развертывания приложения;
2) common_start - установка базовых пакетов, настройка времени, генерация ssh-ключенй для настройки borgbackup;
3) nginx - настройка веб сервера (добавление сертификата/ключа, настройка https, обратного прокси до бэкенда);
4) backend - настройка бэкенда (передача файлов приложения, запуск сервисов, миграций);
5) masterdb|slavedb - настройка БД (передача конфиг-файлов, создание пользователей, запуск БД);
6) monitoring - настройка логирования и мониторинга/алертинга (rsyslog, grafana, prometheus, node_exporter, alertmanager);
7) backup - настройка бэкапов со всех машин (borgbackup).

Развертывание приложения (нужен vpn):
```
$ vagrant up
---
$ vagrant status
Current machine states:

nginx                     running (virtualbox)
backend                   running (virtualbox)
masterdb                  running (virtualbox)
slavedb                   running (virtualbox)
monitoring                running (virtualbox)
backup                    running (virtualbox)
---
$ ansible-playbook -i ansible/inventory.ini ansible/start.yml
```
Доступ:
1) https://192.168.56.10 - приложение;
2) https://192.168.56.40:8443 - grafana.


Восстановление VMs:
```
$ ansible-playbook -i ansible/inventory.ini ansible/repair.yml --limit <hostname>
```
Принцип: 
1) Nginx, Backend, Monitoring, Slave - проходятся по базовой настройке.
2) MasterDB - дополнительно остнавливает реплику, снимает дамп, передает его на мастер и снова запускает реплику.
3) Backup - заново добавляются уже созданные ключи и частично прогоняется базовый конфиг.


****
#### **Демонстрация:**
Приложение:
![WebApp-Login](https://github.com/YuP26/O_HT/blob/main/project/screens/webapp1.png)\
![WebApp-Reg](https://github.com/YuP26/O_HT/blob/main/project/screens/webapp2.png)\
![WebApp-Noteadd](https://github.com/YuP26/O_HT/blob/main/project/screens/webapp3.png)\
![WebApp-Note](https://github.com/YuP26/O_HT/blob/main/project/screens/webapp4.png)\
![WebApp-Notedel](https://github.com/YuP26/O_HT/blob/main/project/screens/webapp5.png)\

Мониторинг-алертинг:
(1 скрин)
![Мониторинг](https://github.com/YuP26/O_HT/blob/main/project/screens/monitoring.png)\

Бэкапы:
```
root@backup:/backups# ls
backend  masterdb  monitoring  nginx  slavedb
root@backup:/backups# borg list nginx 
Enter passphrase for key /backups/nginx: 
etc-2025-06-30_00:37:12              Mon, 2025-06-30 00:37:15 [413791c1cd8aa6f8824fa2fc2e6cefb7798befda8a7da9470e9440f3d548d94a]
etc-2025-06-30_00:39:19              Mon, 2025-06-30 00:39:20 [88a4610bb605bf95cd93bd0925b6189d19cb2eaee6815921d6f835ac39ffa841]
etc-2025-06-30_00:41:29              Mon, 2025-06-30 00:41:30 [8a17209c640097763e9cf903b36ae0a6ed467c59a57fbea9e03740c9a5e3aede]
etc-2025-06-30_00:43:40              Mon, 2025-06-30 00:43:41 [e4e4e7acb39d0920c8b59111f6e2d0b555205566d25491a32e18c3a794ff1db8]

```
Логи:
```
root@monitoring:~# ls /var/log/rsyslog/
192.168.56.10  192.168.56.20  192.168.56.30  192.168.56.31  192.168.56.50

root@monitoring:~# ls /var/log/rsyslog/192.168.56.20
CRON.log      kernel.log         python3.log   sshd.log  systemd.log         systemd-udevd.log
gunicorn.log  node_exporter.log  rsyslogd.log  sudo.log  systemd-logind.log  useradd.log

root@monitoring:~# cat /var/log/rsyslog/192.168.56.30/kernel.log 
Jun 30 00:37:25 masterdb kernel: [ 1229.786491] [UFW BLOCK] IN=eth1 OUT= MAC=08:00:27:f0:ac:d1:08:00:27:07:01:8d:08:00 SRC=192.168.56.40 DST=192.168.56.30 LEN=340 TOS=0x00 PREC=0x00 TTL=64 ID=5135 DF PROTO=TCP SPT=59520 DPT=9100 WINDOW=501 RES=0x00 ACK PSH URGP=0 
Jun 30 00:37:25 masterdb kernel: [ 1230.006330] [UFW BLOCK] IN=eth1 OUT= MAC=08:00:27:f0:ac:d1:08:00:27:07:01:8d:08:00 SRC=192.168.56.40 DST=192.168.56.30 LEN=340 TOS=0x00 PREC=0x00 TTL=64 ID=5136 DF PROTO=TCP SPT=59520 DPT=9100 WINDOW=501 RES=0x00 ACK PSH URGP=0 
```
Master/SlaveDB:
```
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| webapp_db          |
+--------------------+
5 rows in set (0.002 sec)


MariaDB [(none)]> use webapp_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [webapp_db]> show tables;
+----------------------------+
| Tables_in_webapp_db        |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| notes_note                 |
+----------------------------+
11 rows in set (0.001 sec)

MariaDB [webapp_db]> select * from notes_note;
+----+----------------+------------------------------+----------------------------+----------------------------+-----------+
| id | title          | body                         | created_at                 | updated_at                 | author_id |
+----+----------------+------------------------------+----------------------------+----------------------------+-----------+
|  2 | Заметка        | ЗаметкаЗаметка               | 2025-06-29 21:57:15.287201 | 2025-06-29 21:57:15.287286 |         1 |
+----+----------------+------------------------------+----------------------------+----------------------------+-----------+
1 row in set (0.002 sec)
```
