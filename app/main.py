from fastapi import FastAPI, Response, Request, HTTPException
from app.appeal.config.Config import ConnCassandra
# from app.appeal.Created import Created
import os

from app.protected.config.init_sql import initialize_tables, add_test_data
from app.protected.Registration import Registration
from app.protected.Login import Login
from app.protected.Check import Check
from app.protected.Logout import Logout
from app.protected.Device import Device

from app.appeal.config.InitializeCs import InitializeCs
from app.appeal.config.Config import ConnCassandra
from app.appeal.crud.CrudCassandra import CrudCassandra

app = FastAPI()

@app.get("/startpg")
async def startup_event():
    await initialize_tables()
    await add_test_data()
    print("🚀 Приложение запущено, таблицы инициализированы, добавлены тестовые данные.")

@app.post("/registration")
async def reg(request: Request, response: Response):
    data = await Registration.registration(request, response)
    return data

@app.post("/login")
async def log(request: Request, response: Response):
    data = await Login.login(request, response)
    return data

@app.post("/logout")
async def out(request: Request, response: Response):
    data = await Logout.logout(request, response)
    return data

@app.get("/device")
async def dev(request: Request):
    data = await Device.device(request)
    return data

# Базовый маршрут для проверки работоспособности API
@app.get("/protected")
async def read_root(request: Request):
    protected = await Check.check(request)
    if protected != True:
        raise protected
    # return {"msg": "Список пользователей"}
    return protected


    





@app.get("/startcs")
async def startcs():
    data = InitializeCs.initialize_tables()
    return data

@app.get("/byid")
async def get_by_id():
    data = await CrudCassandra.get()
    return data


@app.get("/data")
async def get_data():
    try:

        conn = ConnCassandra.connection()

        # Получаем данные из таблицы
        conn.set_keyspace(os.getenv("CASSANDRA_KEYSPACE"))
        rows = conn.execute("SELECT * FROM appeals")
        data = [{"id": str(row.id), "name": row.name, "value": row.value} for row in rows]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @app.get("/appeals/created")
# async def created_data(request: Request, response: Response):
#     data = await Created.created(request)
#     return data











# # Регистрация пользователя
# @app.post("/registration")
# async def reg(request: Request):
#     data = await CrudUserPostgresql.registration_user(request)
#     return data


# # Вход пользователя
# @app.post("/login")
# async def door(request: Request, response: Response):
#     data = await CrudUserPostgresql.login(request, response)
#     return data


# # Базовый маршрут для проверки работоспособности API
# @app.get("/users")
# async def read_root(request: Request):
#     print("Cookies:", request.cookies)
#     protected_user = await ProtectedUser.check_auth_user(request)  # <--- добавляем await
#     if not protected_user:
#         return {"error": "Unauthorized"}
    
#     data = await CrudUserPostgresql.getAll()
#     return data


# # Получение по ID
# @app.get("/users/{user_id}")
# async def read_item(user_id: int, q: Union[str, None] = None):
#     data = await CrudUserPostgresql.get(user_id)
#     return json.loads(data)


# # Добавление
# @app.post("/users/add")
# async def create_item(user: dict):
#     data = await CrudUserPostgresql.add(user)
#     return data


# # Изменение по ID
# @app.put("/users/{user_id}")
# async def update_item(user_id: int, user: dict):
#     data = await CrudUserPostgresql.update_data(user_id, user)
#     return data


# # Удаление по ID
# @app.delete("/users/{user_id}")
# async def delete_item(user_id: int):
#     data = await CrudUserPostgresql.delete(user_id)
#     return data







# @app.get("/protected")
# async def protected(request: Request):
#     jwt_token = request.cookies.get("jwt")  # Получаем JWT из cookies
#     if not jwt_token:
#         raise HTTPException(status_code=401, detail="Token is missing")
#     return {"token": jwt_token}