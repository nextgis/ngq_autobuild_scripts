@echo off
cmake -G "Visual Studio 10 Win64" ^
-D CMAKE_INSTALL_PREFIX=%1 ^
-D TIFF_LIBRARY=%OSGEO4W_ROOT%\lib\libtiff_i.lib ^
-D TIFF_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D JPEG_LIBRARY=%OSGEO4W_ROOT%\lib\jpeg_i.lib ^
-D JPEG_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D PNG_LIBRARY=%OSGEO4W_ROOT%\lib\libpng16.lib ^
-D PNG_PNG_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D GDAL_ENABLE_FRMT_WMS=TRUE ^
%2

