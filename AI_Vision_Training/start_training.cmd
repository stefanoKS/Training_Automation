@echo off
setlocal
for /f "tokens=2 delims=:" %%C in ('chcp') do set "ORIGINAL_CODEPAGE=%%C"
chcp 65001 >nul
cd /d "%~dp0"
if errorlevel 1 goto folder_error
if not exist "%~dp0.venv\Scripts\python.exe" goto missing_environment

set "PATH=%~dp0.venv\Scripts;%PATH%"
"%~dp0.venv\Scripts\python.exe" -m jupyter lab
set "LAUNCH_EXIT=%ERRORLEVEL%"
if "%LAUNCH_EXIT%"=="0" goto finish
echo JupyterLab を起動できませんでした。上のエラーと START_HERE.md を確認してください。
echo JupyterLab failed. Check the error above and START_HERE.md.
goto failure

:folder_error
set "LAUNCH_EXIT=1"
echo 教材フォルダを開けません。START_HERE.md を確認してください。
echo Cannot open the course folder. See START_HERE.md.
goto failure

:missing_environment
set "LAUNCH_EXIT=1"
echo 基本環境がありません。START_HERE.md の準備手順を先に完了してください。
echo Base environment missing. Complete START_HERE.md before launching.

:failure
pause

:finish
chcp %ORIGINAL_CODEPAGE% >nul
endlocal & exit /b %LAUNCH_EXIT%
