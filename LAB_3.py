import sqlite3
import hashlib


conn = sqlite3.connect("users.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    login TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL
)
""")
conn.commit()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def add_user(login, password, full_name):
    try:
        hashed = hash_password(password)
        cursor.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
                       (login, hashed, full_name))
        conn.commit()
        print("Користувач доданий успішно.")
    except sqlite3.IntegrityError:
        print("Користувач з таким логіном вже існує.")


def update_password(login, new_password):
    hashed = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE login = ?", (hashed, login))
    if cursor.rowcount == 0:
        print("Користувача не знайдено.")
    else:
        conn.commit()
        print("Пароль оновлено.")


def authenticate_user(login):
    cursor.execute("SELECT password FROM users WHERE login = ?", (login,))
    result = cursor.fetchone()
    
    if result is None:
        print("Користувача не знайдено.")
        return
    
    input_password = input("Введіть пароль: ")
    input_hash = hash_password(input_password)
    
    if input_hash == result[0]:
        print("Успішна автентифікація!")
    else:
        print("Невірний пароль.")



add_user("danylo", "pass111", "Ромащенко Данило Валерійович")
update_password("danylo", "newpass111")
authenticate_user("danylo")

