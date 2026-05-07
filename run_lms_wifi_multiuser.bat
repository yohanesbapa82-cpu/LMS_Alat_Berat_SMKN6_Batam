@echo off
title LMS WIFI SERVER - MULTI USER
color 0A

echo ==========================================
echo     LMS SERVER WIFI (MULTI USER)
echo ==========================================

REM ================================
REM MASUK KE FOLDER PROJECT
REM ================================
cd /d "C:\Users\DELL\LMS_ALAT_BERAT_V4"

REM ================================
REM CONFIG
REM ================================
set PORT=8501
set HOST=0.0.0.0

REM ================================
REM DETEKSI PYTHON
REM ================================
where python >nul 2>nul
if %errorlevel% neq 0 (
set PYTHON_CMD=py
) else (
set PYTHON_CMD=python
)

REM ================================
REM AKTIFKAN VENV (JIKA ADA)
REM ================================
if exist venv\Scripts\activate (
call venv\Scripts\activate
)

REM ================================
REM FIREWALL (BUKA PORT)
REM ================================
netsh advfirewall firewall add rule name="LMS_WIFI_8501" dir=in action=allow protocol=TCP localport=%PORT% >nul 2>nul

REM ================================
REM AMBIL IP LOKAL
REM ================================
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (
set IP=%%a
goto :done
)
:done
set IP=%IP:~1%

echo.
echo ==========================================
echo LMS SERVER BERJALAN DI:
echo http://%IP%:%PORT%
echo ==========================================
echo AKSES DARI HP / LAPTOP LAIN:
echo http://%IP%:%PORT%
echo ==========================================
echo.

REM ================================
REM JALANKAN STREAMLIT (MODE LAN)
REM ================================
streamlit run main.py ^
--server.address %HOST% ^
--server.port %PORT% ^
--server.headless true ^
--server.enableCORS false ^
--server.enableXsrfProtection false ^
--browser.gatherUsageStats false

pause
