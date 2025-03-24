from fastapi import Request, HTTPException
import datetime
from datetime import timezone


from app.protected.crud.CrudJwt import CrudJwt
from app.protected.crud.CrudRedis import CrudRedis


class Check:


    @staticmethod
    async def check(request: Request):
            
        # Получаем JWT из cookies
        jwt_token = request.cookies.get("sessionid")
        if not jwt_token:
            raise HTTPException(status_code=401, detail="Токена нет необходимо авторизоваться")

        # Получаем информацию из JWT
        payload = await CrudJwt.decode_token(jwt_token)
        user_id = payload.get("user_id")
        device_id = payload.get("device_id")
        exp = payload.get("exp")

        if not user_id or not device_id:
            raise HTTPException(status_code=401, detail="Отсутствует user_id или device_id")

        # Преобразуем exp в datetime и сравниваем с текущим временем
        if datetime.datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Срок действия токена истек")

        # Получаем JWT с Redis
        data = await CrudRedis.get(user_id, device_id)
        if data != jwt_token:
            raise HTTPException(status_code=401, detail="Токена нет")

        return True
    

    @staticmethod
    async def check_for_logout(request: Request):
            
        # Получаем JWT из cookies
        jwt_token = request.cookies.get("sessionid")
        if not jwt_token:
            raise HTTPException(status_code=401, detail="Token is missing")

        # Получаем информацию из JWT
        payload = await CrudJwt.decode_token(jwt_token)
        user_id = payload.get("user_id")
        device_id = payload.get("device_id")
        exp = payload.get("exp")
        # Проверяем, что user_id и device_id не пустые и exp не истек
        if not user_id or not device_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id or device_id")

        # Преобразуем exp в datetime и сравниваем с текущим временем
        if datetime.datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        # Получаем JWT с Redis
        data = await CrudRedis.get(user_id, device_id)
        if data != jwt_token:
            raise HTTPException(status_code=401, detail="Токена нет")

        return user_id, device_id
    

    @staticmethod
    async def check_for_device(request: Request):
            
        # Получаем JWT из cookies
        jwt_token = request.cookies.get("sessionid")
        if not jwt_token:
            raise HTTPException(status_code=401, detail="Token is missing")

        # Получаем информацию из JWT
        payload = await CrudJwt.decode_token(jwt_token)
        user_id = payload.get("user_id")
        device_id = payload.get("device_id")
        exp = payload.get("exp")
        # Проверяем, что user_id и device_id не пустые и exp не истек
        if not user_id or not device_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id or device_id")

        # Преобразуем exp в datetime и сравниваем с текущим временем
        if datetime.datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        # Получаем JWT с Redis
        data = await CrudRedis.get(user_id, device_id)
        if data != jwt_token:
            raise HTTPException(status_code=401, detail="Токена нет")

        return user_id