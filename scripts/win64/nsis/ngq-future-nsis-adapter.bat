rem @echo off
rem %1 - qgis install dir
rem %2 - nsis script
rem %3 - nextgis qgis version
rem %4 - nextgis qgis installer name
cd /D %NGQBUILDER_BUILDS_DIR%
makensis.exe ^
/DOSGEO4W_SRC_DIR="E:\builds\env\osgeo4w-4install\*.* E:\builds\env\gdal-ags\*.* E:\builds\env\osgeo4w-iconv-1.9-dll\*.* E:\builds\env\libiconv-1.14\*.* E:\builds\env\osgeo4w-gdal-dll\*.*"  ^
/DQGIS_SRC_DIR=%1 ^
/DGRASS_SRC_DIR="E:\builds\env\osgeo4w-grass" ^
/DSAGA_SRC_DIR="E:\builds\env\osgeo4w-saga" ^
/DINSTALLER_NAME=%NGQBUILDER_BUILDS_DIR%\%4 ^
/DPROGRAM_VERSION=%3 ^
/DPLUGINS="e:\builds\qgis-plugins\identifyplus" ^
/DQGIS_MANUAL_FILE_NAME_RU="QGIS-2.6-UserGuide-ru.pdf" ^
/DQGIS_MANUAL_FILE_NAME_EN="QGIS-2.6-UserGuide-en.pdf" ^
%2