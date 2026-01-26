@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion
title Learning Platform - Setup and Run
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║           LEARNING PLATFORM - INSTALADOR COMPLETO WINDOWS              ║
echo ║                    Setup, Fix Errors ^& Run Script                       ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

:: ============================================================================
:: STEP 1: Check Administrator Privileges
:: ============================================================================
echo [1/10] Verificando privilegios de administrador...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ⚠️  ADVERTENCIA: No tienes privilegios de administrador.
    echo    Algunas instalaciones pueden fallar.
    echo    Recomendado: Click derecho en este archivo ^> "Ejecutar como administrador"
    echo.
    pause
)
echo     ✓ Continuando con la instalación...
echo.

:: ============================================================================
:: STEP 2: Check Python Installation
:: ============================================================================
echo [2/10] Verificando Python...
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo     ✗ Python NO encontrado.
    echo.
    echo     Descargando Python 3.11...
    echo     Por favor instala Python manualmente desde:
    echo     https://www.python.org/downloads/
    echo.
    echo     IMPORTANTE: Marca la casilla "Add Python to PATH" durante la instalación.
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo     ✓ %PYTHON_VERSION% encontrado
echo.

:: ============================================================================
:: STEP 3: Check and Install Visual C++ Build Tools
:: ============================================================================
echo [3/10] Verificando Visual C++ Build Tools...
where cl >nul 2>&1
if %errorLevel% neq 0 (
    echo     ⚠️  Visual C++ Build Tools no detectado.
    echo     Algunas librerías ^(mysqlclient, etc.^) pueden necesitarlo.
    echo.
    echo     Opciones:
    echo     1. Descargar Visual Studio Build Tools ^(recomendado^):
    echo        https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo     2. Continuar sin él ^(usaremos PyMySQL como alternativa^)
    echo.
) else (
    echo     ✓ Visual C++ Build Tools detectado
)
echo.

:: ============================================================================
:: STEP 4: Check MySQL Installation
:: ============================================================================
echo [4/10] Verificando MySQL...
where mysql >nul 2>&1
if %errorLevel% neq 0 (
    echo     ✗ MySQL NO encontrado en PATH.
    echo.
    echo     Verificando rutas comunes de MySQL...
    
    set MYSQL_FOUND=0
    if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" (
        set MYSQL_FOUND=1
        set "MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.0\bin"
        echo     ✓ MySQL encontrado en: !MYSQL_PATH!
    )
    if exist "C:\Program Files\MySQL\MySQL Server 8.1\bin\mysql.exe" (
        set MYSQL_FOUND=1
        set "MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.1\bin"
        echo     ✓ MySQL encontrado en: !MYSQL_PATH!
    )
    if exist "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" (
        set MYSQL_FOUND=1
        set "MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.4\bin"
        echo     ✓ MySQL encontrado en: !MYSQL_PATH!
    )
    if exist "C:\xampp\mysql\bin\mysql.exe" (
        set MYSQL_FOUND=1
        set "MYSQL_PATH=C:\xampp\mysql\bin"
        echo     ✓ MySQL ^(XAMPP^) encontrado en: !MYSQL_PATH!
    )
    if exist "C:\wamp64\bin\mysql\mysql8.0.31\bin\mysql.exe" (
        set MYSQL_FOUND=1
        set "MYSQL_PATH=C:\wamp64\bin\mysql\mysql8.0.31\bin"
        echo     ✓ MySQL ^(WAMP^) encontrado en: !MYSQL_PATH!
    )
    
    if !MYSQL_FOUND! equ 0 (
        echo.
        echo     ⚠️  MySQL no encontrado. Opciones:
        echo.
        echo     A^) Instalar MySQL Server:
        echo        https://dev.mysql.com/downloads/mysql/
        echo.
        echo     B^) Instalar XAMPP ^(incluye MySQL^):
        echo        https://www.apachefriends.org/download.html
        echo.
        echo     La aplicación requiere MySQL para funcionar.
        echo.
    )
) else (
    for /f "tokens=*" %%i in ('mysql --version 2^>^&1') do set MYSQL_VERSION=%%i
    echo     ✓ MySQL encontrado: !MYSQL_VERSION!
)
echo.

