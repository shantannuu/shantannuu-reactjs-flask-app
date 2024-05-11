# backend/app.py
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

DB_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing (CORS)

# PostgreSQL connection details
DB_NAME = 'React_flask_app'
DB_USER = 'postgres'
DB_PASSWORD = 'shantanu'
DB_HOST = 'localhost'
DB_PORT = '5432'

def get_db_connection():
    # return 
    # psycopg2.connect(
    #     dbname=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     host=DB_HOST,
    #     port=DB_PORT
    # )
    return psycopg2.connect(DB_URL)

@app.route('/api/post-data', methods=['POST'])
def post_data():
    try:
        # Extract data from request
        data = request.get_json()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert data into database
        cursor.execute("INSERT INTO students (name) VALUES (%s)", (data['name'],))
        conn.commit()

        # Close database connection
        cursor.close()
        conn.close()

        return jsonify({"message": "Data posted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/get-data', methods=['GET'])
def get_data():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch data from database
        cursor.execute("SELECT * FROM students ORDER BY id")
        data = cursor.fetchall()

        # Close database connection
        cursor.close()
        conn.close()

        # Convert data to a list of dictionaries
        data_list = [{'id': row[0], 'name': row[1]} for row in data]

        return jsonify(data_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/update-data/<int:id>', methods=['PUT'])
def update_data(id):
    try:
        # Extract data from request
        data = request.get_json()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update data in the database
        cursor.execute("UPDATE students SET name = %s WHERE id = %s", (data['name'], id))
        conn.commit()

        # Close database connection
        cursor.close()
        conn.close()

        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete-data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete data from the database
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()

        # Close database connection
        cursor.close()
        conn.close()

        return jsonify({"message": "Data deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
