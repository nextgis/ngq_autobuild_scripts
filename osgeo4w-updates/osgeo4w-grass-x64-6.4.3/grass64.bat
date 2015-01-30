set ICON=%OSGEO4W_ROOT%\apps\grass\grass-6.4.3\etc\gui\icons\grass_osgeo.ico
set ICON_CMD=%OSGEO4W_ROOT%\apps\grass\grass-6.4.3\etc\gui\icons\grass_cmd.ico
set BATCH=%OSGEO4W_ROOT%\bin\grass64.bat
textreplace -std -t "%OSGEO4W_ROOT%"\bin\grass64.bat
textreplace -std -t "%OSGEO4W_ROOT%"\bin\grass64
textreplace -std -t "%OSGEO4W_ROOT%"\apps\grass\grass-6.4.3\etc\fontcap
del "%OSGEO4W_ROOT%"\bin\grass64.bat.tmpl
del "%OSGEO4W_ROOT%"\bin\grass64.tmpl

if not %OSGEO4W_MENU_LINKS%==0 mkdir "%OSGEO4W_STARTMENU%"
if not %OSGEO4W_MENU_LINKS%==0 nircmd shortcut "%OSGEO4W_ROOT%\bin\nircmd.exe" "%OSGEO4W_STARTMENU%\GRASS GIS 6.4.3" "GRASS GIS 6.4.3 GUI" "exec hide """%BATCH%" -wx" "%ICON%"
if not %OSGEO4W_MENU_LINKS%==0 nircmd shortcut "%BATCH%" "%OSGEO4W_STARTMENU%\GRASS GIS 6.4.3" "GRASS GIS 6.4.3 Command Line" "-text" "%ICON%"
rem if not %OSGEO4W_DESKTOP_LINKS%==0 nircmd shortcut "%OSGEO4W_ROOT%\bin\nircmd.exe" "~$folder.desktop$" "GRASS GIS 6.4.3" "exec hide """%BATCH%" -wx" "%ICON%"
