@echo off
rem %1 - building dir
rem %2 - canfiguration env bat
rem %3 - sln

cd /D %1
call %2
msbuild /p:Configuration=Release %3
if exist INSTALL.vcproj (
    msbuild /p:Configuration=Release INSTALL.vcproj
) else (
    msbuild /p:Configuration=Release INSTALL.vcxproj
)