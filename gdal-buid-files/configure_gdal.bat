@echo off
cmake -G "Visual Studio 9 2008" ^
-D CMAKE_INSTALL_PREFIX=%1 ^
-D TIFF_LIBRARY=%OSGEO4W_ROOT%\lib\libtiff_i.lib ^
-D TIFF_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D JPEG_LIBRARY=%OSGEO4W_ROOT%\lib\jpeg_i.lib ^
-D JPEG_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D PNG_LIBRARY=%OSGEO4W_ROOT%\lib\libpng13.lib ^
-D PNG_PNG_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D ICONV_LIBRARIES=E:\builds\libiconv-1.14\lib\libiconv.lib ^
-D ICONV_INCLUDE_DIR=E:\builds\libiconv-1.14\include ^
-D GDAL_ENABLE_FRMT_WMS=TRUE ^
%2

