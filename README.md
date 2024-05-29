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

#### [Схема БД](https://dbdiagram.io/d/georeport-64edcb6a02bd1c4a5e99ec69)

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
~/root/projects/ = папка проекта 

1. Скопировать файл .env в ~/

2. Добавить конфигуратор nginx. Дефолтный конфигуратор nginx находится в ~/server/conf.d/app.conf (устанавливается автоматически в докер).
    
3. Открыть папку ~/ в терминале и выполнить:\
    `git init`\
    `git clone https://github.com/MOSTDORGEOTREST/report_autification_backend.git`

4. Запуск через docker-compose:\
    `docker-compose up --force-recreate -d --build`

Переразвертка через скрипт:\
    `cd /root/projects/report_autification_backend`\
    `bash script.sh`

Для очищения докера от проекта:\
    `docker rm $(docker ps -a -q) -f`\
    `docker rmi $(docker images -a -q) -f`


## Пример запроса:

```
import requests
import warnings
from typing import Optional
import json

warnings.filterwarnings('ignore')

url = ''   # 'https://georeport.ru'

access_token = None

username = ''
password = ''

def get_token():
    with requests.Session() as sess:
        reg = sess.post(f'{url}/auth/sign-in/',
                        data={
                            'username': username,
                            'password': password,
                            'grant_type': 'password',
                            'scope': '',
                            'client_id': '',
                            'client_secret': ''
                        }, verify=True, allow_redirects=True)

        response = sess.post(f'{url}/auth/token/')
        response_str = response.content.decode('utf-8')
        response_dict = json.loads(response_str)

        return response_dict['access_token']

def request_qr(
        object_number: Optional[str],
        laboratory_number: Optional[str],
        test_type: Optional[str],
        data: Optional[dict]
):
    report_data = {
        'object_number': object_number,
        'laboratory_number': laboratory_number,
        'test_type': test_type,
        'data': data,
        'active': True
    }

    try:
        global access_token

        access_token = get_token() if access_token is None else access_token

        response_report = requests.post(
            f'{url}/reports/',
            json=report_data,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        assert response_report.ok, 'Не удалось сохранить значения в базе'

        response_report_dict = json.loads(response_report.content.decode('utf-8'))

        response_qr = requests.post(
            f'{url}/reports/qr/?id={response_report_dict["id"]}',
            json=report_data,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        assert response_report.ok, 'Не удалось получить qr'

        with open('qr.png', 'wb') as file:
            file.write(response_qr.content)
        return 'qr.png'

    except Exception as err:
        assert True, f'Не удается подключиться к серверу georeport: {str(err)}'
```

developed by Tishin Nick
