@echo off
echo "======== Configurate env  Start==========="
set OSGEO4W_ROOT=E:\builds\env\osgeo4w
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
set OSGEO4W_ROOT=%OSGEO4W_ROOT:\=/%

set VS90COMNTOOLS=%PROGRAMFILES(x86)%\Microsoft Visual Studio 9.0\Common7\Tools\
call "%PROGRAMFILES(x86)%\Microsoft Visual Studio 9.0\VC\vcvarsall.bat" x86

set INCLUDE=%INCLUDE%;"%PROGRAMFILES%\Microsoft SDKs\Windows\v7.0\include"
set LIB=%LIB%;"%PROGRAMFILES%\Microsoft SDKs\Windows\v7.0\lib"

path %PATH%;%PROGRAMFILES(x86)%\CMake\bin;c:\cygwin64\bin;%PROGRAMFILES(x86)%/Git/bin;

@set GRASS_PREFIX=%OSGEO4W_ROOT%/apps/grass/grass-6.4.4
@set INCLUDE=%INCLUDE%;%OSGEO4W_ROOT%\include
@set LIB=%LIB%;%OSGEO4W_ROOT%\lib;%OSGEO4W_ROOT%\lib;%OSGEO4W_ROOT%/apps/Python27/libs

@set INCLUDE=%INCLUDE%;E:\builds\env\osgeo4w-gdal\include
@set LIB=%LIB%;E:\builds\env\osgeo4w-gdal\lib
path %PATH%;E:\builds\env\osgeo4w-gdal\bin;E:\builds\env\osgeo4w-iconv-1.9\bin

echo "======== Configurate env  Finish==========="

 