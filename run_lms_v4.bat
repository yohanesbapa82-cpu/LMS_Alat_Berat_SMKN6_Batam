@echo off
title LMS ALAT BERAT V4 LAUNCHER
color 0A

echo ==========================================
echo     LMS ALAT BERAT V4 - AUTO RUNNER
echo ==========================================

REM ================================
REM MASUK KE FOLDER PROJECT
REM ================================
cd /d "C:\Users\DELL\LMS_ALAT_BERAT_V4"

if %errorlevel% neq 0 (
echo [ERROR] Folder tidak ditemukan!
pause
exit /b
)

REM ================================
REM CEK PYTHON
REM ================================
where python >nul 2>nul
if %errorlevel% neq 0 (
echo [INFO] Python tidak terdeteksi, mencoba 'py'...
set PYTHON_CMD=py
) else (
set PYTHON_CMD=python
)

REM ================================
REM AKTIFKAN VIRTUAL ENV (JIKA ADA)
REM ================================
if exist venv\Scripts\activate (
echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate
)

REM ================================
REM INSTALL DEPENDENCY
REM ================================
if exist requirements.txt (
echo [INFO] Menginstall dependency...
%PYTHON_CMD% -m pip install -r requirements.txt
)

REM ================================
REM DETEKSI JENIS PROJECT
REM ================================

echo [INFO] Mendeteksi jenis aplikasi...

findstr /C:"streamlit" main.py >nul
if %errorlevel%==0 (
echo [INFO] Mode Streamlit terdeteksi
streamlit run main.py
goto END
)

REM Default: Python biasa
echo [INFO] Menjalankan sebagai Python script
%PYTHON_CMD% main.py

:END
echo.
echo ==========================================
echo [SELESAI] Program berhenti / error terjadi
echo ==========================================
pause
