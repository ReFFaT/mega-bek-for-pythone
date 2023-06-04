
import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)
# получение меню
@app.route('/menu', methods=['GET'])
def get_menu():
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM menu")
    menu_table = cur.fetchall()

    menu_data = []
    for row in menu_table:
        menu_item = {
            'id': row[0],
            'title': row[1],
            'dishList': json.loads(row[2])
        }
        menu_data.append(menu_item)

    conn.close()

    return jsonify(menu_data)

# добавление меню
@app.route('/menu', methods=['POST'])
def add_menu_item():
    try:
        # Получение данных из запроса
        menu_data = request.json
        title = menu_data['title']

        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Добавление записи в таблицу меню
        cur.execute("INSERT INTO menu (title) VALUES (?)", (title,))

        # Получение данных из таблицы всех блюд, соответствующих новому разделу
        cur.execute("SELECT * FROM all_dishes WHERE type = ? AND selected = 'true'", (title,))
        dish_rows = cur.fetchall()

        # Обновление dishList для нового раздела в таблице меню
        dishList = []
        for row in dish_rows:
            dish_item = {
                'id': row[0],
                'image': row[1],
                'name': row[2],
                'title': row[3],
                'price': row[4],
                'gram': row[5],
                'type': row[6]
            }
            dishList.append(dish_item)

        cur.execute("UPDATE menu SET dishList = ? WHERE title = ?", (json.dumps(dishList), title))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Menu item added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# обновление меню
