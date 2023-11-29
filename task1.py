from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Retrieve database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT")
SECRET_KEY = os.getenv("secret_key")

@app.route('/api/getHostfamilies', methods=['GET'])
def get_host_families():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            port=DB_PORT
        )

        auth_token = request.headers.get('Authorization')

        # Check authorization token
        if auth_token != f'Bearer {SECRET_KEY}':
            return jsonify({'message': 'Unauthorized'}), 401

        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()

            # Execute queries and perform operations here
            cursor.execute("SELECT id FROM host_families")
            rows = cursor.fetchall()
            truncate_query = "TRUNCATE TABLE host_family_ranking;"
            cursor.execute(truncate_query)
            for row in rows:
                cursor.execute("INSERT INTO host_family_ranking (hf_id, hf_ranking) VALUES (%s, %s)", (row[0], 1))

            connection.commit()
            print("Queries executed successfully")

    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

    return jsonify({'message': 'Success'})

if __name__ == '__main__':
    app.run(debug=True)
