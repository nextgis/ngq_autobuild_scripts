@echo off
rem %1 - building dir
rem %2 - canfiguration env bat
rem %3 - qgis src dir
cd /D %1
call %2
msbuild /p:Configuration=Release %3
msbuild /p:Configuration=Release INSTALL.vcproj