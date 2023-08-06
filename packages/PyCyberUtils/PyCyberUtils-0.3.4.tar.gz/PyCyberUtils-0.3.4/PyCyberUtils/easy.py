from bson.objectid import ObjectId
from requests.exceptions import ConnectionError
from contextlib import suppress
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pymongo.errors import ServerSelectionTimeoutError
import motor.motor_asyncio
import json
import logging
import coloredlogs
import inspect

from .exceptions import *
from .models import *


class CyberUtils(dict):

    def __init__(self, config: ModelConfig, log_level: int = logging.INFO):
        config = jsonable_encoder(config)
        self.__load_config__(config)

        self.app_name = config.get('app_name')
        self.app_token = config.get('app_token')

        logging.basicConfig(level=log_level,
                            format='%(asctime)s | %(levelname)s | %(message)s')
        self.__logger__ = logging.getLogger(__name__)
        coloredlogs.install(level=logging.getLevelName(log_level), logger=self.__logger__)

        if logger_conf := config.get('logger', {}):
            logger_conf.update(dict(name="logger"))
            self.logger = CyberLogger(ModelLogger(**logger_conf), self)
            config['services'].append(logger_conf)

        if services_conf := config.get('services', []):
            self.caller = CyberCaller(ModelServicesList(**dict(services=services_conf)), self)

        if db_conf := config.get('database', {}):
            self.db = CyberDB(ModelDatabase(**db_conf), self)

        super().__init__()

    def __load_config__(self, config: dict):
        self.app_name = config.get('app_name', None)
        if not self.app_name:
            raise CyberUtilConfigMissing("Application name missing")
        self.app_token = config.get('app_token', None)
        if not self.app_token:
            raise CyberUtilConfigMissing("Application token missing")

    def __prepare_log__(self, message: object, status_code: int = None, method: str = None, log_server: bool = False, stack=None):
        the_class = send_content = None
        with suppress(KeyError):
            the_class = stack[1][0].f_locals["self"].__class__.__name__
            info = inspect.getframeinfo(stack[1][0])
            the_method = info.function
        method_caller = f'{self.app_name} | {f"(Line: {info.lineno}) " if the_class else ""}{the_class}.{the_method}()' if the_class and the_method else self.app_name
        status_code = f"{' | ' if method_caller else ''}{status_code}" if status_code else ''
        method_type = f"{' | ' if status_code or method_caller else ''}{method.upper()}" if method else ''
        msg_content = f"{' | ' if status_code or method_caller else ''}{message}" if isinstance(message, str) else ''
        if isinstance(message, dict):
            msg_final = f"{method_caller}{status_code}{method_type}"
            is_json = True
        else:
            msg_final = f"{method_caller}{status_code}{method_type}{msg_content}"
            is_json = False
        if hasattr(self, "caller") and log_server:
            send_content = dict(app_name=self.app_name, content=msg_content,
                                logtime=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            if the_class and the_method:
                send_content.update(dict(caller=f"{the_class}.{the_method}()"))
            if status_code:
                send_content.update(dict(status_code=status_code))
            if method_type:
                send_content.update(dict(method_type=method_type))
        return msg_final, is_json, send_content

    def log(self, message: object, status_code: int = None, status_name: str = 'info', method: str = None, log_server=False):
        if not hasattr(logging, status_name):
            self.__logger__.error(f"CyberLogger does not support {status_name} status name")
            return
        msg_final, is_json, log_for_server = self.__prepare_log__(message, status_code, method, log_server, inspect.stack())
        getattr(self.__logger__, status_name)(msg_final)
        if is_json:
            print(json.dumps(message, ensure_ascii=False, indent=4))
        if hasattr(self, "logger") and any([self.logger.get("auto_log", False), log_server]) and log_for_server:
            self.caller.do('post', "logger", json_content=ModelLog(**log_for_server).__dict__)
        if not status_code:
            status_code = 200
        return dict(code=status_code, content=message)


class CyberModel(dict):

    def __init__(self, config: dict, utils: CyberUtils):
        self.log = utils.log
        self.update(config)
        super().__init__()


class CyberLogger(CyberModel):

    def __init__(self, config: ModelLogger, utils: CyberUtils):
        config = jsonable_encoder(config)
        super().__init__(config, utils)


class CyberCaller(CyberModel):

    def __init__(self, config: ModelServicesList, utils: CyberUtils):
        config = jsonable_encoder(config)
        super().__init__(config, utils)
        self.headers = {
            'User-Agent': f"PyCyberUtils 0.0.1",
            'Cyber-Service-Name': utils.app_name,
            'Cyber-Service-Token': utils.app_token
        }

    def __get_service__(self, service_name):
        if not isinstance(service_name, str):
            service_name = jsonable_encoder(service_name)
        for service in self.get('services', {}):
            if service.get('name', '') == service_name:
                return dict(enabled=True, url=service.get('url', ''))
        self.log(f"{service_name} not defined in the configuration", status_code=500, status_name='error', log_server=False)
        return dict(enabled=False, url='')

    def do(self, method: str, service: object, api: str = '', data: object = {}, json_content: dict = {},
           params: dict = {}, files: dict = None, headers: dict = None, timeout: int = 3, log_server=False):
        if method.lower() == 'post':
            from requests import post as caller
        else:
            from requests import get as caller
        if not api and isinstance(data, str):
            api = f"/{data}"
            data = dict()
        conf = self.__get_service__(service)
        if not headers:
            headers = {}
        new_headers = self.headers | headers
        if conf.get('enabled', True):
            if url := conf.get('url', '').removesuffix('/'):
                try:
                    data.update(conf.get('data', {}))
                    json_content.update(conf.get('json', {}))
                    params.update(conf.get('params', {}))
                    if result := caller(url=f"{url}{api}", data=data, json=json_content, files=files,
                                        params=params, headers=new_headers,
                                        timeout=timeout):
                        if conf.get('type', '') == 'json':
                            return self.log(result.json(), result.status_code, log_server=log_server)
                        return self.log(result.content.decode('cp1252'), result.status_code, log_server=log_server)
                    return self.log(dict(error="No response from endpoint"), status_code=0, status_name='error', log_server=log_server)
                except ConnectionError as e:
                    return self.log(dict(error=str(e)), status_code=0, status_name='error', log_server=log_server)
            raise CyberCallerConfigMissing(f"Missing endpoint for service {service}")


class CyberDB(CyberModel):

    def __init__(self, config: ModelDatabase, utils: CyberUtils):
        config = jsonable_encoder(config)
        self.__load_config__(config)
        mongo_uri = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}?authSource=admin'
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        super().__init__(config, utils)

    def __load_config__(self, config: dict):
        self.user = config.get('user')
        self.password = config.get('password')
        self.host = config.get('host')
        self.port = config.get('port')
        self.db_name = config.get('db_name')

    def collection(self, collection_name: str):
        with suppress(ServerSelectionTimeoutError):
            self.log(f"Recogemos coleccion {collection_name}", log_server=False)
            return getattr(self.client, self.db_name).get_collection(collection_name)
        raise DatabaseConnectionError("Could not connect to MongoDB")

    @staticmethod
    def parse_helper(result: dict) -> dict:
        result['_id'] = str(result['_id'])
        return dict(result)

    async def retrieve_all(self,
                           collection_name: str,
                           query: dict = None,
                           filter_fields: dict = None) -> list:
        results = []
        async for result in self.collection(collection_name).find(
                query, filter_fields):
            print(result)
            results.append(self.parse_helper(result))
        return results

    async def retrieve_one(self, collection_name: str, id_obj: str) -> dict:
        result = await self.collection(collection_name).find_one(
            {"_id": ObjectId(id_obj)})
        if result:
            return self.parse_helper(result)

    async def insert(self, collection_name: str, data: dict) -> dict:
        result = await self.collection(collection_name).insert_one(data)
        new_result = await self.collection(collection_name).find_one(
            {"_id": result.inserted_id})
        return self.parse_helper(new_result)

    async def change(self, collection_name: str, id_obj: str,
                     data: dict) -> bool:
        if len(data) < 1:
            return False
        result = await self.collection(collection_name).find_one(
            {"_id": ObjectId(id_obj)})
        if result:
            updated_result = await self.collection(collection_name).update_one(
                {"_id": ObjectId(id_obj)}, data)
            if updated_result:
                return True
            return False

    async def delete(self, collection_name: str, id_obj: str) -> bool:
        result = await self.collection(collection_name).find_one(
            {"_id": ObjectId(id_obj)})
        if result:
            await self.collection(collection_name).delete_one(
                {"_id": ObjectId(id_obj)})
            return True
