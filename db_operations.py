import psycopg2

def connect_db():
    return psycopg2.connect(dbname="mydatabase", user="postgres", password="Qq12345", host="192.168.1.60")

def fetch_emails():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT email FROM users;")
        emails = cursor.fetchall()
    conn.close()
    return emails

def fetch_phone_numbers():
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT phone_number FROM phone_numbers;")
        phone_numbers = cursor.fetchall()
    conn.close()
    return phone_numbers

def insert_email(email):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO users (email) VALUES (%s);", (email,))
    conn.commit()
    conn.close()

def insert_phone_number(phone_number):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO phone_numbers (phone_number) VALUES (%s);", (phone_number,))
    conn.commit()
    conn.close()

