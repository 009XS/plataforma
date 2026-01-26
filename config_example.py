# ========================================
# CONFIGURACIÓN DE EJEMPLO
# ========================================
# Copiar este archivo como config.py y configurar valores reales

import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent

# ====================================
# CONFIGURACIÓN DE FLASK
# ====================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_clave_secreta_muy_segura_aqui')

# Tamaño máximo de archivos (100 MB)
MAX_CONTENT_LENGTH = 100 * 1024 * 1024

# ====================================
# CONFIGURACIÓN DE MYSQL
# ====================================

MYSQL_CONFIG = {
    'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
    'USER': os.environ.get('MYSQL_USER', 'root'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'DB': os.environ.get('MYSQL_DB', 'eduplatform'),
    'CURSORCLASS': 'DictCursor'
}

# ====================================
# CONFIGURACIÓN DE EMAIL (SMTP)
# ====================================

EMAIL_CONFIG = {
    'SERVER': 'smtp.gmail.com',
    'PORT': 587,
    'USER': os.environ.get('EMAIL_USER', 'tu_email@gmail.com'),
    'PASS': os.environ.get('EMAIL_PASS', 'tu_app_password'),
    'FROM': os.environ.get('EMAIL_FROM', 'tu_email@gmail.com'),
    'SUPPORT': os.environ.get('SUPPORT_EMAIL', 'soporte@tudominio.com')
}

# Nota: Para Gmail, usar "App Passwords" en lugar de la contraseña regular
# https://myaccount.google.com/apppasswords

# ====================================
# CONFIGURACIÓN DE GOOGLE OAUTH
# ====================================

# Opción 1: Cargar desde archivo client_secret.json
# Opción 2: Usar variables de entorno

GOOGLE_OAUTH = {
    'CLIENT_ID': os.environ.get('GOOGLE_CLIENT_ID', 'tu_client_id.apps.googleusercontent.com'),
    'CLIENT_SECRET': os.environ.get('GOOGLE_CLIENT_SECRET', 'tu_client_secret'),
    'REDIRECT_URI': os.environ.get('GOOGLE_REDIRECT_URI', 'http://127.0.0.1:5000/google_callback')
}

# Crear credenciales en: https://console.cloud.google.com/apis/credentials

# ====================================
# CONFIGURACIÓN DE OPENAI
# ====================================

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'sk-...')

# Obtener API key en: https://platform.openai.com/api-keys

# ====================================
# CONFIGURACIÓN DE STRIPE
# ====================================

STRIPE_CONFIG = {
    'SECRET_KEY': os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...'),
    'PUBLIC_KEY': os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_...'),
    'WEBHOOK_SECRET': os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_...')
}

# Obtener keys en: https://dashboard.stripe.com/apikeys

# ====================================
# CONFIGURACIÓN DE FIREBASE (OPCIONAL)
# ====================================

FIREBASE_CREDENTIALS_FILE = 'firebase_admin.json'

# Descargar credenciales desde:
# Firebase Console > Project Settings > Service Accounts > Generate New Private Key

# ====================================
# RUTAS DE UPLOADS
# ====================================

UPLOAD_FOLDER = BASE_DIR / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Subdirectorios
UPLOAD_SUBDIRS = {
    'tareas': UPLOAD_FOLDER / 'tareas',
    'recursos': UPLOAD_FOLDER / 'recursos',
    'avatares': UPLOAD_FOLDER / 'avatares',
    'comunicados': UPLOAD_FOLDER / 'comunicados',
    'evidencias': UPLOAD_FOLDER / 'evidencias'
}

# Crear subdirectorios
for subdir in UPLOAD_SUBDIRS.values():
    subdir.mkdir(exist_ok=True)

# ====================================
# EXTENSIONES PERMITIDAS
# ====================================

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
    'doc', 'docx', 'ppt', 'pptx', 'xlsx', 'xls',
    'mp4', 'mp3', 'avi', 'mov',
    'py', 'java', 'cpp', 'c', 'js', 'html', 'css',
    'zip', 'rar', 'json', 'csv'
}

# ====================================
# CONFIGURACIÓN DE GAMIFICACIÓN
# ====================================

GAMIFICATION_CONFIG = {
    'XP_POR_TAREA_COMPLETADA': 50,
    'XP_POR_TAREA_PERFECTA': 100,  # Calificación 100
    'XP_POR_EXAMEN_APROBADO': 200,
    'XP_POR_RECURSO_VISTO': 10,
    'XP_POR_DIA_RACHA': 25,
    'EDUCOINS_POR_NIVEL': 100,
    'EDUCOINS_POR_INSIGNIA': 50,
    
    # Umbrales de nivel
    'NIVELES': {
        'bronce': 0,
        'plata': 500,
        'oro': 2000,
        'diamante': 5000,
        'maestro': 10000
    }
}

# ====================================
# CONFIGURACIÓN DE SEGURIDAD
# ====================================

SECURITY_CONFIG = {
    'SESSION_COOKIE_SECURE': False,  # True en producción con HTTPS
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'PERMANENT_SESSION_LIFETIME': 3600,  # 1 hora en segundos
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOCKOUT_DURATION': 900  # 15 minutos en segundos
}

# ====================================
# CONFIGURACIÓN DE LOGGING
# ====================================

LOGGING_CONFIG = {
    'LEVEL': 'INFO',
    'FILE': 'auditoria.log',
    'MAX_BYTES': 10485760,  # 10 MB
    'BACKUP_COUNT': 5
}

# ====================================
# CONFIGURACIÓN DE CACHE (Futuro)
# ====================================

CACHE_CONFIG = {
    'TYPE': 'simple',  # 'redis', 'memcached'
    'DEFAULT_TIMEOUT': 300
}

# ====================================
# CONFIGURACIÓN DE API EXTERNA
# ====================================

# CoinGecko (criptomonedas)
COINGECKO_API_ENABLED = False

# Polygon (mercados financieros)
POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY', '')

# ====================================
# MODO DE DESARROLLO
# ====================================

DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
TESTING = False

# ====================================
# NOTAS
# ====================================

"""
IMPORTANTE:

1. NUNCA subir este archivo a control de versiones si contiene credenciales reales
2. Agregar config.py a .gitignore
3. Usar variables de entorno en producción
4. Cambiar SECRET_KEY en producción
5. Usar HTTPS en producción (SESSION_COOKIE_SECURE = True)
6. Configurar CORS apropiadamente en producción
7. Usar contraseñas seguras para MySQL
8. Habilitar autenticación de 2 factores cuando sea posible

PARA USAR ESTE ARCHIVO:

1. Copiar como config.py:
   cp config_example.py config.py

2. Editar config.py con valores reales

3. Importar en app.py:
   from config import *

4. O usar variables de entorno (.env):
   pip install python-dotenv
   
   Crear archivo .env:
   SECRET_KEY=...
   MYSQL_PASSWORD=...
   etc.
"""
