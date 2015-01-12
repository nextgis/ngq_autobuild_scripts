@echo off
rem %1 - building dir
rem %2 - canfiguration env bat
rem %3 - canfiguration qgis bat
rem %4 - qgis src dir
rem %5 - qgis install dir

cd /D %1
call %2
call %3 %5 %4