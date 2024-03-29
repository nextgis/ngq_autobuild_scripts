@echo off
cmake -G "Visual Studio 9 2008" ^
-D CMAKE_INSTALL_PREFIX=%1 ^
-D TIFF_LIBRARY=%OSGEO4W_ROOT%\lib\libtiff_i.lib ^
-D TIFF_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D JPEG_LIBRARY=%OSGEO4W_ROOT%\lib\jpeg_i.lib ^
-D JPEG_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D PNG_LIBRARY=%OSGEO4W_ROOT%\lib\libpng13.lib ^
-D PNG_PNG_INCLUDE_DIR=%OSGEO4W_ROOT%\include ^
-D PROJ_LIBRARY=%OSGEO4W_ROOT%\lib\proj_i.lib ^
-D GEOS_LIBRARY=%OSGEO4W_ROOT%\lib\geos_c.lib ^
-D ICONV_LIBRARIES=E:\builds\env\libiconv-1.14\lib\libiconv.lib ^
-D ICONV_INCLUDE_DIR=E:\builds\env\libiconv-1.14\include ^
-D GDAL_ENABLE_FRMT_WMS=TRUE ^
-D GDAL_BUILD_NETWORK_SUPPORT=TRUE ^
-D SWIG_DIR=E:\GDAL\swigwin\swigwin-3.0.2 ^
-D SWIG_EXECUTABLE=E:\GDAL\swigwin\swigwin-3.0.2\swig.exe ^
-D OGR_ENABLE_SQLITE=TRUE ^
-D SQLITE3_LIBRARY=%OSGEO4W_ROOT%\lib\sqlite3_i.lib ^
-D SPATIALITE_LIBRARY=%OSGEO4W_ROOT%\lib\spatialite_i.lib ^
-D GDAL_ENABLE_FRMT_PDF=FALSE ^
%2

