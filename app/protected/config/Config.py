import asyncpg
import os
from dotenv import load_dotenv
import redis.asyncio as redis
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Определяем путь к .env
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')

# Проверяем, существует ли файл .env
if not os.path.exists(env_path):
    print(f"⚠️  Файл .env не найден по пути: {env_path}")
else:
    load_dotenv(env_path)  # Загружаем переменные окружения


class ConnPostgresql:
    
    # Получение переменных окружения (атрибуты класса)
    POSTGRES_USER_1_USER = os.getenv("POSTGRES_USER_1_USER")
    POSTGRES_USER_1_PASSWORD = os.getenv("POSTGRES_USER_1_PASSWORD")
    POSTGRES_USER_1_DB_NAME = os.getenv("POSTGRES_USER_1_DB_NAME")
    POSTGRES_USER_1_HOST = os.getenv("POSTGRES_USER_1_HOST")
    POSTGRES_USER_1_PORT = os.getenv("POSTGRES_USER_1_PORT")

    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        # Подключение к базе данных
        self.conn = await asyncpg.connect(
            user=self.POSTGRES_USER_1_USER,
            password=self.POSTGRES_USER_1_PASSWORD,
            database=self.POSTGRES_USER_1_DB_NAME,
            host=self.POSTGRES_USER_1_HOST,
            port=self.POSTGRES_USER_1_PORT
        )
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        # Закрытие соединения с базой данных
        if self.conn:
            await self.conn.close()


class ConnRedis:

    # Получение переменных окружения (атрибуты класса)
    REDIS_AUTH_1_HOST = os.getenv('REDIS_AUTH_1_HOST')
    REDIS_AUTH_1_PORT = os.getenv('REDIS_AUTH_1_PORT')
    REDIS_AUTH_1_DB = os.getenv('REDIS_AUTH_1_DB')
    REDIS_AUTH_1_PASSWORD = os.getenv('REDIS_AUTH_1_PASSWORD')

    # Подключение к базе данных
    @staticmethod
    async def connection():
        try:
            conn = redis.Redis(
                host=ConnRedis.REDIS_AUTH_1_HOST,
                port=ConnRedis.REDIS_AUTH_1_PORT,
                db=ConnRedis.REDIS_AUTH_1_DB,
                password=ConnRedis.REDIS_AUTH_1_PASSWORD
            )
            
            # Проверка соединения
            if not conn:
                print("Ошибка: не удалось установить соединение с Redis")
                return False
            
            # Проверка, что соединение действительно работает
            await conn.ping()
            return conn
        
        except Exception as e:
            print(f"Ошибка при подключении к Redis: {e}")
            return False


class ConnJwt:

    # Получение переменных окружения
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # Проверяем корректность подключения
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY не найден в переменных окружения")
    




class ConnCassandra:

    # Получение переменных окружения
    CASSANDRA_HOSTS = os.getenv("CASSANDRA_HOSTS")
    CASSANDRA_PORT = os.getenv("CASSANDRA_PORT")
    CASSANDRA_USER = os.getenv("CASSANDRA_USER")
    CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD")

    # Подключение к Cassandra
    @staticmethod
    async def connection():
        cluster = Cluster(
            contact_points=ConnCassandra.CASSANDRA_HOSTS.split(","),
            port=int(ConnCassandra.CASSANDRA_PORT),
            auth_provider=PlainTextAuthProvider(
                username=ConnCassandra.CASSANDRA_USER,
                password=ConnCassandra.CASSANDRA_PASSWORD
            )
        )
        return cluster.connect()