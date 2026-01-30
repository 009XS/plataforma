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
    ) else (
        REM Agregar MySQL al PATH para esta sesión
        set "PATH=!MYSQL_PATH!;%PATH%"
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

set "VENV_DIR=%~dp0venv"
set "PYTHON_EXE=python"
set "PIP_EXE=pip"

if exist "%VENV_DIR%" (
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
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
    set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
    set "PIP_EXE=%VENV_DIR%\Scripts\pip.exe"
    echo     ✓ Entorno virtual activado
) else (
    echo     ⚠️  Usando Python global
)

"%PYTHON_EXE%" -m pip install --upgrade pip setuptools wheel --quiet
echo     ✓ pip, setuptools y wheel actualizados
echo.

:: ============================================================================
:: STEP 7: Install Core Dependencies First
:: ============================================================================
echo [7/10] Instalando dependencias del proyecto...
echo.

if not exist "requirements.txt" (
    echo     ✗ No se encontró requirements.txt
    echo     Asegúrate de ejecutar este script desde la carpeta del proyecto.
    pause
    exit /b 1
)

echo     Instalando requirements.txt (esto puede tardar unos minutos)...
"%PYTHON_EXE%" -m pip install -r requirements.txt --no-warn-script-location > install_log.txt 2>&1
if %errorLevel% neq 0 (
    echo     ⚠️  Hubo errores durante la instalación.
    echo     Revisa install_log.txt para más detalles.
    pause
) else (
    echo     ✓ Requerimientos instalados correctamente.
)
echo.

:: ============================================================================
:: STEP 8: Quick Checks (optional files)
:: ============================================================================
echo [8/10] Verificando archivos opcionales...
if exist "client_secret.json" (
    echo     ✓ client_secret.json encontrado
) else (
    echo     ⚠️  client_secret.json no encontrado (Google OAuth deshabilitado)
)
if exist "firebase_admin.json" (
    echo     ✓ firebase_admin.json encontrado
) else (
    echo     ⚠️  firebase_admin.json no encontrado (Firebase deshabilitado)
)
echo.

:: ============================================================================
:: STEP 9: Setup Configuration Files
:: ============================================================================
echo [9/10] Configurando archivos de configuración...
if exist "config.py" (
    echo     ✓ config.py ya existe
) else (
    echo     ⚠️  config.py no encontrado
)
if exist ".env" (
    echo     ✓ .env ya existe
) else (
    echo     ℹ️  .env no existe (opcional)
)
echo.

:: ============================================================================
:: STEP 10: Create/Verify Database
:: ============================================================================
echo [10/10] Verificando base de datos MySQL...

set "MYSQL_EXE="
for /f "delims=" %%i in ('where mysql 2^>nul') do (
    if not defined MYSQL_EXE set "MYSQL_EXE=%%i"
)

if defined MYSQL_EXE (
    echo     ✓ MySQL detectado: %MYSQL_EXE%
    set "MYSQL_USER=root"
    set /p MYSQL_USER=Usuario MySQL (default root): 
    if "%MYSQL_USER%"=="" set "MYSQL_USER=root"
    set /p MYSQL_PASS=Contraseña MySQL (deja vacío si no tiene): 

    if "%MYSQL_PASS%"=="" (
        set "MYSQL_AUTH=-u %MYSQL_USER%"
    ) else (
        set "MYSQL_AUTH=-u %MYSQL_USER% -p%MYSQL_PASS%"
    )

    "%MYSQL_EXE%" %MYSQL_AUTH% -e "CREATE DATABASE IF NOT EXISTS eduplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>nul
    if %errorLevel% equ 0 (
        echo     ✓ Base de datos 'eduplatform' verificada/creada
    ) else (
        echo     ⚠️  No se pudo verificar la base de datos automáticamente.
        echo     Ejecuta manualmente:
        echo        mysql -u %MYSQL_USER% -p
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
echo   2. Crear Usuario Tutor
echo   3. Sembrar Base de Datos
echo   4. Probar Conexión Gemini AI
echo   5. Verificar Endpoints
echo   6. Volver al Menú Principal
echo.
set /p U_OP="Elige una opción: "

if "%U_OP%"=="1" (
    echo Ejecutando create_test_user.py...
    "%PYTHON_EXE%" scripts/create_test_user.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="2" (
    echo Ejecutando create_tutor_user.py...
    "%PYTHON_EXE%" scripts/create_tutor_user.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="3" (
    echo Ejecutando seed_db.py...
    "%PYTHON_EXE%" seed_db.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="4" (
    echo Ejecutando test_gemini.py...
    "%PYTHON_EXE%" tests/test_gemini.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="5" (
    echo Ejecutando verify_endpoints.py...
    "%PYTHON_EXE%" tests/verify_endpoints.py
    pause
    goto UTILITIES
)
if "%U_OP%"=="6" goto MENU_PRINCIPAL
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

"%PYTHON_EXE%" app.py

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