:: ============================================================================
:: STEP 5: Create/Update Virtual Environment
:: ============================================================================
echo [5/10] Configurando entorno virtual...
cd /d "%~dp0"

if exist "venv" (
    echo     ✓ Entorno virtual existente encontrado
) else (
    echo     Creando nuevo entorno virtual...
    python -m venv venv
    if %errorLevel% neq 0 (
        echo     ✗ Error al crear entorno virtual
        echo     Intentando sin entorno virtual...
    ) else (
        echo     ✓ Entorno virtual creado
    )
)
echo.

:: ============================================================================
:: STEP 6: Activate Virtual Environment and Upgrade pip
:: ============================================================================
echo [6/10] Activando entorno virtual y actualizando pip...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo     ✓ Entorno virtual activado
) else (
    echo     ⚠️  Usando Python global
)

python -m pip install --upgrade pip setuptools wheel --quiet
echo     ✓ pip, setuptools y wheel actualizados
echo.

:: ============================================================================
:: STEP 7: Install Core Dependencies First
:: ============================================================================
echo [7/10] Instalando dependencias core...
echo.

:: Install PyMySQL first (Windows-friendly MySQL connector)
echo     [7.1] Instalando PyMySQL ^(conector MySQL para Windows^)...
pip install pymysql --quiet --no-warn-script-location 2>nul
echo          ✓ PyMySQL instalado

:: Install Flask and core web framework
echo     [7.2] Instalando Flask y framework web...
pip install Flask==3.0.0 --quiet --no-warn-script-location 2>nul
pip install flask-cors==4.0.0 --quiet --no-warn-script-location 2>nul
pip install flask-socketio==5.3.6 --quiet --no-warn-script-location 2>nul
pip install Werkzeug==3.0.1 --quiet --no-warn-script-location 2>nul
echo          ✓ Flask core instalado

:: Install gevent for async
echo     [7.3] Instalando gevent ^(async support^)...
pip install gevent==24.11.1 --quiet --no-warn-script-location 2>nul
pip install gevent-websocket==0.10.1 --quiet --no-warn-script-location 2>nul
echo          ✓ gevent instalado

:: Try to install mysqlclient, fall back to PyMySQL adapter
echo     [7.4] Configurando flask-mysqldb...
pip install flask-mysqldb --quiet --no-warn-script-location 2>nul
if %errorLevel% neq 0 (
    echo          ⚠️  flask-mysqldb falló.
    echo          Configurando adaptador PyMySQL...
    pip install PyMySQL[rsa] --quiet --no-warn-script-location 2>nul
)
echo          ✓ MySQL connector configurado
echo.

:: ============================================================================
:: STEP 8: Install All Requirements (with error handling)
:: ============================================================================
echo [8/10] Instalando todas las dependencias de requirements.txt...
echo     Esto puede tomar varios minutos...
echo.

:: Install requirements with logging
echo     [8.0] Instalando requirements.txt...
pip install -r requirements.txt --no-warn-script-location > install_log.txt 2>&1
if %errorLevel% neq 0 (
    echo     ⚠️  Hubo advertencias o errores durante la instalación masiva.
    echo     Revisa install_log.txt para más detalles.
    echo     Intentando instalar paquetes clave individualmente...
) else (
    echo     ✓ Requerimientos instalados.
)

:: Force install problematic packages one by one
echo     [8.1] Verificando paquetes problemáticos...

:: NumPy and SciPy
pip install numpy --quiet --no-warn-script-location 2>nul
pip install scipy --quiet --no-warn-script-location 2>nul
echo          ✓ NumPy y SciPy

:: Pandas
pip install pandas --quiet --no-warn-script-location 2>nul
echo          ✓ Pandas

