from fastapi import Request, Response
import uuid


from app.protected.crud.CrudPostgresql import CrudPostgresql
from app.protected.crud.CrudJwt import CrudJwt
from app.protected.crud.CrudRedis import CrudRedis


class Registration:

    @staticmethod
    async def registration(request: Request, response: Response):

        # Получаем JSON-данные из тела запроса
        data = await request.json()
        if not data:
            return {"msg": "Переданы некорректные данные"}
        
        company_name = data.get("company_name")
        user_name = data.get("user_name")
        user_email = data.get("email")
        user_pass = data.get("password")

        # Проверка наличия обязательных полей
        if not company_name or not user_name or not user_email or not user_pass:
            return {"msg": "Все поля обязательны"}

        # Сбор данных клиента
        user_id, company_id, is_admin = await CrudPostgresql.set(company_name, user_name, user_email, user_pass)
        device_id = str(uuid.uuid4())
        # ip = request.client.host
        ip = request.client.host if request.client else "Unknown"
        ua = request.headers.get("user-agent", "Unknown Browser")
        token = await CrudJwt.create_token(user_id, company_id, is_admin, device_id, ip, ua)

        # Записываем сессию пользователя в Redis
        await CrudRedis.set(user_id, device_id, ip, ua, token)

        # Устанавливаем sessionid в cookies
        response.set_cookie(
            key="sessionid",  # Имя куки
            value=token,  # Значение куки (уникальный идентификатор сессии)
            max_age=3600,  # Время жизни куки — 1 час
            httponly=True,  # Куки доступны только на стороне сервера
            samesite="Strict"  # Защита от CSRF-атак
            # secure=True
        )

        return {"msg": "Пользователь создан"}