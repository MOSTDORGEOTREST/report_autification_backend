import datetime
from fastapi import FastAPI, Response, Request
from starlette.middleware.cors import CORSMiddleware
from passlib.hash import bcrypt
from sqlalchemy.future import select
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from db.database import async_session
from db import tables
from db.database import Base, engine
from api import router
from config import configs
from db.tables import LicenseLevel

def create_ip_ports_array(ip: str, *ports):
    array = []
    for port in ports:
        array.append(f"{ip}:{str(port)}")
    return array

app = FastAPI(
    title="Georeport MDGT",
    description="Сервис аутентификации протоколов испытаний",
    version="2.0.0")


origins = []

origins += create_ip_ports_array(configs.host_ip, 3000, 8000, 80, 9573)
origins += create_ip_ports_array('http://localhost', 3000, 8000, 80, 9573)
origins += create_ip_ports_array('http://89.223.65.190', 3000, 8000, 80, 9573)
origins += create_ip_ports_array('http://37.139.85.41', 3000, 8000, 80, 9573)
origins += create_ip_ports_array("192.168.176.1", 3000, 8000, 80, 9573)

#@app.middleware("http")
#async def add_process_time_header(request: Request, call_next):
#    response = await call_next(request)
#    response.headers["httponly"] = 'true'
#    response.headers["secure"] = 'true'
#    response.headers["samesite"] = 'none'
#    return response

allow_methods = [
    "GET",
    "POST",
    "OPTIONS",
    "DELETE",
    "PATCH",
    "PUT"
]

allow_headers = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
    "Accept",
    "X-Requested-With"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

@app.middleware("http")
async def log_incoming_request(request: Request, call_next):
    headers = request.headers
    authorization_header = headers.get("Authorization")
    print(f"Incoming request headers: {headers}")
    print(f"Authorization header: {authorization_header}")
    response = await call_next(request)
    return response

app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def index():
    return JSONResponse(content={'massage': 'successful'}, status_code=200)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def create_surer():
        async with async_session() as session:
            async with session.begin():

                user_names = await session.execute(
                    select(tables.Users).
                    filter_by(username="mdgt_admin")
                )
                user_names = user_names.scalars().first()

                if not user_names:

                    try:
                        user = tables.Users(
                            username=configs.superuser_name,
                            password_hash=bcrypt.hash(configs.superuser_password),
                            mail="tnick1502@mail.ru",
                            organization="МОСТДОРГЕОТРЕСТ",
                            organization_url="https://mdgt.ru/",
                            phone=74956566910,
                            is_superuser=True,
                            active=True,
                            license_level=LicenseLevel.ENTERPRISE,
                            license_end_date=datetime.date(year=2030, month=12, day=31),
                            license_update_date=datetime.date.today(),
                            limit=1000000000
                        )

                        session.add(user)

                        user_trial = tables.Users(
                            username="trial",
                            password_hash=bcrypt.hash("trial"),
                            mail="nick.mdgt@mail.ru",
                            organization="МОСТДОРГЕОТРЕСТ",
                            organization_url="https://mdgt.ru/",
                            phone=70000000000,
                            is_superuser=False,
                            active=True,
                            license_level=LicenseLevel.STANDART,
                            license_end_date=datetime.date(year=2030, month=12, day=31),
                            license_update_date=datetime.date.today(),
                            limit=100
                        )

                        session.add(user_trial)

                        report = tables.Reports(
                            id="95465771a6f399bf52cd57db2cf640f8624fd868",
                            user_id=1,
                            datetime=datetime.datetime.now(),
                            laboratory_number="1",
                            test_type="Трехосное нагружение",
                            object_number="1",
                            data={
                                "Лабораторный номер": "Э1-1/-/ТС",
                                "Объект": "-",
                                "Даты выдачи протокола": "2022-04-26",
                                "Модуль деформации E, МПа:": 8.3,
                                "Модуль деформации E50, МПа": 7.7,
                                "Коэффициент поперечной деформации ν, д.е.": 0.41,
                                "Модуль повторного нагружения Eur, МПа:": 33.6,
                            },
                            active=True,
                        )
                        session.add(report)

                        for i in range(50):

                            import random

                            E = round(random.uniform(15, 50), 2)
                            c = round(random.uniform(0.001, 0.05), 3)
                            fi = round(random.uniform(25, 35), 2)

                            report = tables.Reports(
                                id=f"9546577{i}6f399bf52cd57db2cf640f8624fd868",
                                user_id=2,
                                datetime=datetime.date.today(),
                                object_number=random.choice(["112-54", "341-15", "294-41"]),
                                laboratory_number=f"1{i}",
                                test_type="Трехосное нагружение",
                                data={
                                    "Модуль деформации E50, МПа": E,
                                    "Эффективный угол внутреннего трения, град": fi,
                                    "Эффективное сцепление c, МПа": c,
                                },
                                active=True,
                            )
                            session.add(report)

                        await session.commit()
                        print("Создан суперпользователь")
                    except Exception as err:
                        print("Ошибка создания суперпользователя ", str(err))

    await create_surer()



