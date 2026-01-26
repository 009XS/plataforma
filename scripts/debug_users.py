
import os
import sys
from flask import Flask
from flask_mysqldb import MySQL

# Setup minimal Flask app to access DB
app = Flask(__name__)
# Load config from app.py by importing or manually setting
# Manual setting is safer to avoid side effects of importing app
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'eduplatform'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def check_users():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, nombre, email, numero_control, tipo_usuario, activo, password_hash FROM usuarios")
            users = cursor.fetchall()
            print(f"Found {len(users)} users.")
            for u in users:
                ph = u['password_hash']
                short_hash = ph[:20] if ph else "None"
                print(f"ID: {u['id']}, Name: {u['nombre']}, Role: {u['tipo_usuario']}, Control: {u['numero_control']}, Active: {u['activo']}, Hash: {short_hash}...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_users()
