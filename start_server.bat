@echo off
title ICHTP Server
echo =========================================
echo       Starting ICHTP Local Server
echo =========================================
echo.
echo Please wait while the server is starting...
echo Once started, you can open your browser.
echo Press Ctrl+C or close this window to stop the server.
echo.

:: 檢查是否有虛擬環境，若有則自動啟用
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

:: 啟動伺服器 (綁定 0.0.0.0 讓同網域的區網也可以連線)
python manage.py run --host 0.0.0.0

pause
