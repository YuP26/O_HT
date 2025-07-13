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

настроить правильное резервное копирование\
проверяем статус и делаем бэкап
```
vagrant@barman:~$ sudo barman check node1
2025-07-13 20:33:26,788 [7727] barman.utils WARNING: Failed opening the requested log file. Using standard error instead.
Server node1:
	PostgreSQL: OK
	superuser or standard user with backup privileges: OK
	PostgreSQL streaming: OK
	wal_level: OK
	replication slot: OK
	directories: OK
	retention policy settings: OK
2025-07-13 20:33:26,880 [7727] barman.server ERROR: Check 'backup maximum age' failed for server 'node1'
	backup maximum age: FAILED (interval provided: 4 days, latest backup age: No available backups)
	backup minimum size: OK (0 B)
	wal maximum age: OK (no last_wal_maximum_age provided)
	wal size: OK (0 B)
	compression settings: OK
	failed backups: OK (there are 0 failed backups)
2025-07-13 20:33:26,881 [7727] barman.server ERROR: Check 'minimum redundancy requirements' failed for server 'node1'
	minimum redundancy requirements: FAILED (have 0 backups, expected at least 1)
	pg_basebackup: OK
	pg_basebackup compatible: OK
	pg_basebackup supports tablespaces mapping: OK
	systemid coherence: OK (no system Id stored on disk)
	pg_receivexlog: OK
	pg_receivexlog compatible: OK
	receive-wal running: OK
	archiver errors: OK
vagrant@barman:~$ sudo barman backup --wait node1
2025-07-13 20:36:47,882 [7766] barman.utils WARNING: Failed opening the requested log file. Using standard error instead.
Starting backup using postgres method for server node1 in /var/lib/barman/node1/base/20250713T203647
2025-07-13 20:36:47,981 [7766] barman.backup INFO: Starting backup using postgres method for server node1 in /var/lib/barman/node1/base/20250713T203647
Backup start at LSN: 0/9000100 (000000010000000000000009, 00000100)
2025-07-13 20:36:47,987 [7766] barman.backup_executor INFO: Backup start at LSN: 0/9000100 (000000010000000000000009, 00000100)
Starting backup copy via pg_basebackup for 20250713T203647
2025-07-13 20:36:47,988 [7766] barman.backup_executor INFO: Starting backup copy via pg_basebackup for 20250713T203647
WARNING: pg_basebackup does not copy the PostgreSQL configuration files that reside outside PGDATA. Please manually backup the following files:
	/etc/postgresql/14/main/postgresql.conf
	/etc/postgresql/14/main/pg_hba.conf
	/etc/postgresql/14/main/pg_ident.conf

2025-07-13 20:36:48,524 [7766] barman.backup_executor WARNING: pg_basebackup does not copy the PostgreSQL configuration files that reside outside PGDATA. Please manually backup the following files:
	/etc/postgresql/14/main/postgresql.conf
	/etc/postgresql/14/main/pg_hba.conf
	/etc/postgresql/14/main/pg_ident.conf

Copy done (time: less than one second)
2025-07-13 20:36:48,525 [7766] barman.backup_executor INFO: Copy done (time: less than one second)
Finalising the backup.
2025-07-13 20:36:48,526 [7766] barman.backup_executor INFO: Finalising the backup.
2025-07-13 20:36:48,546 [7766] barman.postgres INFO: Restore point 'barman_20250713T203647' successfully created
Backup size: 33.6 MiB
2025-07-13 20:36:48,553 [7766] barman.backup INFO: Backup size: 33.6 MiB
Backup end at LSN: 0/B000000 (00000001000000000000000A, 00000000)
2025-07-13 20:36:48,554 [7766] barman.backup INFO: Backup end at LSN: 0/B000000 (00000001000000000000000A, 00000000)
Backup completed (start time: 2025-07-13 20:36:47.988924, elapsed time: less than one second)
2025-07-13 20:36:48,554 [7766] barman.backup INFO: Backup completed (start time: 2025-07-13 20:36:47.988924, elapsed time: less than one second)
Waiting for the WAL file 00000001000000000000000A from server 'node1'
2025-07-13 20:36:48,555 [7766] barman.server INFO: Waiting for the WAL file 00000001000000000000000A from server 'node1'
2025-07-13 20:36:48,555 [7766] barman.wal_archiver INFO: Found 1 xlog segments from streaming for node1. Archive all segments in one run.
Processing xlog segments from streaming for node1
	000000010000000000000009
2025-07-13 20:36:48,556 [7766] barman.wal_archiver INFO: Archiving segment 1 of 1 from streaming: node1/000000010000000000000009
2025-07-13 20:36:48,724 [7766] barman.wal_archiver INFO: Found 1 xlog segments from streaming for node1. Archive all segments in one run.
Processing xlog segments from streaming for node1
	00000001000000000000000A
2025-07-13 20:36:48,725 [7766] barman.wal_archiver INFO: Archiving segment 1 of 1 from streaming: node1/00000001000000000000000A
2025-07-13 20:36:48,799 [7766] barman.wal_archiver INFO: No xlog segments found from streaming for node1.
```
удаляем бд и восстанавливаем из бэкапа
```
postgres=# DROP DATABASE otus_test;
DROP DATABASE
postgres=# \l
                              List of databases
   Name    |  Owner   | Encoding | Collate |  Ctype  |   Access privileges   
-----------+----------+----------+---------+---------+-----------------------
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
(3 rows)

vagrant@barman:~$ sudo barman recover node1 20250713T203347 /var/lib/postgresql/14/main/ --remote-ssh-comman "ssh postgres@192.168.57.11"
2025-07-13 20:38:58,907 [7793] barman.utils WARNING: Failed opening the requested log file. Using standard error instead.
2025-07-13 20:38:58,916 [7793] barman.wal_archiver INFO: No xlog segments found from streaming for node1.
The authenticity of host '192.168.57.11 (192.168.57.11)' can't be established.
ED25519 key fingerprint is SHA256:eFm0/+2mE6WoNG5FP9S9sGvwuSZsUNIGfHIGAoaBcWE.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Starting remote restore for server node1 using backup 20250713T203347
2025-07-13 20:39:01,451 [7793] barman.recovery_executor INFO: Starting remote restore for server node1 using backup 20250713T203347
Destination directory: /var/lib/postgresql/14/main/
2025-07-13 20:39:01,452 [7793] barman.recovery_executor INFO: Destination directory: /var/lib/postgresql/14/main/
Remote command: ssh postgres@192.168.57.11
2025-07-13 20:39:01,452 [7793] barman.recovery_executor INFO: Remote command: ssh postgres@192.168.57.11
2025-07-13 20:39:01,651 [7793] barman.recovery_executor WARNING: Unable to retrieve safe horizon time for smart rsync copy: The /var/lib/postgresql/14/main/.barman-recover.info file does not exist
Copying the base backup.
2025-07-13 20:39:02,062 [7793] barman.recovery_executor INFO: Copying the base backup.
2025-07-13 20:39:02,065 [7793] barman.copy_controller INFO: Copy started (safe before None)
2025-07-13 20:39:02,066 [7793] barman.copy_controller INFO: Copy step 1 of 4: [global] analyze PGDATA directory: /var/lib/barman/node1/base/20250713T203347/data/
2025-07-13 20:39:02,448 [7793] barman.copy_controller INFO: Copy step 2 of 4: [global] create destination directories and delete unknown files for PGDATA directory: /var/lib/barman/node1/base/20250713T203347/data/
2025-07-13 20:39:02,738 [7814] barman.copy_controller INFO: Copy step 3 of 4: [bucket 0] starting copy safe files from PGDATA directory: /var/lib/barman/node1/base/20250713T203347/data/
2025-07-13 20:39:03,130 [7814] barman.copy_controller INFO: Copy step 3 of 4: [bucket 0] finished (duration: less than one second) copy safe files from PGDATA directory: /var/lib/barman/node1/base/20250713T203347/data/
2025-07-13 20:39:03,150 [7814] barman.copy_controller INFO: Copy step 4 of 4: [bucket 0] starting copy files with checksum from PGDATA directory: /var/lib/barman/node1/base/20250713T203347/data/
2025-07-13 20:39:03,396 [7814] barman.copy_controller INFO: Copy step 4 of 4: [bucket 0] finished (duration: less than one second) copy files with checksum from PGDATA directory: /var/lib/barman/node1/base/20250713T203347/data/
2025-07-13 20:39:03,410 [7793] barman.copy_controller INFO: Copy finished (safe before None)
Copying required WAL segments.
2025-07-13 20:39:03,653 [7793] barman.recovery_executor INFO: Copying required WAL segments.
2025-07-13 20:39:03,656 [7793] barman.recovery_executor INFO: Starting copy of 3 WAL files 3/3 from WalFileInfo(compression='gzip', name='000000010000000000000008', size=16460, time=1752438828.115622) to WalFileInfo(compression='gzip', name='00000001000000000000000A', size=16463, time=1752439008.3121965)
2025-07-13 20:39:04,396 [7793] barman.recovery_executor INFO: Finished copying 3 WAL files.
Generating archive status files
2025-07-13 20:39:04,397 [7793] barman.recovery_executor INFO: Generating archive status files
Identify dangerous settings in destination directory.
2025-07-13 20:39:05,015 [7793] barman.recovery_executor INFO: Identify dangerous settings in destination directory.

WARNING
The following configuration files have not been saved during backup, hence they have not been restored.
You need to manually restore them in order to start the recovered PostgreSQL instance:

    postgresql.conf
    pg_hba.conf
    pg_ident.conf

Recovery completed (start time: 2025-07-13 20:38:58.917548, elapsed time: 6 seconds)

Your PostgreSQL server has been successfully prepared for recovery!
```
перезапускаем сервис и првоеряем восстановление
```
postgres=# \l
WARNING:  terminating connection due to immediate shutdown command
server closed the connection unexpectedly
	This probably means the server terminated abnormally
	before or while processing the request.
The connection to the server was lost. Attempting reset: Failed.

vagrant@node1:~$ sudo systemctl restart postgresql
vagrant@node1:~$ sudo -u postgres psql
could not change directory to "/home/vagrant": Permission denied
psql (14.18 (Ubuntu 14.18-0ubuntu0.22.04.1))
Type "help" for help.

postgres=# \l
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

postgres=# 
```
