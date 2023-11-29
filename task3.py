from flask import Flask, jsonify, request
import mysql.connector
from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)


# MySQL configuration
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT")

# Secret key for authentication
SECRET_KEY = os.getenv("secret_key")
# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = connection.cursor()

    print("Connected to MySQL")

except mysql.connector.Error as e:
    print("Error connecting to MySQL:", e)


@app.route('/api/users', methods=['GET'])
def get_users():
    auth_token = request.headers.get('Authorization')

    # Check authorization token
    if auth_token != f'Bearer {SECRET_KEY}':
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()  # Fetch all rows

        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }
            user_list.append(user_dict)

        return jsonify({'users': user_list})

    except mysql.connector.Error as e:
        print("Error fetching users:", e)
        return jsonify({'message': 'Error fetching users'}), 500


if __name__ == '__main__':
    app.run(debug=True)