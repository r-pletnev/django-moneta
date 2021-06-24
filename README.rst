django-moneta
=============
Приложение для интеграции платежной системы PayAnyWay(Moneta) в проекты работающие на Django
Работают только методы непосредственно связанные с оплатой.

***Внимание:*** Для корректного функционирования приложения **Check URL** в настройках магазина в админке PayAnyWay должен быть указан!


Спецификация: https://demo.moneta.ru/doc/MONETA.Assistant.ru.pdf

## Установка ##
```sh
pip install django-moneta
```

Запустить миграцию в корне проекта:
```sh
python ./manage.py migrate moneta
```



settings.py:
```python
INSTALLED_APPS = [
    ...,
    moneta
]

MONETA = {
    "basic_config": {
        "account_id": 123,
        "account_username": "test",
        "account_password": "123",
        "payment_system_name": "plastic",
        "currency": "RUB",
        "account_code": "secret",
    }

LOGGING = {
    ...
    'loggers': {
      "moneta-log": {
        "handlers": ["console"],
            "level": "DEBUG",
      }
    },
}
```

## Настройки ##
**Основные**
Основные настройки хранятся в словаре *basic_config*:
Идентификатор магазина в системе PayAnyWay
```python
account_id: 123
```

Имя пользователя в системе PayAnyWay
```python
account_username: "username"
```
Пароль пользователя в системе PayAnyWay
```python
account_password: "password"
```
Код для формирования подписи
```python
account_code: "secret"
```
В настройках можно указать и другие параметры из спецификации, например валюту, по-умолчанию Российский рубль, и систему платежа, по-умолчанию: пластиковая карточка. Полное описание настроек есть в спецификации.

## Сигналы ##
**`signals.invoice_checking`**
Сигнал посылается после создания инвойса в базе данных.
**`signals.invoice_paid`**
Сигнал посылается после оплаты пользователем.


Для поиска пользователя можно использовать `subscriber_id` у документа invoice.

## Маршруты ##

Маршруты по-умолчанию:
**check_notification** - служебный маршрут, платежный сервис отправлется проверочный запрос на него
**paid_notification** - служебный маршрут, платежный сервис отправялет запрос об успешном платеже на этот путь
**init_pay** - простая форма оплаты
**api_init_pay** - формирование url для оплаты отдельным http запросом
**success** - используется после успешной оплаты
**fail** - используется после неудачной оплаты
