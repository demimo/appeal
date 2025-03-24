from app.protected.config.Config import ConnPostgresql

async def initialize_tables():

    """
    Создает таблицы, если они не существуют, и добавляет тестовые данные.
    """
    async with ConnPostgresql() as conn:
        
        # Создание таблиц
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL UNIQUE
            );
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                email_verify BOOLEAN DEFAULT FALSE,
                is_admin BOOLEAN DEFAULT FALSE
            );
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS company_user (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                company_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
            );
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS company_partner (
                id SERIAL PRIMARY KEY,
                company_id INT,
                partner_company_id INT,
                is_partner BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
                FOREIGN KEY (partner_company_id) REFERENCES companies(id) ON DELETE CASCADE
            );
        ''')
        print("✅ Таблицы успешно созданы или уже существуют.")


async def add_test_data():

    """
    Добавляет тестовые данные в таблицы.
    """
    async with ConnPostgresql() as conn:

        # Добавление данных в таблицу companies
        await conn.execute('''
            INSERT INTO companies (company_name)
            VALUES ($1)
            ON CONFLICT (company_name) DO NOTHING;
        ''', "Test Company 1")

        await conn.execute('''
            INSERT INTO companies (company_name)
            VALUES ($1)
            ON CONFLICT (company_name) DO NOTHING;
        ''', "Test Company 2")

        # Добавление данных в таблицу users
        await conn.execute('''
            INSERT INTO users (user_name, email, hashed_password, email_verify, is_admin)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (email) DO NOTHING;
        ''', "User 1", "user1@example.com", "hashed_password_1", True, False)

        await conn.execute('''
            INSERT INTO users (user_name, email, hashed_password, email_verify, is_admin)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (email) DO NOTHING;
        ''', "Admin User", "admin@example.com", "hashed_password_admin", True, True)

        # Добавление данных в таблицу company_user
        await conn.execute('''
            INSERT INTO company_user (user_id, company_id)
            VALUES ($1, $2);
        ''', 1, 1)

        await conn.execute('''
            INSERT INTO company_user (user_id, company_id)
            VALUES ($1, $2);
        ''', 2, 2)

        # Добавление данных в таблицу company_partner
        await conn.execute('''
            INSERT INTO company_partner (company_id, partner_company_id, is_partner)
            VALUES ($1, $2, $3);
        ''', 1, 2, True)

        await conn.execute('''
            INSERT INTO company_partner (company_id, partner_company_id, is_partner)
            VALUES ($1, $2, $3);
        ''', 2, 1, True)

        print("✅ Тестовые данные успешно добавлены.")