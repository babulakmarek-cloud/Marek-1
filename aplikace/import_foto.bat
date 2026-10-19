@echo off
rem Pretahnete slozku s fotkami na tento soubor (nebo ji zadejte po vyzvani).
rem Zalozi zakazku "Maroldovka VZT" a nahraje fotky. Popisky doplnite v aplikaci.
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
%PY% -m pip install -q -r requirements.txt
set "FOLDER=%~1"
if "%FOLDER%"=="" set /p FOLDER=Cesta ke slozce s fotkami: 
%PY% import_foto.py --folder "%FOLDER%" --job "Maroldovka VZT" --customer "Maroldovka" --area "Strecha" --phase pred
pause
