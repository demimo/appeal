from fastapi import HTTPException
import os


from app.appeal.config.Config import ConnCassandra




class InitializeCs:

    @staticmethod
    def initialize_tables():

        try:

            # Установка подключения
            conn = ConnCassandra.connection()

            # Создаем keyspace и таблицу
            conn.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {"appeal"}
                WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 2}};
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS appeals (
                    id UUID PRIMARY KEY,
                    name TEXT,
                    value INT
                );
            """)

            # Добавляем тестовые данные
            conn.execute("""
                INSERT INTO appeals (id, name, value)
                VALUES (uuid(), 'test_name_1', 100);
            """)
            conn.execute("""
                INSERT INTO appeals (id, name, value)
                VALUES (uuid(), 'test_name_2', 200);
            """)

            return {"message": "Keyspace, table, and test data created!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))