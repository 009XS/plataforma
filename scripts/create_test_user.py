"""Script para crear/actualizar usuario de prueba con contraseña válida"""
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
    
    # Generar hash de contraseña compatible con Werkzeug
    password_hash = generate_password_hash('admin123')
    
    # Verificar usuarios existentes
    cursor.execute("SELECT id, nombre, numero_control, tipo_usuario, activo FROM usuarios ORDER BY id LIMIT 5")
    users = cursor.fetchall()
    
    print("\n=== Usuarios existentes ===")
    for u in users:
        print(f"  ID:{u['id']} - {u['nombre']} ({u['numero_control']}) - Rol: {u['tipo_usuario']} - Activo: {u['activo']}")
    
    if users:
        # Actualizar password de todos los usuarios activos
        cursor.execute("UPDATE usuarios SET password_hash = %s WHERE activo = 1", (password_hash,))
        mysql.connection.commit()
        updated = cursor.rowcount
        print(f"\n=== Contraseña actualizada para {updated} usuario(s) ===")
        print("Nueva contraseña para TODOS los usuarios activos: admin123")
    else:
        # Crear usuario de prueba
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, numero_control, curp, tipo_usuario, password_hash, activo, semestre)
            VALUES (%s, %s, %s, %s, %s, %s, 1, '2025-1')
        ''', ('Admin Test', 'admin@test.com', 'ADMIN001', 'TEST000000HDFRRR00', 'admin', password_hash))
        mysql.connection.commit()
        print("\n=== Usuario de prueba creado ===")
        print("Numero de control: ADMIN001")
        print("Contraseña: admin123")
        print("Rol: admin")
    
    cursor.close()
    print("\n=== Listo! ===")
