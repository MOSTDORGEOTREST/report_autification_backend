# Georeport backend

### Сервис для аутентификации протоколов лабораторных испытаний. 

#### Функционал:
* сервис данных пользователей
* сервис лицензий хранит данные лицензий и проверяет лицензию пользователя при отправке запросов пользователя
* сервис отчетов хранит данные по всем отчетам в базе

#### Стек:
* fastapi
* postgresql
* sqlalchemy
* s3

#### [Схема БД](https://dbdiagram.io/d/63088a2bf1a9b01b0feae726)

## Для разработки:
1. Скопировать файл .env в корень проекта
    
2. Создать папку для проекта. Открыть папку в терминале и выполнить:\
    `git init`\
    `git clone https://github.com/MOSTDORGEOTREST/report_autification_front.git`

3. Запуск через docker-compose:\
    `docker-compose -f docker-compose-dev.yml up`

4. Запуск тестов:\
    `docker-compose exec web pytest . -v`

## Деплой:
~/ = папка проекта 

1. Скопировать файл .env в ~/

2. Добавить конфигуратор nginx. Дефолтный конфигуратор nginx находится в ~/server/conf.d/app.conf (устанавливается автоматически в докер). Сертификат и ключ key.key и crt.crt должны находится в папке ~/*
    
3. Открыть папку ~/ в терминале и выполнить:\
    `git init`\
    `git clone https://github.com/MOSTDORGEOTREST/report_autification_front.git`

4. Запуск через docker-compose:\
    `docker-compose up --force-recreate -d --build`


Для очищения докера от проекта:\
    `docker rm $(docker ps -a -q) -f`\
    `docker rmi $(docker images -a -q) -f`


## Пример запроса:

```
data = {
    "object_number": "test",
    "laboratory_number": "test",
    "test_type": "test",
    "data": {
        "test": "test"
    },
    "active": True
}


def request_qr(data):
    with requests.Session() as sess:
        sess.post("https://georeport.ru/auth/sign-in/",
                  data={
                      "username": "trial",
                      "password": "trial",
                      "grant_type": "password",
                      "scope": "",
                      "client_id": "",
                      "client_secret": ""
                  },
                  verify=False, allow_redirects=False
                  )

        response = sess.post('https://georeport.ru/reports/report_and_qr', json=data)
        if not response.ok:
            return (False, response.json()['detail'])

        qr_path = f"{data['object_number']} {data['laboratory_number']} {data['test_type']}.png"

        with open(qr_path, "wb") as file:
            file.write(response.content)
        return (True, qr_path)```

