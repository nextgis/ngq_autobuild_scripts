@echo off
rem %1 - building dir
rem %2 - canfiguration env bat
rem %3 - qgis src dir
rem %4 - qgis install dir

cd /D %1
call %2

echo "======== Configurate qgis  Start==========="

cmake -G "Visual Studio 10 Win64" ^
-D PEDANTIC=TRUE ^
-D WITH_QSPATIALITE=TRUE ^
-D WITH_MAPSERVER=TRUE ^
-D MAPSERVER_SKIP_ECW=TRUE ^
-D WITH_GLOBE=TRUE ^
-D WITH_TOUCH=TRUE ^
-D WITH_ORACLE=TRUE ^
-D CMAKE_BUILD_TYPE=Release ^
-D CMAKE_INSTALL_PREFIX=%4 ^
-D BISON_EXECUTABLE=bison.exe ^
-D FLEX_EXECUTABLE=flex.exe ^
-D SPATIALINDEX_LIBRARY=%OSGEO4W_ROOT%\lib\spatialindex-64.lib ^
-D SPATIALITE_LIBRARY=%OSGEO4W_ROOT%\lib\spatialite_i.lib ^
%3

echo "======== Configurate qgis  Finish==========="
