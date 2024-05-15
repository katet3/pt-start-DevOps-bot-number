import psycopg2
from psycopg2 import sql, connect, OperationalError

def create_connection(db_name="postgres"):
    """ Функция для создания и открытия подключения к базе данных """
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user='postgres',  # Замените на ваше имя пользователя
            password='Qq12345',  # Замените на ваш пароль
            host='192.168.1.60',  # Замените на ваш хост, если отличается
            port='5432'  # Порт, на котором работает ваш PostgreSQL сервер
        )
        return conn
    except OperationalError as e:
        print(f"Ошибка подключения: {e}")
        return None

def create_database():
    """ Функция для создания новой базы данных """
    conn = create_connection("postgres")  # Подключаемся к базовой БД для создания новой
    conn.autocommit = True  # Включаем autocommit для создания базы данных
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE mydatabase")
        print("База данных создана успешно")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    cursor.close()
    conn.close()

def create_tables():
    """ Функция для создания таблиц """
    conn = create_connection("mydatabase")  # Подключаемся к новой базе данных
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL
            );
            CREATE TABLE phone_numbers (
                id SERIAL PRIMARY KEY,
                phone_number VARCHAR(20) NOT NULL
            );
        """)
        print("Таблицы созданы успешно")
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    conn.commit()  # Фиксируем изменения
    cursor.close()
    conn.close()

def insert_data():
    """ Функция для вставки данных в таблицы """
    conn = create_connection("mydatabase")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email) VALUES (%s)", ('example@example.com',))
        cursor.execute("INSERT INTO users (email) VALUES (%s)", ('user@domain.com',))
        cursor.execute("INSERT INTO phone_numbers (phone_number) VALUES (%s)", ('+1234567890',))
        cursor.execute("INSERT INTO phone_numbers (phone_number) VALUES (%s)", ('+1987654321',))
        conn.commit()
        print("Данные добавлены успешно")
    except psycopg2.Error as e:
        print(f"Ошибка при вставке данных: {e}")
        conn.rollback()
    cursor.close()
    conn.close()

# Вызов функций
create_database()  # Создаем базу данных
create_tables()    # Создаем таблицы
insert_data()      # Вставляем тестовые данные
