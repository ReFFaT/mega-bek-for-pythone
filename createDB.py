import sqlite3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)

conn = sqlite3.connect('restaurant.db')

# создаем курсор для работы с базой данных
cur = conn.cursor()


# Создание таблицы всех блюд
cur.execute('''CREATE TABLE IF NOT EXISTS all_dishes
               (id INTEGER PRIMARY KEY,
               image TEXT,
               name TEXT NOT NULL,
               title TEXT,
               price REAL NOT NULL,
               gram INTEGER,
               type TEXT,
               selected TEXT)''')

# Добавление записей в таблицу всех блюд (Пример записи)
cur.execute("INSERT INTO all_dishes (id, image, name, title, price, gram, type, selected) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, 'steak.svg', 'Стейк', 'Описание стейка', 400, 600, 'Горячие блюда', 'true'))

# Создание таблицы меню
cur.execute('''CREATE TABLE IF NOT EXISTS menu
               (id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               dishList TEXT)''')

cur.execute("INSERT INTO menu (id, title) VALUES (?, ?)",
            (1, 'Горячие блюда'))  # Пример записи
cur.execute("INSERT INTO menu (id, title) VALUES (?, ?)",
            (2, 'Десерты'))  # Пример записи
cur.execute("INSERT INTO menu (id, title) VALUES (?, ?)",
            (3, 'Напитки'))  # Пример записи
# Добавьте другие категории в таблицу

# Обновление таблицы меню с учетом флага "selected"
cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")




cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )''')

# Добавление тестовых данных
cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Администратор", "admin@example.com", "admin123", "admin"))
cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            ("Пользователь", "user@example.com", "user123", "user"))



# Создаем новую таблицу "orders" с новой структурой
cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                address TEXT,
                time TEXT,
                dishList TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')

# Вставляем новые данные в таблицу "orders"
cur.execute("INSERT INTO orders (id, user_id, address, time, dishList) VALUES (?, ?, ?, ?, ?)",
            (1, 1, "Some address", "Some time", json.dumps([
                {
                    "id": 1,
                    "value": 2
                },
                {
                    "id": 2,
                    "value": 3
                },
                {
                    "id": 3,
                    "value": 1
                }
            ])))

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()