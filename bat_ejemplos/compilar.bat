@echo off
title Creando ejecutable
set archivo=%1
set archivospec=%archivo:~,-3%spec
set archivopy=%archivo:~,-3%py
echo Compilando %archivospec%
"C:\\Users\\Edouard\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pyinstaller.exe" --noconfirm %archivospec%
if %ERRORLEVEL% neq 0 (goto ProcessError)
goto salida_bien
:ProcessError
echo \nERROR con el %archivospec%, compilando %archivopy% en su lugar\n\n
"C:\\Users\\Edouard\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pyinstaller.exe" --noconfirm %archivopy%

if %ERRORLEVEL% neq 0 (goto salida_mal)

:salida_bien
echo Todo listo
goto fin

:salida_mal
echo Hubo un error
goto fin


:fin
pause
