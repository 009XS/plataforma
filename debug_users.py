
import os
import sys
from app import app, mysql

def check_users():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, nombre, email, numero_control, tipo_usuario, password_hash, activo FROM usuarios")
            users = cursor.fetchall()
            print(f"Total users found: {len(users)}")
            for user in users:
                print(f"User: {user['nombre']}, Role: {user['tipo_usuario']}, Control #: {user['numero_control']}, Active: {user['activo']}")
                print(f"  Hash start: {str(user['password_hash'])[:20]}...")
        except Exception as e:
            print(f"Error checking users: {e}")

if __name__ == "__main__":
    check_users()
