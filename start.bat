@echo off
echo =========================================
echo   SmartHome AI Monitor - Lancement
echo =========================================
echo.

REM Ajouter Docker au PATH
set PATH=%PATH%;C:\Program Files\Docker\Docker\resources\bin;C:\ProgramData\DockerDesktop\version-bin

REM Vérifier si Docker est disponible en ligne de commande
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Commande docker introuvable. Verifier l'installation de Docker Desktop.
    pause
    exit /b 1
)

REM Vérifier si le daemon Docker tourne
docker info >nul 2>&1
if "%errorlevel%" == "0" goto docker_ready

echo [INFO] Docker Desktop n'est pas demarre. Lancement en cours...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo [INFO] En attente que Docker soit pret (peut prendre 30 a 60 secondes)...

:wait_loop
timeout /t 5 /nobreak >nul
docker info >nul 2>&1
if "%errorlevel%" neq "0" goto wait_loop

echo [INFO] Docker pret !

:docker_ready

echo.
echo [1/2] Arret des anciens conteneurs...
docker compose down 2>nul

echo.
echo [2/2] Construction et lancement de tous les services...
docker compose up --build -d

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Echec du lancement. Affichage des logs...
    docker compose logs --tail=20
    pause
    exit /b 1
)

echo.
echo [3/3] Synchronisation des flows Node-RED (pipeline IA)...
timeout /t 15 /nobreak >nul
docker cp flows.json mynodered:/data/flows.json
docker restart mynodered
echo [OK] Flows Node-RED mis a jour et pipeline IA active !

echo.
echo =========================================
echo   Tous les services sont lances !
echo =========================================
echo.
echo   Dashboard Web  :  http://localhost:8080
echo   Node-RED       :  http://localhost:1880
echo   Node-RED /ui   :  http://localhost:1880/ui
echo   EMQX Admin     :  http://localhost:18083
echo   IA Python      :  http://localhost:5000/status
echo.
echo   Logs en direct :  docker compose logs -f
echo =========================================
echo.

REM Ouvrir automatiquement le dashboard dans le navigateur
timeout /t 3 /nobreak >nul
start http://localhost:8080

pause
