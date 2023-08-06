from typing import Optional
from pydantic import BaseModel, Field


class ModelDatabase(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    db_name: str = Field(...)
    host: str = Field(...)
    port: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user": "admin",
                "password": "SuperSecretPassword123!",
                "db_name": "my_test_db",
                "host": "127.0.0.1",
                "port": 27017
            }
        }


class ModelServices(BaseModel):
    name: str = Field(...)
    url: str = Field(...)
    type: Optional[str]
    enabled: Optional[bool]
    params: Optional[dict]
    data: Optional[dict]
    headers: Optional[dict]

    class Config:
        schema_extra = {
            "example": {
                "name": "GeoIP",
                "url": "http://api.ipstack.com",
                "type": "json",
                "enabled": True,
                "headers": {
                    "Api-Token": "sjdfbisabdh"
                },
                "params": {
                    "access_token": "abcdabcd"
                },
                "data": {
                    "field_username": "my_user"
                }
            }
        }


class ModelServicesList(BaseModel):
    services: list[ModelServices]

    class Config:
        schema_extra = {
            "example": {
                "services": [
                    {
                        "name": "GeoIP",
                        "url": "http://api.ipstack.com",
                        "type": "json",
                        "params": {
                            "access_token": "abcdabcd"
                        },
                        "enabled": True
                    }
                ]
            }
        }


class ModelLogger(BaseModel):
    url: str = Field(...)
    auto_log: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "url": "http://127.0.0.1:6677",
                "auto_log": True
            }
        }


class ModelLog(BaseModel):
    app_name: str = Field(...)
    content: object = Field(...)
    caller: Optional[str]
    status_code: Optional[int]
    method_type: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "app_name": "MyAppName",
                "content": "Exception on line 15",
                "caller": "MyAppName.MyFunction()",
                "status_code": 500,
                "method_type": "post"
            }
        }


class ModelConfig(BaseModel):
    app_name: str = Field(...)
    app_token: str = Field(...)
    logger: Optional[ModelLogger]
    database: Optional[ModelDatabase]
    services: Optional[list[ModelServices]]

    class Config:
        schema_extra = {
            "example": {
                "app_name": "MyAppName",
                "app_token": "MyAccessToken",
                "logger": "http://127.0.0.1:6677",
                "database": {
                    "user": "admin",
                    "password": "SuperSecretPassword123!",
                    "db_name": "my_test_db",
                    "host": "127.0.0.1",
                    "port": 27017
                },
                "services": [{
                    "Google": {
                        "url": "https://google.com",
                        "type": "html",
                        "enabled": False
                    }
                },{
                    "GeoIP": {
                        "url": "http://api.ipstack.com",
                        "type": "json",
                        "params": {
                            "access_key": "MyAPIKey"
                        },
                        "enabled": True
                    }
                }]
            }
        }
