from pydantic import BaseSettings, Field
import os
from dotenv import load_dotenv
import http.client

load_dotenv(dotenv_path=os.path.normpath(".env"))

def get_self_public_ip():
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode()

class Configs_docker_compose(BaseSettings):
    host_ip: str = get_self_public_ip()
    database_url: str = Field(..., env='DATABASE_URL')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')
    jwt_expiration: int = Field(..., env='JWT_EXPIRATION')
    superuser_name: str = Field(..., env='SUPERUSER_NAME')
    superuser_password: str = Field(..., env='SUPERUSER_PASSWORD')
    endpoint_url: str = Field(..., env='AWS_URI')
    aws_access_key_id: str = Field(..., env='AWS_ACCCESS_KEY')
    service_name: str = Field(..., env='AWS_SERVICE_NAME')
    aws_secret_access_key: str = Field(..., env='AWS_SECRET_KEY')
    region_name: str = Field(..., env='AWS_REGION')
    bucket: str = Field(..., env='AWS_BUCKET')
    file_count: int = Field(..., env='FILE_COUNT')
    file_size: str = Field(..., env='FILE_SIZE')

configs = Configs_docker_compose()
