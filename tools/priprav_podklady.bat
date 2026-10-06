@echo off
rem Pripravi ciste podklady pro MH BIM ze vsech DXF v aktualni slozce.
rem Pouziti: priprav_podklady.bat X,Y      (X,Y = spolecny vztazny bod v mm)
rem Vystup: slozka mhbim\ s *_heiz.dxf a *_arch.dxf.  Potreba: Python + pip install ezdxf
if "%~1"=="" ( echo Zadej vztazny bod X,Y v mm, napr. priprav_podklady.bat 12500,40300 & exit /b 1 )
if not exist mhbim mkdir mhbim
for %%F in (*.dxf) do (
  echo === %%F
  python "%~dp0mhbim_podklad.py" "%%F" "mhbim\%%~nF_arch.dxf" --profil arch --posun %1 --bez-srafy
  python "%~dp0mhbim_podklad.py" "%%F" "mhbim\%%~nF_heiz.dxf" --profil heiz --posun %1
)
