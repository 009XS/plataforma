"""Script para crear un usuario TUTOR de prueba"""
from flask import Flask
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'eduplatform'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

with app.app_context():
    cursor = mysql.connection.cursor()

    # Generar hash de contraseña
    password_hash = generate_password_hash('tutor123')

    # Verificar si ya existe un usuario tutor
    cursor.execute("SELECT id, nombre, numero_control FROM usuarios WHERE tipo_usuario = 'tutor' LIMIT 1")
    existing_tutor = cursor.fetchone()

    if existing_tutor:
        # Actualizar contraseña del tutor existente
        cursor.execute("UPDATE usuarios SET password_hash = %s, activo = 1 WHERE id = %s", 
                      (password_hash, existing_tutor['id']))
        mysql.connection.commit()
        print("\n=== Usuario TUTOR actualizado ===")
        print(f"ID: {existing_tutor['id']}")
        print(f"Nombre: {existing_tutor['nombre']}")
        print(f"Numero de control: {existing_tutor['numero_control']}")
        print("Nueva contraseña: tutor123")
    else:
        # Crear nuevo usuario tutor
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, numero_control, curp, tipo_usuario, password_hash, activo, semestre)
            VALUES (%s, %s, %s, %s, %s, %s, 1, '2025-1')
        ''', ('Tutor Test', 'tutor@test.com', 'TUT001', 'TUTOR00000HDFRRR00', 'tutor', password_hash))
        mysql.connection.commit()
        new_id = cursor.lastrowid
        
        print("\n=== Usuario TUTOR creado ===")
        print(f"ID: {new_id}")
        print("Nombre: Tutor Test")
        print("Numero de control: TUT001")
        print("Contraseña: tutor123")
        print("Rol: tutor")

    cursor.close()
    print("\n=== Listo! Ahora puedes iniciar sesión ===")
