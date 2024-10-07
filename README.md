# Телеграм бот для НРИ Киберпанка

Данный бот создан для помощи игрокам и ГМу в организации и проведении игр по НРИ.

## Конфигурация 
*Пример конфигурация yaml файла*

```yaml
token: TOKEN
database: 
  type: postgresql+psycopg2
  user: postgres
  password: postgres
  host: localhost
  port: 5432
  echo: false # вывод отладочной информации
```

## Установка
* клонируйте репозиторий
* создайте файл `config.yaml` на основе `config_example.yaml`
* запустите `poetry install` 
* запустите `poetry run python -m pager`

## Использование
* добавьте бота в чат
* или начните с команды `/start`

