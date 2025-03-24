import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster

# Определяем путь к .env
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')

# Проверяем, существует ли файл .env
if not os.path.exists(env_path):
    print(f"⚠️  Файл .env не найден по пути: {env_path}")
else:
    load_dotenv(env_path)  # Загружаем переменные окружения

class ConnCassandra:

    @staticmethod
    def connection():
        try:
            # Получаем строку с хостами и преобразуем её в список
            cassandra_hosts = os.getenv("CASSANDRA_HOSTS")
            if cassandra_hosts:
                contact_points = cassandra_hosts.split(',')
            else:
                raise ValueError("CASSANDRA_HOSTS не задан в .env файле")

            cluster = Cluster(contact_points)

            # Пространство ключей сеанса
            session = cluster.connect("appeal")
            print("✅ Подключение к Cassandra успешно установлено!")
            return session
        except Exception as e:
            print(f"❌ Ошибка подключения к Cassandra: {e}")
            raise