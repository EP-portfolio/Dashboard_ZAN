@echo off
REM Script de lancement du Dashboard avec acces reseau
REM ====================================================

echo ========================================
echo   DASHBOARD ZAN - Lancement Reseau
echo ========================================
echo.

REM Changer vers le repertoire du Dashboard
cd /d "%~dp0"

REM Afficher l'adresse IP locale
echo Recuperation de l'adresse IP locale...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"Adresse IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo.
    echo Votre adresse IP locale: !IP!
    echo.
)

REM Lancer Streamlit avec acces reseau
echo Lancement du Dashboard...
echo.
echo Le Dashboard sera accessible sur:
echo   - Local: http://localhost:8501
echo   - Reseau: http://%IP%:8501
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

streamlit run app.py --server.address 0.0.0.0 --server.port 8501

pause