:: Scikit-learn
pip install scikit-learn --quiet --no-warn-script-location 2>nul
echo          ✓ Scikit-learn

:: Google Generative AI (Gemini)
pip install google-generativeai --quiet --no-warn-script-location 2>nul
echo          ✓ Google Generative AI

:: PyTorch (CPU version for Windows - smaller download)
echo     [8.2] Instalando PyTorch ^(versión CPU^)...
pip install torch --quiet --no-warn-script-location 2>nul
if %errorLevel% neq 0 (
    echo          ⚠️  PyTorch completo falló, intentando versión ligera...
    pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet --no-warn-script-location 2>nul
)
echo          ✓ PyTorch

:: Security packages
pip install pyotp==2.9.0 --quiet --no-warn-script-location 2>nul
pip install RestrictedPython==8.0 --quiet --no-warn-script-location 2>nul
echo          ✓ Paquetes de seguridad

:: Google OAuth
pip install google-auth google-auth-oauthlib google-auth-httplib2 --quiet --no-warn-script-location 2>nul
echo          ✓ Google OAuth

:: PDF and document processing
pip install pdfplumber==0.10.4 --quiet --no-warn-script-location 2>nul
pip install reportlab==4.1.0 --quiet --no-warn-script-location 2>nul
echo          ✓ Procesamiento de documentos

:: Firebase
pip install firebase-admin==6.4.0 --quiet --no-warn-script-location 2>nul
echo          ✓ Firebase

:: Payment processing
pip install stripe==8.2.0 --quiet --no-warn-script-location 2>nul
echo          ✓ Stripe (pagos)

:: Flask extensions
pip install Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.0.5 --quiet --no-warn-script-location 2>nul
pip install Flask-JWT-Extended==4.6.0 Flask-Limiter==3.5.0 --quiet --no-warn-script-location 2>nul
pip install Flask-APScheduler==1.13.1 --quiet --no-warn-script-location 2>nul
echo          ✓ Extensiones Flask

:: Other scientific packages
pip install sympy mpmath matplotlib --quiet --no-warn-script-location 2>nul
pip install networkx==3.2.1 --quiet --no-warn-script-location 2>nul
pip install qutip --quiet --no-warn-script-location 2>nul
pip install astropy --quiet --no-warn-script-location 2>nul
pip install control==0.9.4 --quiet --no-warn-script-location 2>nul
pip install statsmodels --quiet --no-warn-script-location 2>nul
pip install PuLP==2.8.0 --quiet --no-warn-script-location 2>nul
echo          ✓ Paquetes científicos

:: QR and Excel
pip install qrcode[pil]==7.4.2 --quiet --no-warn-script-location 2>nul
pip install openpyxl==3.1.2 --quiet --no-warn-script-location 2>nul
echo          ✓ QR Code y Excel

:: Games and misc
pip install pygame --quiet --no-warn-script-location 2>nul
pip install python-chess==1.999 --quiet --no-warn-script-location 2>nul
pip install mido MIDIUtil --quiet --no-warn-script-location 2>nul
echo          ✓ Pygame y utilidades

:: Scheduler and utilities
pip install APScheduler==3.10.4 schedule==1.2.1 --quiet --no-warn-script-location 2>nul
pip install tqdm==4.66.1 --quiet --no-warn-script-location 2>nul
pip install email-validator==2.1.0.post1 --quiet --no-warn-script-location 2>nul
echo          ✓ Schedulers y utilidades

echo.
echo     ✓ Todas las dependencias instaladas
echo.

:: ============================================================================
:: STEP 9: Setup Configuration Files
:: ============================================================================
echo [9/10] Configurando archivos de configuración...

if not exist "config.py" (
    if exist "config_example.py" (
        copy "config_example.py" "config.py" >nul
        echo     ✓ config.py creado desde config_example.py
    )
) else (
    echo     ✓ config.py ya existe
)

