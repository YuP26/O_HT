### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №29 - Репликация postgres**  
**Цель** - Научиться настраивать репликацию и создавать резервные копии в СУБД PostgreSQL;


**Задание:**  
1) настроить hot_standby репликацию с использованием слотов
2) настроить правильное резервное копирование

#### **Описание реализации:**  
Реализация выполнена согласно описанным в методическом указании шагам. \
https://docs.google.com/document/d/1EU_KF3x9e2f75sNL4sghDIxib9eMfqex/edit?tab=t.0 \
Дз выполнено через vagrant+ansible и проверено вручную \

****
#### **Проверка**  
настроить hot_standby репликацию с использованием слотов
```
vagrant@node1:~$ sudo -u postgres psql
could not change directory to "/home/vagrant": Permission denied
psql (14.18 (Ubuntu 14.18-0ubuntu0.22.04.1))
Type "help" for help.

postgres=# CREATE DATABASE otus_test;
CREATE DATABASE
postgres=#  \l
                              List of databases
   Name    |  Owner   | Encoding | Collate |  Ctype  |   Access privileges   
-----------+----------+----------+---------+---------+-----------------------
 otus_test | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
(4 rows)

vagrant@node2:~$ sudo -u postgres psql
could not change directory to "/home/vagrant": Permission denied
psql (14.18 (Ubuntu 14.18-0ubuntu0.22.04.1))
Type "help" for help.

postgres=#  \l
                              List of databases
   Name    |  Owner   | Encoding | Collate |  Ctype  |   Access privileges   
-----------+----------+----------+---------+---------+-----------------------
 otus_test | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
(4 rows)


node1
 pid  | usesysid |  usename   |  application_name  |  client_addr  | client_hostname | client_port |         backend_start         | backend_xmin |   state   | sent_lsn  | write_lsn | flush_lsn | replay_lsn |    write_lag    |    flush_lag    |   replay_lag    | sync_priority | sync_state |          reply_time           
------+----------+------------+--------------------+---------------+-----------------+-------------+-------------------------------+--------------+-----------+-----------+-----------+-----------+------------+-----------------+-----------------+-----------------+---------------+------------+-------------------------------
 7084 |    16385 | barman     | barman_receive_wal | 192.168.57.13 |                 |       48028 | 2025-07-13 23:11:29.276196+03 |              | streaming | 0/4000060 | 0/4000060 | 0/4000000 |            | 00:00:09.370145 | 00:00:09.370145 | 00:00:20.012117 |             0 | async      | 2025-07-13 23:11:49.294849+03
 7085 |    16384 | replicator | walreceiver        | 192.168.57.12 |                 |       56508 | 2025-07-13 23:11:29.744704+03 |          735 | streaming | 0/4000060 | 0/4000060 | 0/4000060 | 0/4000060  |                 |                 |                 |             0 | async      | 2025-07-13 23:11:50.072243+03
(2 rows)


node2
pid  |  status   | receive_start_lsn | receive_start_tli | written_lsn | flushed_lsn | received_tli |      last_msg_send_time       |     last_msg_receipt_time     | latest_end_lsn |        latest_end_time        | slot_name |  sender_host  | sender_port |                                                                                                                                        conninfo                                                                                                                                         
------+-----------+-------------------+-------------------+-------------+-------------+--------------+-------------------------------+-------------------------------+----------------+-------------------------------+-----------+---------------+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 6961 | streaming | 0/3000000         |                 1 | 0/4000060   | 0/4000060   |            1 | 2025-07-13 23:12:09.977221+03 | 2025-07-13 23:12:09.976249+03 | 0/4000060      | 2025-07-13 23:11:39.929422+03 |           | 192.168.57.11 |        5432 | user=replicator password=******** channel_binding=prefer dbname=replication host=192.168.57.11 port=5432 fallback_application_name=walreceiver sslmode=prefer sslcompression=0 sslsni=1 ssl_min_protocol_version=TLSv1.2 gssencmode=prefer krbsrvname=postgres target_session_attrs=any
```

настроить правильное резервное копирование
```
