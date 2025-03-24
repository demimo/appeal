from fastapi import  HTTPException
import bcrypt

from app.protected.config.Config import ConnPostgresql


class CrudPostgresql:

    # Асинхронный метод для добавления пользователя в базу данных
    @staticmethod
    async def set(company_name, user_name, user_email, user_pass):

        # Хеширование пароля
        password = user_pass.encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')

        # Используем как асинхронный контекстный менеджер
        async with ConnPostgresql() as conn:

            # Группируем операции в транзакцию
            async with conn.transaction():
         
                # Проверяем на существование пользователя
                check_company_name = await conn.fetchrow(
                    'SELECT company_name FROM companies WHERE company_name = $1',
                    company_name
                )
                if check_company_name:
                    raise HTTPException(status_code=400, detail="Компания с таким именем уже существует")
                
                # Проверяем на существование пользователя
                check_email = await conn.fetchrow(
                    'SELECT email FROM users WHERE email = $1',
                    user_email
                )
                if check_email:
                    raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

                # Добавляем компанию в базу данных
                company_row_id = await conn.fetchrow('''
                    INSERT INTO companies (company_name)
                    VALUES ($1)
                    RETURNING id;
                ''', company_name)
                company_id = company_row_id["id"]

                # Добавляем пользователя в базу данных
                is_admin = True
                user_row_id = await conn.fetchrow('''
                    INSERT INTO users (user_name, email, hashed_password, is_admin)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id, is_admin;
                ''', user_name, user_email, hashed_password, is_admin)
                user_id = user_row_id["id"]
                user_is_admin = user_row_id["is_admin"]

                # Связываем пользователя и компанию
                await conn.execute('''
                    INSERT INTO company_user (user_id, company_id)
                    VALUES ($1, $2);
                ''', user_id, company_id)

                # Возвращаем id
                return user_id, company_id, user_is_admin
            


    # Асинхронный метод для получения данных пользователя из базы данных
    @staticmethod
    async def get(user_email, user_pass):
            
        # Используем как асинхронный контекстный менеджер
        async with ConnPostgresql() as conn:

            # Группируем операции в транзакцию
            async with conn.transaction():

                # Получаем id, is_admin и хеш пароля пользователя с базы
                user_row = await conn.fetchrow(
                    'SELECT id, email, is_admin, hashed_password FROM users WHERE email = $1',
                    user_email
                )
                if user_row is None:
                    raise HTTPException(status_code=404, detail="Пользователь с таким email не зарегистрирован")
                user_id = user_row["id"]
                is_admin = user_row["is_admin"]
                hashed_password = user_row["hashed_password"]

                # Проверка пароля
                if bcrypt.checkpw(user_pass.encode(), hashed_password.encode()) == False:
                    raise HTTPException(status_code=401, detail="Не верный пароль")
                
                # Получаем company_id пользователя с базы
                company_row = await conn.fetchrow(
                    'SELECT company_id FROM company_user WHERE user_id = $1',
                    user_id
                )
                company_id = company_row["company_id"]

                # Возвращаем id
                return user_id, company_id, is_admin


        




            




# # Получение всех данных
# async def getAll():

#     # Используем ConnUserPostgresql как асинхронный контекстный менеджер
#     async with ConnPostgresql() as conn:

#         # Выполнение SQL-запроса
#         rows = await conn.fetch('SELECT * FROM users LIMIT 50')

#     # Проверяем, есть ли результат запроса
#     if rows is None:
#         # Если пользователя нет, возвращаем ошибку (например, 404)
#         return {"error": "User not found"}  # Просто словарь, FastAPI сам превратит его в JSON
    
#     # Возвращаемые данные в виде словаря, FastAPI сам превратит его в JSON
#     data = []
#     for row in rows:
#         data.append(dict(row))

#     return data




# # Получение данных по ID с базы данных
# async def get(item_id: int):
#     # Используем ConnUserPostgresql как асинхронный контекстный менеджер
#     async with ConnPostgresql() as conn:

#         # Выполнение SQL-запроса по ID
#         row = await conn.fetchrow('SELECT * FROM users WHERE id = $1', item_id)

#     # Проверяем, есть ли результат запроса
#     if row is None:
#         # Если пользователя нет, возвращаем ошибку (например, 404)
#         return json.dumps({"error": "User not found"}, ensure_ascii=False, indent=4)
    
#     # Преобразуем данные в словарь
#     data = dict(row)

#     # Возвращаем данные в формате JSON
#     return json.dumps(data, ensure_ascii=False, indent=4)




# # Асинхронная функция для вставки данных в базу
# async def add(item_data: dict):  # Используем стандартный dict
#     # Используем ConnUserPostgresql как асинхронный контекстный менеджер
#     async with ConnPostgresql() as conn:

#         # Выполнение SQL-запроса на вставку данных
#         await conn.execute('''
#             INSERT INTO users (first_name, last_name, email, hashed_password) VALUES($1, $2, $3, $4)
#         ''', item_data['first_name'], item_data['last_name'], item_data['email'], item_data['hashed_password'])

#     return {"message": "Данные успешно добавлены!"}




# # # Асинхронная функция для изменения данных в базе по ID
# # async def update_data(data_id: int, item_data: dict):  # Используем стандартный dict
# #     # Подключение к базе данных
# #     conn = await ConnUserPostgresql.connection()

# #     # Динамическое построение SQL-запроса в зависимости от того, какие поля переданы
# #     set_clause = []
# #     values = []

# #     # Проходим по всем ключам и значениям, добавляя их в запрос
# #     for index, (key, value) in enumerate(item_data.items(), 1):
# #         set_clause.append(f"{key} = ${index}")
# #         values.append(value)

# #     # Если не переданы данные для обновления, просто завершаем функцию
# #     if not set_clause:
# #         await conn.close()
# #         return {"message": "Нет изменений для обновления"}
    
# #     # Формируем окончательный SQL-запрос
# #     query = f"""
# #         UPDATE users 
# #         SET {', '.join(set_clause)} 
# #         WHERE id = ${len(set_clause) + 1}
# #     """

# #     # Добавляем ID пользователя в значения
# #     values.append(data_id)

# #     # Выполнение SQL-запроса
# #     await conn.execute(query, *values)

# #     # Закрытие соединения
# #     await conn.close()

# #     return {"message": "Данные успешно изменены!"}



# # Удаление данных по ID с базы данных
# async def delete(item_id: int):
#     # Используем ConnUserPostgresql как асинхронный контекстный менеджер
#     async with ConnPostgresql() as conn:

#         # Выполнение SQL-запроса по ID
#         result = await conn.execute('DELETE FROM users WHERE id = $1', item_id)

#     # Если не удалено ни одной строки, возвращаем None
#     if result == "DELETE 0":
#         await conn.close()
#         return {"message": "Данные не найдены для удаления."}

#     # Возвращаем данные в формате JSON
#     return {"message": "Данные успешно удалены!"}









