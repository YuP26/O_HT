### **Otus - Administrator Linux. Professional.**  
#### **ДЗ №17 - Настраиваем центральный сервер для сбора логов.**  
**Цель** - Научится проектировать централизованный сбор логов и рассмотреть особенности разных платформ для сбора логов..

**Задание:**  
1) Настроить 2 центральных лог системы elk и rsyslog:
    В elk должны уходить только логи nginx;
    В rsyslog все остальное.
2) Все критичные логи  должны собираться и локально и удаленно
3) Настроить аудит, следящий за изменением конфигов nginx
4) Все логи с nginx должны уходить на удаленный сервер (локально только критичные).
5) Логи аудита должны также уходить на удаленную систему

****
#### **Описание реализации:**  
Сделано по примерам из: \
https://www.dmosk.ru/miniinstruktions.php?mini=rsyslog \
https://www.dmosk.ru/instruktions.php?object=elk-ubuntu#java\
Крайне отвратительный документ ниже пользы не принес (очень странно для уровня отуса): \
https://docs.google.com/document/d/16UBAMu4LYqvRv6PmCeHcmOampMrIZavH/edit?tab=t.0 \
Машины настраиваются через ansible, проверяются вручную. \ 
Стенд включает в себя 3 машины:
1) Веб-сервер nginx;
2) ELK-сервер для сбора всех логов;
3) Rsyslog-сервер для сбора всех остальных логов.
***
##### Подготовка стенда.
Параметры стенда:
```
VBox - generic/ubuntu2204 (версия generic/ubuntu2204)
ansible [core 2.16.3]
python version = 3.12.3
jinja version = 3.1.2
Vagrant 2.4.3
VirtualBox v.7.0.26 r168464
```
Вклчюаем сервер и проверяем статус машин:
```
vagrant up

vagrant status
Current machine states:

web                       running (virtualbox)
log-elk-nginx             running (virtualbox)
log-all                   running (virtualbox)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```
Запускаем ansible-playbook. Результат выполенния расположен в файле ansuble_result.txt:
```
ansible-playbook -i hosts rsyslog.yml
```

***
##### Проверка логов
Заходим на сервер log-all и проверяем наличие логов:
```
root@log-all:~# ls /var/log/rsyslog/
log-all

root@log-all:~# ls /var/log/rsyslog/log-all/
 CRON.log  '**INVALID PROPERTY NAME**'   rsyslogd.log   sshd.log   sudo.log   systemd.log   systemd-logind.log
