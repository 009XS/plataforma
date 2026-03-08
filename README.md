# 🎓 Learning Platform - Plataforma Educativa Completa

## 📋 Descripción

Plataforma educativa completa con gestión de usuarios, materias, tareas, recursos, gamificación, chat en tiempo real, videollamadas, foros, calendario y mucho más.

## ✨ Características Principales

### 👥 Gestión de Usuarios
- Múltiples roles: Alumno, Docente, Tutor, Orientador, Admin
- Autenticación tradicional y Google OAuth
- Sistema de permisos por rol

### 📚 Módulo Académico
- Gestión de materias y grupos
- Sistema de tareas con calificaciones
- Recursos educativos (documentos, videos, etc.)
- Exámenes en línea
- Detector de plagio en código

### 🎮 Gamificación
- Sistema de XP y niveles (Bronce → Maestro)
- Educoins (moneda virtual)
- Insignias y logros
- Rachas diarias
- Tienda virtual con avatares y temas
- Ligas semanales

### 💬 Comunicación
- Chat en tiempo real con SocketIO
- Mensajes privados
- Chat grupal por materia
- Notificaciones push (Firebase)
- Notificaciones internas

### 🎥 Colaboración
- Videollamadas integradas
- Pizarra colaborativa
- Foros de discusión con votos
- Sistema de comentarios

### 📊 Análisis y Reportes
- Dashboard con estadísticas
- Predicción de deserción (ML)
- Reportes de rendimiento
- Análisis de progreso
- Exportación de datos

### 🤖 Características Avanzadas
- Tutor IA con OpenAI
- Laboratorios virtuales (Física, Química)
- Retos de código con evaluación automática
- Quiz generados por IA
- Sistema de recomendaciones

### 📅 Organización
- Calendario de eventos
- Recordatorios automáticos
- Gestión de horarios
- Asistencia con QR

## 🛠️ Requisitos Previos

### Software Necesario
- Python 3.8 o superior
- Anaconda (recomendado)
- MySQL 5.7 o superior
- Node.js (opcional, para herramientas de frontend)

### Servicios Externos (Opcionales)
- **Firebase**: Para notificaciones push móviles
- **OpenAI API**: Para tutor IA y generación de contenido
- **Stripe**: Para procesamiento de pagos
- **Google OAuth**: Para autenticación con Google

## 📦 Instalación

### 1. Clonar o Descargar el Proyecto

```bash
cd /home/ubuntu/learning_platform
```

### 2. Crear Entorno Virtual (Anaconda)

```bash
conda create -n learning_platform python=3.9
conda activate learning_platform
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Algunas dependencias científicas (rdkit, pyscf, etc.) pueden requerir instalación específica:

```bash
conda install -c conda-forge rdkit
conda install -c pyscf pyscf
```

### 4. Configurar MySQL

#### Crear Usuario y Base de Datos

```sql
CREATE DATABASE eduplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'eduuser'@'localhost' IDENTIFIED BY 'tu_password_segura';
GRANT ALL PRIVILEGES ON eduplatform.* TO 'eduuser'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar la Aplicación

#### Opción A: Variables de Entorno en tu sistema

Configura variables de entorno del sistema operativo (PowerShell, CMD o panel de Windows).

#### Opción B: Usar Variables de Entorno (Recomendado)

Crear archivo `.env`:

```bash
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
MYSQL_HOST=localhost
MYSQL_USER=eduuser
MYSQL_PASSWORD=tu_password_segura
MYSQL_DB=eduplatform

APP_ENV=production
FLASK_DEBUG=0
TRUST_PROXY=1
SOCKETIO_CORS_ALLOWED_ORIGINS=https://tu-dominio.com
SESSION_TTL_MINUTES=180

EMAIL_FROM=tu_email@gmail.com
EMAIL_USER=tu_email@gmail.com
EMAIL_PASS=tu_app_password

GEMINI_API_KEY=tu_gemini_api_key
STRIPE_SECRET_KEY=sk_test_xxx

GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/google_callback

# Opcional
SUPPORT_EMAIL=soporte@tudominio.com
SCHEDULER_ENABLED=1
ROUTE_DEDUP_KEEP=first
```

La app carga automaticamente `.env` al iniciar (`python-dotenv`).

### 6. Configurar Servicios Externos (Opcional)

#### Firebase (Notificaciones Push)

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Descargar `firebase_admin.json`
3. Colocar en la raíz del proyecto