@app.route('/menu/<int:menu_id>', methods=['PUT'])
def update_menu(menu_id):
    try:
        # Получение данных из запроса
        menu_data = request.json
        title = menu_data['title']

        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Получение блюд из таблицы all_dishes, соответствующих указанному заголовку и флагу активности
        cur.execute("SELECT * FROM all_dishes WHERE type = ? AND selected = 'true'", (title,))
        dish_rows = cur.fetchall()

        # Обновление dishList в таблице меню
        dishList = []
        for row in dish_rows:
            dish_item = {
                'id': row[0],
                'image': row[1],
                'name': row[2],
                'title': row[3],
                'price': row[4],
                'gram': row[5],
                'type': row[6]
            }
            dishList.append(dish_item)

        cur.execute("UPDATE menu SET title = ?, dishList = ? WHERE id = ?", (title, json.dumps(dishList), menu_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Menu item updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# удаление меню
@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Удаление записи из таблицы меню по ID
        cur.execute("DELETE FROM menu WHERE id=?", (item_id,))

        # Сохраняем изменения в базе данных
        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()

        return jsonify({'message': 'Menu item deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    







                                                                                                                        # блюда

# создание блюда
@app.route('/dishes', methods=['POST'])
def add_dish():
    try:
        # Получение данных из запроса
        dish_data = request.json
        image = dish_data['image']
        name = dish_data['name']
        title = dish_data['title']
        price = dish_data['price']
        gram = dish_data['gram']
        dish_type = dish_data['type']
        selected = dish_data['selected']

        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Добавление записи в таблицу всех блюд
        cur.execute("INSERT INTO all_dishes (image, name, title, price, gram, type, selected) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (image, name, title, price, gram, dish_type, selected))
        cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")

        conn.commit()
        conn.close()

        return jsonify({'message': 'Dish added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "image": "steak.svg",
#   "name": "Стейк",
#   "title": "Описание стейка",
#   "price": 400,
#   "gram": 600,
#   "type": "Горячие блюда",
#   "selected": "true"
# }    

# удаление блюда
@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    try:
        # Открытие соединения с базой данных
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Удаление записи из таблицы всех блюд по заданному ID
        cur.execute("DELETE FROM all_dishes WHERE id = ?", (dish_id,))
        cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")

        conn.commit()
        conn.close()

        return jsonify({'message': 'Dish deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


# обновление блюда
@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    try:
        # Получение данных из запроса
        dish_data = request.json
        image = dish_data['image']
        name = dish_data['name']
        title = dish_data['title']
        price = dish_data['price']
        gram = dish_data['gram']
        type = dish_data['type']
        selected = dish_data['selected']

        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Обновление записи в таблице всех блюд по ID
            cur.execute("UPDATE all_dishes SET image=?, name=?, title=?, price=?, gram=?, type=?, selected=? WHERE id=?",
                        (image, name, title, price, gram, type, selected, dish_id))

            # Обновление таблицы меню с учетом изменений
            cur.execute("UPDATE menu SET dishList = (SELECT json_group_array(json_object('id', all_dishes.id, 'image', all_dishes.image, 'name', all_dishes.name, 'title', all_dishes.title, 'price', all_dishes.price, 'gram', all_dishes.gram, 'type', all_dishes.type)) FROM all_dishes WHERE all_dishes.type = menu.title AND all_dishes.selected = 'true')")

            conn.commit()

        return jsonify({'message': 'Dish updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "image": "new_image.svg",
#   "name": "Новое блюдо",
#   "title": "Описание нового блюда",
#   "price": 500,
#   "gram": 800,
#   "type": "Горячие блюда",
#   "selected": "true"
# }


# получение блюда
@app.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    try:
        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Получение записи из таблицы всех блюд по ID
            cur.execute("SELECT * FROM all_dishes WHERE id=?", (dish_id,))
            dish = cur.fetchone()

            if dish is None:
                return jsonify({'error': 'Dish not found'}), 404

            # Формирование объекта блюда
            dish_data = {
                'id': dish[0],
                'image': dish[1],
                'name': dish[2],
                'title': dish[3],
                'price': dish[4],
                'gram': dish[5],
                'type': dish[6],
                'selected': dish[7]
            }

        return jsonify(dish_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# получение всех блюд
@app.route('/dishes', methods=['GET'])
def get_all_dishes():
    try:
        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Получение всех записей из таблицы всех блюд
            cur.execute("SELECT * FROM all_dishes")
            dishes = cur.fetchall()

            # Формирование списка объектов блюд
            dish_list = []
            for dish in dishes:
                dish_data = {
                    'id': dish[0],
                    'image': dish[1],
                    'name': dish[2],
                    'title': dish[3],
                    'price': dish[4],
                    'gram': dish[5],
                    'type': dish[6],
                    'selected': dish[7]
                }
                dish_list.append(dish_data)

        return jsonify(dish_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


                                                                                                                        # пользователи
# Получение всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        user_list = []
        for user in users:
            user_data = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'password': user[3],
                'role': user[4]
            }
            user_list.append(user_data)

        conn.close()

        return jsonify(user_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Получение конкретного пользователя
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'error': 'User not found'}), 404

        user_data = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3],
            'role': user[4]
        }

        conn.close()

        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Обновление пользователя
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        user_data = request.json

        # Проверка наличия обязательных полей
        if 'name' not in user_data or 'email' not in user_data or 'password' not in user_data or 'role' not in user_data:
            return jsonify({'error': 'Missing required fields'}), 400

        name = user_data['name']
        email = user_data['email']
        password = user_data['password']
        role = user_data['role']

        cur.execute("UPDATE users SET name=?, email=?, password=?, role=? WHERE id=?",
                    (name, email, password, role, user_id))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User updated successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "name": "Новое имя",
#   "email": "новыйemail@example.com",
#   "password": "новыйпароль",
#   "role": "новаяроль"
# }

# создание
@app.route('/register', methods=['POST'])
def register_user():
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()
        
        # Получение данных из запроса
        user_data = request.json
        name = user_data['name']
        email = user_data['email']
        password = user_data['password']
        
        # Установка роли пользователя
        role = 'user'
        
        # Вставка данных в таблицу пользователей
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                    (name, email, password, role))
        conn.commit()
        
        # Получение ID созданного пользователя
        user_id = cur.lastrowid
        
        # Получение информации о созданном пользователе
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        
        # Формирование ответа с информацией о созданном пользователе
        user_data = {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[4]
        }
        
        # Закрытие соединения с базой данных
        conn.close()
        
        return jsonify({'user': user_data, 'message': 'User registered successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# {
#   "name": "John Doe",
#   "email": "johndoe@example.com",
#   "password": "password123"
# }

# Удаление пользователя
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# авторизация
@app.route('/login', methods=['POST'])
def login():
    try:
        # Получение данных из запроса
        login_data = request.json
        email = login_data['email']
        password = login_data['password']

        # Открытие соединения с базой данных
        with sqlite3.connect('restaurant.db') as conn:
            cur = conn.cursor()

            # Поиск пользователя по email и password
            cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cur.fetchone()

            if user is None:
                return jsonify({'error': 'Invalid email or password'}), 401

            # Формирование объекта пользователя с дополнительным полем "authorized"
            user_data = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'password': user[3],
                'role': user[4],
                'authorized': True
            }

        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400
# {
#   "email": "example@example.com",
#   "password": "password123"
# }




                # заказыуууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууу


# Удаление заказа по его ID
@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()

    # Проверяем, существует ли заказ с указанным ID
    cur.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
    existing_order = cur.fetchone()

    if existing_order:
        # Удаляем заказ из таблицы
        cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Order deleted successfully'})
    else:
        conn.close()
        return jsonify({'message': 'Order not found'})
    









    
# Создание нового заказа
@app.route('/order', methods=['POST'])
def create_order():
    try:
        conn = sqlite3.connect('restaurant.db')
        cur = conn.cursor()

        # Получаем данные заказа из тела запроса
        order_data = request.json

        # Извлекаем необходимые поля из данных заказа
        user_id = order_data['user_id']
        address = order_data['address']
        time = order_data['time']
        dish_list = order_data['list']
        phone = order_data['phone']
        status = order_data['status']

        # Проверяем, существует ли пользователь с указанным ID
        cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        existing_user = cur.fetchone()

        if existing_user:
            # Вставляем новый заказ в таблицу "orders"
            cur.execute("INSERT INTO orders (user_id, address, time, dishList, phone, status) VALUES (?, ?, ?, ?, ?, ?)",
                        (user_id, address, time, json.dumps(dish_list), phone, status))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Order created successfully'})
        else:
            conn.close()
            return jsonify({'message': 'User not found'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
#     {
#     "id": 1,
#     "user_id": 1,
#     "address": "Some address",
#     "time": "Some time",
#     "dishList": [
#       {
#         "id": 1,
#         "value": 2
#       },
#       {
#         "id": 2,
#         "value": 3
#       },
#       {
#         "id": 3,
#         "value": 1
#       }
#     ],
#     "phone": "1234567890",
#     "status": "pending"
#   },



# Получение информации о заказе по ID пользователя
@app.route('/order/user/<int:user_id>', methods=['GET'])

def get_order_by_user(user_id):
    conn = sqlite3.connect('restaurant.db')
    cur = conn.cursor()
    
    # Получаем информацию о заказе пользователя из таблицы "orders"
    cur.execute("SELECT orders.id, orders.user_id, orders.address, orders.time, orders.dishList, orders.phone, orders.status FROM orders JOIN users ON orders.user_id = users.id WHERE user_id = ?", (user_id,))
    orders = cur.fetchall()

    if orders:
        response = []
        for order in orders:
            # Разбираем JSON-строку в список блюд
            dish_list = json.loads(order[4])
            dish_objects = []

            # Получаем объекты блюд из таблицы "all_dishes" по их идентификаторам
            for dish in dish_list:
                cur.execute("SELECT * FROM all_dishes WHERE id = ?", (dish['id'],))
                dish_data = cur.fetchone()

                if dish_data:
                    # Формируем информацию о блюде в формате JSON с полем "value"
                    dish_object = {
                        "id": dish_data[0],
                        "image": dish_data[1],
                        "name": dish_data[2],
                        "title": dish_data[3],
                        "price": dish_data[4],
                        "gram": dish_data[5],
                        "type": dish_data[6],
                        "value": dish['value']
                    }
                    dish_objects.append(dish_object)
            # Формируем информацию о заказе в формате JSON
            order_data = {
                "id": order[0],
                "user_id": order[1],
                "address": order[2],
                "time": order[3],
                "list": dish_objects,
                "phone": order[5],
                "status": order[6]
            }
            response.append(order_data)

        conn.close()
        return jsonify(response)
    else:
        conn.close()
        return jsonify({'message': 'No orders found for the user'})

if __name__ == '__main__':
    app.run(debug=True)