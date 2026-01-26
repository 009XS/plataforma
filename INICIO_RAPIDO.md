# 🚀 GUÍA DE INICIO RÁPIDO - Learning Platform

## ⚡ Para Comenzar en 5 Minutos

### 1️⃣ Requisitos Previos
```bash
# Verificar Python
python3 --version  # Debe ser 3.8+

# Verificar MySQL
mysql --version
```

### 2️⃣ Instalación Rápida

#### Opción A: Instalación Automática (Recomendado)
```bash
cd /home/ubuntu/learning_platform
chmod +x install.sh
./install.sh
```

#### Opción B: Instalación Manual
```bash
# Crear entorno virtual (opcional pero recomendado)
conda create -n learning_platform python=3.9 -y
conda activate learning_platform

# O con venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Configurar Base de Datos

```sql
-- Conectar a MySQL
mysql -u root -p

-- Crear base de datos
CREATE DATABASE eduplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Crear usuario (opcional)
CREATE USER 'eduuser'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON eduplatform.* TO 'eduuser'@'localhost';
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

### 4️⃣ Configurar Credenciales

Edita `app.py` (líneas 105-108):

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'          # Tu usuario
app.config['MYSQL_PASSWORD'] = ''          # Tu contraseña
app.config['MYSQL_DB'] = 'eduplatform'
```

**O** crea archivo `.env`:
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

### 5️⃣ Iniciar la Aplicación

#### Opción A: Script de Inicio
```bash
./start.sh
```

#### Opción B: Directo
```bash
python3 app.py
```

### 6️⃣ Abrir en Navegador

```
http://127.0.0.1:5000
```

---

## 👤 Crear Primer Usuario Admin

La base de datos se crea automáticamente al iniciar, pero SIN usuarios por defecto.

### Opción A: Desde MySQL
```sql
USE eduplatform;

INSERT INTO usuarios (
    nombre, email, numero_control, curp, 
    tipo_usuario, activo, semestre
) VALUES (
    'Admin Sistema',
    'admin@eduplatform.com',
    'ADMIN001',
    'AAAA000000HDFRRR00',
    'admin',
    1,
    '2025-1'
);
```

### Opción B: Desde la Aplicación (Futuro)
Proximamente habrá un script de seed para crear usuarios de prueba.

### 📝 Login
- **Número de Control**: ADMIN001
- **CURP**: AAAA000000HDFRRR00
- **Rol**: admin

---

## 🔧 Solución Rápida de Problemas

### ❌ Error: Can't connect to MySQL
```bash
# Verificar que MySQL esté corriendo
sudo systemctl status mysql

# Iniciarlo si no está corriendo
sudo systemctl start mysql
```

### ❌ Error: ModuleNotFoundError
```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Para dependencias científicas con conda
conda install -c conda-forge rdkit
```

### ❌ Puerto 5000 en uso
Edita `app.py` (última línea):
```python
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)  # Cambiar puerto
```

### ❌ Error de permisos en MySQL
```sql
-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON eduplatform.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📚 Documentación Completa

Para información detallada, consulta:

- **README.md**: Documentación completa
- **CORRECCIONES.md**: Lista de todas las correcciones aplicadas
- **config_example.py**: Ejemplo de configuración avanzada

---

## 🎯 Características Principales

### Para Alumnos
- ✅ Ver tareas y entregarlas
- ✅ Consultar calificaciones
- ✅ Acceder a recursos educativos
- ✅ Chat con compañeros
- ✅ Sistema de gamificación (XP, insignias)

### Para Docentes
- ✅ Crear y calificar tareas
- ✅ Subir recursos
- ✅ Gestionar materias
- ✅ Comunicarse con alumnos
- ✅ Ver reportes de rendimiento

### Para Administradores
- ✅ Gestión de usuarios
- ✅ Reportes y estadísticas
- ✅ Configuración del sistema
- ✅ Logs de auditoría

---

## 🔐 Servicios Opcionales

La aplicación funciona perfectamente sin estos servicios, pero puedes configurarlos para funcionalidades adicionales:

### Firebase (Notificaciones Push)
1. Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Descargar `firebase_admin.json`
3. Colocar en raíz del proyecto

### Google OAuth
1. Configurar en [Google Cloud Console](https://console.cloud.google.com/)
2. Descargar `client_secret.json`
3. Colocar en raíz del proyecto

### OpenAI (Tutor IA)
1. Obtener API key en [OpenAI](https://platform.openai.com/)
2. Agregar a `app.py` o `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

---

## 📞 Soporte

**Email**: cecytemhuixquilucan32@gmail.com

---

## ⚠️ Notas Importantes

1. 🔒 **NUNCA** subir a GitHub con credenciales reales
2. 🌐 Este servidor corre en **localhost de ESTA máquina**
3. 🔧 Cambiar `SECRET_KEY` en producción
4. 🛡️ Usar HTTPS en producción
5. 📊 Las tablas se crean automáticamente al iniciar

---

## ✅ Checklist de Verificación

Antes de iniciar, verifica:

- [ ] Python 3.8+ instalado
- [ ] MySQL instalado y corriendo
- [ ] Base de datos `eduplatform` creada
- [ ] Credenciales configuradas en `app.py` o `.env`
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Puerto 5000 disponible (o cambiado)

---

## 🎉 ¡Listo!

Si seguiste todos los pasos, tu plataforma debería estar funcionando en:

```
http://127.0.0.1:5000
```

### Próximos pasos:
1. Crear tu primer usuario admin (ver arriba)
2. Hacer login
3. Explorar las funcionalidades
4. Crear usuarios adicionales (alumnos, docentes)
5. ¡Empezar a usar la plataforma!

---

**¿Problemas?** Consulta `README.md` o el archivo `CORRECCIONES.md` para más detalles.

**¡Éxito! 🚀**
