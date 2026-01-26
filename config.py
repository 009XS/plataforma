import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu_clave_secreta_muy_segura_aqui')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    
    # Mail Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER', 'tu_email@gmail.com')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS', 'tu_app_password')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_FROM', 'tu_email@gmail.com')

    # Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your_gemini_api_key')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # Construir URI de conexión MySQL
    # Formato: mysql+pymysql://username:password@host/db_name
    _db_user = os.environ.get('MYSQL_USER', 'root')
    _db_pass = os.environ.get('MYSQL_PASSWORD', '')
    _db_host = os.environ.get('MYSQL_HOST', 'localhost')
    _db_name = os.environ.get('MYSQL_DB', 'eduplatform')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_db_user}:{_db_pass}@{_db_host}/{_db_name}"

class ProductionConfig(Config):
    DEBUG = False
    _db_user = os.environ.get('MYSQL_USER', 'root')
    _db_pass = os.environ.get('MYSQL_PASSWORD', '')
    _db_host = os.environ.get('MYSQL_HOST', 'localhost')
    _db_name = os.environ.get('MYSQL_DB', 'eduplatform')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_db_user}:{_db_pass}@{_db_host}/{_db_name}"
    
    # Security overrides
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
