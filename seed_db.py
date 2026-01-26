
import warnings
# Suppress specific warnings
warnings.filterwarnings("ignore", message=".*google.genai.*")
warnings.filterwarnings("ignore", category=FutureWarning)

from app import app, mysql
from werkzeug.security import generate_password_hash

def seed_users():
    print("Seeding users...")
    with app.app_context():
        cursor = mysql.connection.cursor()
        
        # Define test users
        users = [
            {
                "nombre": "Administrador Principal",
                "email": "admin@cecytem.mx",
                "numero_control": "admin",
                "curp": "ADMIN123456HEMX00",
                "tipo_usuario": "admin",
                "password": "admin123"
            },
            {
                "nombre": "Juan Pérez (Alumno)",
                "email": "alumno@cecytem.mx",
                "numero_control": "12345678",
                "curp": "ALUM123456HEMX00",
                "tipo_usuario": "alumno",
                "password": "password"
            },
            {
                "nombre": "Prof. María García",
                "email": "docente@cecytem.mx",
                "numero_control": "docente1",
                "curp": "DOC123456HEMX00",
                "tipo_usuario": "docente",
                "password": "password"
            },
            {
                "nombre": "Sr. Padre Tutor",
                "email": "tutor@cecytem.mx",
                "numero_control": "tutor1",
                "curp": "TUTOR123456HEMX00",
                "tipo_usuario": "tutor",
                "password": "password"
            },
            {
                "nombre": "Lic. Orientadora",
                "email": "orientador@cecytem.mx",
                "numero_control": "orientador1",
                "curp": "ORIENT123456HEMX00",
                "tipo_usuario": "orientador",
                "password": "password"
            }
        ]

        for user in users:
            try:
                # Check if user exists
                cursor.execute("SELECT id FROM usuarios WHERE numero_control = %s", (user['numero_control'],))
                existing = cursor.fetchone()
                
                if not existing:
                    hashed_pw = generate_password_hash(user['password'])
                    cursor.execute("""
                        INSERT INTO usuarios (nombre, email, numero_control, curp, tipo_usuario, password_hash, activo)
                        VALUES (%s, %s, %s, %s, %s, %s, 1)
                    """, (user['nombre'], user['email'], user['numero_control'], user['curp'], user['tipo_usuario'], hashed_pw))
                    print(f"[OK] Created user: {user['nombre']} ({user['tipo_usuario']}) - Pass: {user['password']}")
                else:
                    print(f"[SKIP] User exists: {user['numero_control']}")
            except Exception as e:
                print(f"[ERROR] Failed to create {user['numero_control']}: {e}")

        mysql.connection.commit()
        
        # Link Tutor to Alumno
        try:
             cursor.execute("SELECT id FROM usuarios WHERE tipo_usuario='tutor' AND numero_control='tutor1'")
             tutor = cursor.fetchone()
             cursor.execute("SELECT id FROM usuarios WHERE tipo_usuario='alumno' AND numero_control='12345678'")
             alumno = cursor.fetchone()
             
             if tutor and alumno:
                 # Update alumno with tutor_id
                 cursor.execute("UPDATE usuarios SET tutor_id = %s WHERE id = %s", (tutor['id'], alumno['id']))
                 
                 # Add to tutores_estudiantes table if it exists
                 cursor.execute("INSERT IGNORE INTO tutores_estudiantes (tutor_id, estudiante_id) VALUES (%s, %s)", (tutor['id'], alumno['id']))
                 
                 mysql.connection.commit()
                 print("[OK] Linked Tutor to Alumno")
        except Exception as e:
            print(f"Error linking tutor-alumno: {e}")

        print("Seeding complete.")

if __name__ == "__main__":
    seed_users()
