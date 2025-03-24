import jwt
import datetime
import asyncio

from app.protected.config.Config import ConnJwt


class CrudJwt:

    # Создание JWT токена
    @staticmethod
    async def create_token(user_id, company_id, is_admin, devices_id, ip, ua):

        if not ConnJwt.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY не найден в переменных окружения")

        payload = {
            'user_id': user_id,
            'company_id': company_id,
            'is_admin': is_admin,
            'device_id': devices_id,
            'ip': ip,
            'ua': ua,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }

        return await asyncio.to_thread(jwt.encode, payload, ConnJwt.JWT_SECRET_KEY, algorithm='HS256')


    # Асинхронная функция для декодирования токена
    @staticmethod
    async def decode_token(token):

        if not ConnJwt.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY не найден в переменных окружения")

        return await asyncio.to_thread(jwt.decode, token, ConnJwt.JWT_SECRET_KEY, algorithms=['HS256'])
