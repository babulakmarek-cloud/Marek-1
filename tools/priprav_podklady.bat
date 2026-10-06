@echo off
rem Pripravi ciste podklady pro MH BIM ze vsech DXF v aktualni slozce.
rem Pouziti: priprav_podklady.bat X Y [XMIN,YMIN,XMAX,YMAX]
rem   X Y = spolecny vztazny bod v mm (Werk 2: osa 39 x osa E = 24331 68325), oddelene MEZEROU
rem   oblast (nepovinne) v uvozovkach, napr. "15000,60000,178000,95000" = orez bez situace
rem Vystup: slozka mhbim\ s *_heiz.dxf a *_arch.dxf.  Potreba: Python + pip install ezdxf
if "%~2"=="" ( echo Pouziti: priprav_podklady.bat X Y ["XMIN,YMIN,XMAX,YMAX"]   napr. priprav_podklady.bat 24331 68325 & exit /b 1 )
set "OBLAST="
if not "%~3"=="" set "OBLAST=--oblast %~3"
if not exist mhbim mkdir mhbim
for %%F in (*.dxf) do (
  echo === %%F
  python "%~dp0mhbim_podklad.py" "%%F" "mhbim\%%~nF_arch.dxf" --profil arch --posun %~1,%~2 --bez-srafy %OBLAST%
  python "%~dp0mhbim_podklad.py" "%%F" "mhbim\%%~nF_heiz.dxf" --profil heiz --posun %~1,%~2 %OBLAST%
)
