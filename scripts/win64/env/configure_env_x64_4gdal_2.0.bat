@echo off
echo "======== Configurate env  Start==========="
set OSGEO4W_ROOT=E:\builds\env-x64\osgeo4w
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
set OSGEO4W_ROOT=%OSGEO4W_ROOT:\=/%

rem call "%PROGRAMFILES(x86)%\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86
path %PATH%;C:\Windows\Microsoft.NET\Framework64\v4.0.30319

set INCLUDE=%INCLUDE%;C:\Program Files\Microsoft SDKs\Windows\v7.1\include
set LIB=%LIB%;C:\Program Files\Microsoft SDKs\Windows\v7.1\lib\x64

path %PATH%;%PROGRAMFILES(x86)%\CMake\bin;c:\cygwin64\bin;%PROGRAMFILES(x86)%/Git/bin

@set GRASS_PREFIX=%OSGEO4W_ROOT%/apps/grass/grass-6.4.3
@set INCLUDE=%INCLUDE%;%OSGEO4W_ROOT%\include
@set LIB=%LIB%;%OSGEO4W_ROOT%\lib;%OSGEO4W_ROOT%\apps\Python27\libs

echo "======== Configurate env  Finish==========="

 