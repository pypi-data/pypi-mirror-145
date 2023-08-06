import json
from typing import ClassVar, AnyStr, ByteString, Union, Dict, Any, List
from urllib.parse import urlparse

import redis
from utils import encode_string


class RedisConnection:
    host: str
    port: int
    db: int
    username: str
    password: str
    pool: redis.ConnectionPool
    conn: redis.StrictRedis
    uri: str

    def __init__(
        self, host: str, port: int, db: int, username: str, password: str, con_uri: str
    ):
        RedisConnection.host = host
        RedisConnection.port = port
        RedisConnection.db = db
        RedisConnection.username = username
        RedisConnection.password = password
        RedisConnection.con_uri = con_uri
        RedisConnection.pool = redis.ConnectionPool(
            host=RedisConnection.host,
            port=RedisConnection.port,
            db=RedisConnection.db,
            username=RedisConnection.username,
            password=RedisConnection.password,
        )
        RedisConnection.conn = redis.StrictRedis(connection_pool=RedisConnection.pool)

    @property
    def get_host(self) -> str:
        """Get current host
        :return: string host
        """
        return RedisConnection.host

    @property
    def get_port(self) -> int:
        """Get current port redis
        :return: int port
        """
        return RedisConnection.port

    @staticmethod
    def set_db(
        db: int,
    ) -> bool:
        """Set redis db selected
        :param db: int db eg: 0, 1, 2, 3, 4, 5 ...
        :return: none
        """
        RedisConnection.db = db
        return True

    @property
    def get_db(self) -> int:
        """Get current db selected
        :return: int db selected
        """
        return RedisConnection.db

    @property
    def get_username(self) -> str:
        """Get current username
        :return: string username
        """
        return RedisConnection.username

    @property
    def get_password(self) -> str:
        """Get current password
        :return: string password
        """
        return RedisConnection.password

    @property
    def get_credential(self) -> Dict[str, Any]:
        """Get current credential to connect to redis
        :return: dictionary value
        """
        return {
            "host": RedisConnection.host,
            "port": RedisConnection.port,
            "db": RedisConnection.db,
            "username": RedisConnection.username,
            "password": RedisConnection.password,
        }

    def __str__(self):
        return "RedisConnection({}, {}, {}, {}, {})".format(
            RedisConnection.host,
            RedisConnection.port,
            RedisConnection.db,
            RedisConnection.username,
            RedisConnection.password,
        )

    @classmethod
    def from_uri(cls, uri: str) -> ClassVar:
        """Create object connection class from uri
        this will receive uri like this:
            redis://example:secret@localhost:6379/0
        :param uri: string redis uri
        :return: class object
        """
        p = urlparse(uri)
        return cls(p.hostname, p.port, int(p.path[1:]), p.username, p.password, uri)

    @staticmethod
    def generate_sequence_number(key: str) -> str:
        """Generate sequence number based on specified key
            example:
                1 -> will return as 000001
                2 -> will return as 000002
        :param key: string key name
        :return: string sequence number
        """
        last_sequence = RedisConnection.get(key)
        if last_sequence is None:
            init_number = 1
            RedisConnection.set(key, init_number, ttl=0)
            return str(init_number).zfill(10)

        RedisConnection.incr(key)
        seq = RedisConnection.get(key)
        return str(seq).zfill(10)

    @staticmethod
    def get(key: str) -> Union[ByteString, AnyStr, int, float, None]:
        """Get value from specified key
        :param key: string key
        :return: it can be string bytes string, int or float
        """
        hash_key = encode_string(key)
        v = RedisConnection.conn.get(hash_key)
        # if any value from it then decode to utf 8, cause default data type is bytes
        if v is not None and len(v) > 0:
            return v.decode("utf-8")

        return None

    @staticmethod
    def keys(
        key: str,
    ) -> Union[List[Dict[str, Any]], List[str], List[float], List[int]]:
        """Get data from redis for specified keys
        :param key: string key
        :return: boolean (true, false)
        """
        tmp = []
        for k in RedisConnection.conn.keys(key):
            if k is not None and len(k) > 0:
                tmp.append(
                    json.loads(
                        RedisConnection.conn.get(k.decode("utf-8")).decode("utf-8")
                    )
                )
        return tmp

    @staticmethod
    def get_plain_key(key: str) -> Union[ByteString, AnyStr, int, float, None]:
        """Get value from specified key
        :param key: string key
        :return: it can be string bytes string, int or float
        """
        v = RedisConnection.conn.get(key)
        # if any value from it then decode to utf 8, cause default data type is bytes
        if v is not None and len(v) > 0:
            return v.decode("utf-8")

        return None

    @staticmethod
    def set_plain_key(
        key: str,
        value: Union[ByteString, AnyStr, int, float],
        ttl: int = 60 * 10,
    ) -> bool:
        """Save data to redis by specified keys
        :param key: string key
        :param value: it can be bytes string, string, int or float
        :param ttl: default value for time to live
        :return: boolean (true, false)
        """
        if ttl == 0:
            return RedisConnection.conn.set(key, value)

        return RedisConnection.conn.set(key, value, ex=ttl)

    @staticmethod
    def set(
        key: str,
        value: Union[ByteString, AnyStr, int, float],
        ttl: int = 60 * 10,
    ) -> bool:
        """Save data to redis by specified keys
        :param key: string key
        :param value: it can be bytes string, string, int or float
        :param ttl: default value for time to live
        :return: boolean (true, false)
        """
        hash_key = encode_string(key)
        if ttl == 0:
            return RedisConnection.conn.set(hash_key, value)

        return RedisConnection.conn.set(hash_key, value, ex=ttl)

    @staticmethod
    def incr(
        key: str,
    ) -> bool:
        """Increment value in specified keys
        :param key: string key
        :return: boolean (true, false)
        """
        hash_key = encode_string(key)
        return RedisConnection.conn.incr(hash_key)
