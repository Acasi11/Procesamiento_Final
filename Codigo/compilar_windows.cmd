@echo off
rem Ejecutar en el simbolo de herramientas nativas x64 de Visual Studio.
setlocal
cd /d "%~dp0"
python preparar.py || exit /b 1
cl /nologo /TC /O1 /GS- iniciar.c /link /entry:iniciar /subsystem:windows /nodefaultlib kernel32.lib user32.lib shell32.lib /out:..\Ejecutable\LaboratorioFFT.exe
exit /b %errorlevel%