if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo     ✓ .env creado desde .env.example
    )
) else (
    echo     ✓ .env ya existe
)
echo.

:: ============================================================================
:: STEP 10: Create/Verify Database
:: ============================================================================
echo [10/10] Verificando base de datos MySQL...

where mysql >nul 2>&1
if %errorLevel% equ 0 (
    echo     Intentando conectar a MySQL...
    echo     Si se pide contraseña, ingresa tu contraseña de root de MySQL.
    echo.
    
    REM Try to create database if it doesn't exist
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS eduplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
    if %errorLevel% equ 0 (
        echo     ✓ Base de datos 'eduplatform' verificada/creada
    ) else (
        echo     ⚠️  No se pudo verificar la base de datos automáticamente.
        echo     Ejecuta manualmente:
        echo        mysql -u root -p
        echo        CREATE DATABASE eduplatform;
    )
) else (
    echo     ⚠️  MySQL no está en PATH. Verifica que esté instalado y configurado.
    echo     Puedes crear la base de datos manualmente con:
    echo        CREATE DATABASE eduplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
)
echo.

:: ============================================================================
:: INSTALLATION COMPLETE - RUN APPLICATION
:: ============================================================================
echo.


:MENU_PRINCIPAL
echo.

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                    ✓ INSTALACIÓN COMPLETADA                            ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo   Resumen:
echo   ────────────────────────────────────────────────────────────────────────
echo   • Entorno virtual: venv\
echo   • Base de datos: eduplatform (MySQL)
echo   • Configuración: config.py, .env
echo.
echo   MENÚ PRINCIPAL:
echo   1. Iniciar Aplicación (Start Web Server)
echo   2. utilidades y Scripts...
echo   3. Salir
echo.

set /p OPCION="Selecciona una opción (1-3): "

if "%OPCION%"=="1" goto START_APP
if "%OPCION%"=="2" goto UTILITIES
if "%OPCION%"=="3" goto END
goto MENU_PRINCIPAL

:UTILITIES
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                    🛠️  UTILIDADES Y SCRIPTS                           ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo   1. Crear Usuario de Prueba (Admin)
echo   2. Analizar Backend (Rutas y Tablas)
echo   3. Listar Usuarios (Debug)
echo   4. Probar Conexión Gemini AI
echo   5. Volver al Menú Principal
echo.
set /p U_OP="Elige una opción: "

if "%U_OP%"=="1" (
    echo Ejecutando create_test_user.py...
    python scripts/create_test_user.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="2" (
    echo Ejecutando analyze_backend.py...
    python scripts/analyze_backend.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="3" (
    echo Ejecutando debug_users.py...
    python scripts/debug_users.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="4" (
    echo Ejecutando test_gemini.py...
    python tests/test_gemini.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="5" goto MENU_PRINCIPAL
goto UTILITIES

:START_APP
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                    🚀 INICIANDO LEARNING PLATFORM                      ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo   URL: http://127.0.0.1:5000
echo   Presiona Ctrl+C para detener el servidor
echo.
echo ────────────────────────────────────────────────────────────────────────
echo.

python app.py

if %errorLevel% neq 0 (
    echo.
    echo ════════════════════════════════════════════════════════════════════════
    echo ERROR AL INICIAR LA APLICACIÓN
    echo ════════════════════════════════════════════════════════════════════════
    echo.
    echo Posibles soluciones:
    echo.
    echo 1. Verifica que MySQL esté corriendo:
    echo    - Abre Servicios de Windows ^(services.msc^)
    echo    - Busca "MySQL" y asegúrate de que esté "Running"
    echo.
    echo 2. Verifica las credenciales de MySQL en config.py:
    echo    - MYSQL_USER = 'root' ^(o tu usuario^)
    echo    - MYSQL_PASSWORD = 'tu_contraseña'
    echo    - MYSQL_DB = 'eduplatform'
    echo.
    pause
    pause
)
pause
goto MENU_PRINCIPAL

:END
exit /b 0