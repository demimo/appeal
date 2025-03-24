from datetime import timedelta


from app.protected.config.Config import ConnRedis


class CrudRedis:

    # Функция для записи данных в Redis
    @staticmethod
    async def set(user_id: int, device_id: str, ip: str, ua: str, token: str):
        conn = None
        try:
            # Подключаемся к Redis
            conn = await ConnRedis.connection()

            # Формируем ключ и значение
            key = f"sessions:{user_id}:{device_id}"
            value = {'device_id': device_id, 'ip': ip, 'ua': ua, 'token': token}

            # Записываем в Redis
            await conn.hset(key, mapping=value)

            # Устанавливаем TTL (7 дней)
            ttl_seconds = int(timedelta(days=7).total_seconds())
            await conn.expire(key, ttl_seconds)

            return True

        except Exception as e:
            print(f"Error: {e}")
            return None


    # Функция для получения конкретной записи пользователя
    @staticmethod
    async def get(user_id: int, device_id: str):
        try:
            # Подключаемся к Redis
            conn = await ConnRedis.connection()

            # Формируем ключ
            key = f"sessions:{user_id}:{device_id}"

            # Получаем значение по ключу
            value = await conn.hget(key, 'token')

            # Если значение найдено, декодируем его из bytes в строку
            if value is not None:
                return value.decode('utf-8')  # Преобразуем байты в строку
            else:
                return None  # Если значение не найдено, возвращаем None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
        

    # Удаление конкретной записи
    @staticmethod
    async def delete(user_id: int, device_id: str):
        try:
            # Подключаемся к Redis
            conn = await ConnRedis.connection()

            # Формируем ключ
            key = f"sessions:{user_id}:{device_id}"

            # Удаляем только конкретный токен
            deleted = await conn.delete(key)

            return deleted

        except Exception as e:
            print(f"Error: {e}")
            return None


    
    # Получение всех устройств
    @staticmethod
    async def getAll(user_id: int):

        try:
            # Подключаемся к Redis
            conn = await ConnRedis.connection()

            # Шаблон поиска
            pattern = f"sessions:{user_id}:*"

            cursor = b"0"
            sessions = []

            while cursor:
                cursor, keys = await conn.scan(cursor=cursor, match=pattern, count=100)
                for key in keys:
                    # Получаем всю хеш-таблицу
                    data = await conn.hgetall(key)
                    if data:
                        sessions.append({
                            "ip": data.get(b"ip").decode("utf-8") if b"ip" in data else None,
                            "ua": data.get(b"ua").decode("utf-8") if b"ua" in data else None
                        })
                        
            # Возвращаем список словарей с IP и UA
            return sessions

        except Exception as e:
            print(f"Error: {e}")
            return None
        



    # # Функция для получения всех данных пользователя
    # async def getAll(user_id: int):
    #     try:
    #         # Подключаемся к Redis
    #         conn = await ConnRedis.connection()

    #         # Получаем данные
    #         value = await conn.hget(f"user_tokens:{user_id}")

    #         if value is None:
    #             print(f"Ключ {user_id} отсутствует в Redis")
    #             return None

    #         return value.decode("utf-8")  # Преобразуем из байтов в строку
        
    #     except redis.exceptions.RedisError as e:
    #         print(f"Ошибка Redis при чтении ключа {user_id}: {e}")
    #     except Exception as e:
    #         print(f"Неизвестная ошибка при чтении из Redis: {e}")
    #     return None  # Возвращаем None в случае ошибки




    # # Удаление конкретной записи
    # async def delete(user_id: int, token: str):
    #     try:
    #         # Подключаемся к Redis
    #         conn = await ConnRedis.connection()

    #         # Удаляем только конкретный токен
    #         await conn.hdel(f"user_tokens:{user_id}", "device", token)

    #         return True

    #     except redis.exceptions.RedisError as e:
    #         print(f"Ошибка Redis при удалении токена пользователя:{user_id}: {e}")
    #     return False




    # # Удаление всех записей пользователя
    # async def deleteAll(user_id: int):
    #     try:
    #         # Подключаемся к Redis
    #         conn = await ConnRedis.connection()

    #         # Удаляем все токены пользователя
    #         await conn.hgetall(f"user_tokens:{user_id}")

    #         return True

    #     except redis.exceptions.RedisError as e:
    #         print(f"Ошибка Redis при удалении всех токенов пользователя:{user_id}: {e}")
    #     return False



# Загрузка переменных окружения из .env файла
# load_dotenv("../.env")

# Получение переменных окружения
# REDIS_HOST = os.getenv('REDIS_HOST')
# REDIS_PORT = os.getenv('REDIS_PORT')
# REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
# REDIS_DB = os.getenv('REDIS_DB')

# async def main():
#     # Подключение к Redis
#     r = redis.Redis(
#         host=REDIS_HOST,
#         port=REDIS_PORT,
#         db=REDIS_DB,
#         password=REDIS_PASSWORD
#     )

#     # Записываем данные с ключем 'foo'
#     await r.set('foo', 'bar')

#     # Получаем значение ключа 'foo'
#     value = await r.get('foo')
#     print(value)


# asyncio.run(main())