#### Google OAuth

1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Configurar OAuth 2.0
3. Descargar `client_secret.json`
4. Colocar en la raíz del proyecto

## 🚀 Ejecución

### Iniciar la Aplicación

```bash
python app.py
```

Nota sobre Windows: en Python 3.14 algunos wheels de `gevent`/`mysqlclient` pueden requerir compilador C++. Si falla `pip install -r requirements.txt`, usa Python 3.13 o instala Build Tools de Visual C++.

La aplicación estará disponible en: `http://127.0.0.1:5000`

### Iniciar en Modo Desarrollo

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

### Iniciar con SocketIO

```bash
python app.py
```

## 👤 Usuarios de Prueba

La aplicación NO crea usuarios por defecto. Debes crear usuarios manualmente:

### Crear Usuario Admin (SQL)

```sql
INSERT INTO usuarios (nombre, email, numero_control, curp, tipo_usuario, password_hash, activo)
VALUES (
    'Administrador',
    'admin@eduplatform.com',
    'ADMIN001',
    'AAAA000000HDFRRR00',
    'admin',
    -- Dejar NULL si usas login sin password (solo CURP + numero_control)
    NULL,
    1
);
```

### Login

- **Número de Control**: ADMIN001
- **CURP**: AAAA000000HDFRRR00
- **Rol**: admin

## 📁 Estructura del Proyecto

```
learning_platform/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── config_example.py      # Configuración de ejemplo
├── README.md             # Este archivo
├── uploads/              # Archivos subidos (tareas, recursos, etc.)
├── static/               # CSS, JS, imágenes
├── templates/            # Plantillas HTML
├── firebase_admin.json   # Credenciales Firebase (opcional)
└── client_secret.json    # Credenciales Google OAuth (opcional)
```

## 🔧 Configuración de Producción

### Usar un Servidor WSGI (Gunicorn)

```bash
pip install gunicorn
gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 app:app
```

### Configurar Nginx

```nginx
server {
    listen 80;
    server_name tu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:8000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### SSL con Let's Encrypt

```bash
sudo certbot --nginx -d tu_dominio.com
```

## 🐛 Solución de Problemas

### Error de Conexión a MySQL

```
OperationalError: (2002, "Can't connect to local MySQL server")
```

**Solución**: Verificar que MySQL esté corriendo:

```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

### Error de Dependencias Científicas

```
ModuleNotFoundError: No module named 'rdkit'
```

**Solución**: Instalar con conda:

```bash
conda install -c conda-forge rdkit
```

### Firebase no Inicializado

```
⚠️  firebase_admin.json no encontrado
```

**Solución**: Las notificaciones push seguirán funcionando con logging. Para habilitarlas, configurar Firebase.

### Puerto 5000 en Uso

```
OSError: [Errno 98] Address already in use
```

**Solución**: Cambiar puerto en `app.py`:

```python
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
```

## 📚 Documentación Adicional

### APIs Disponibles

Ver documentación completa en: `/api/docs` (cuando esté implementado)

### Módulos Principales

- **Autenticación**: Login, OAuth, sesiones
- **Usuarios**: CRUD, roles, permisos
- **Académico**: Materias, tareas, calificaciones
- **Recursos**: Subida, descarga, visualización
- **Gamificación**: XP, niveles, insignias, tienda
- **Comunicación**: Chat, notificaciones, mensajes
- **Reportes**: Análisis, exportación, predicciones

## 🤝 Contribución

Este es un proyecto educativo. Para mejoras:

1. Fork del proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es para fines educativos.

## 📧 Contacto

Para soporte: cecytemhuixquilucan32@gmail.com

## ⚠️ Notas Importantes

1. **Base de Datos**: Se crea automáticamente al iniciar la aplicación
2. **Uploads**: Directorio se crea automáticamente
3. **Servicios Externos**: Son OPCIONALES - la aplicación funciona sin ellos
4. **Localhost**: Este servidor Flask corre en localhost de la máquina donde se ejecuta, NO en tu máquina local
5. **Credenciales**: Cambiar TODAS las credenciales por defecto en producción

## 🎯 Próximos Pasos

1. Configurar MySQL
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar credenciales en `app.py`
4. Ejecutar: `python app.py`
5. Abrir navegador: `http://127.0.0.1:5000`
6. Crear primer usuario admin (SQL)
7. ¡Empezar a usar la plataforma!

---

**¡Éxito con tu plataforma educativa! 🚀**
