from os import getenv
from flask import Flask, jsonify, abort, url_for
import mysql.connector

LISTEN_PORT = getenv("LISTEN_PORT", 8000)
DB_HOSTNAME = getenv("DB_HOSTNAME", "db")

app = Flask(__name__)

db_config = {
    'host': DB_HOSTNAME,
    'user': 'meow',
    'password': 'meow',
    'database': 'meow'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET'])
def index():
    routes = {
        "list_all_users": url_for('get_all_users', _external=True),
        "get_user_by_id": url_for('get_user', user_id=1, _external=True)  # Example with ID=1
    }
    return jsonify({
        "message": "Available routes ;)",
        "routes": routes
    })

@app.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, favorite_insult FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, favorite_insult FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify(user)
    else:
        abort(404, description="This user doe snot exist mate.")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=LISTEN_PORT)

