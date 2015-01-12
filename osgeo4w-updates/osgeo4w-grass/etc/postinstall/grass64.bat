set ICON=%OSGEO4W_ROOT%\apps\grass\grass-6.4.4\etc\gui\icons\grass_osgeo.ico
set ICON_CMD=%OSGEO4W_ROOT%\apps\grass\grass-6.4.4\etc\gui\icons\grass_cmd.ico
set ICON_TCLTK=%OSGEO4W_ROOT%\apps\grass\grass-6.4.4\etc\gui\icons\grass_tcltk.ico
set BATCH=%OSGEO4W_ROOT%\bin\grass64.bat
textreplace -std -t "%OSGEO4W_ROOT%"\bin\grass64.bat
textreplace -std -t "%OSGEO4W_ROOT%"\bin\grass64
textreplace -std -t "%OSGEO4W_ROOT%"\apps\grass\grass-6.4.4\etc\fontcap

mkdir "%OSGEO4W_STARTMENU%\GRASS GIS 6.4.4" 
xxmklink "%OSGEO4W_STARTMENU%\GRASS GIS 6.4.4\GRASS 6.4.4 GUI.lnk" "%BATCH%" "-wx" \ "Launch GRASS GIS 6.4.4 with wxGUI" 1 "%ICON%" 
xxmklink "%OSGEO4W_STARTMENU%\GRASS GIS 6.4.4\GRASS 6.4.4 Old TclTk GUI.lnk" "%BATCH%" "-tcltk" \ "Launch GRASS GIS 6.4.4 with the old TclTk GUI" 1 "%ICON_TCLTK%" 
xxmklink "%OSGEO4W_STARTMENU%\GRASS GIS 6.4.4\GRASS 6.4.4 Command Line.lnk" "%BATCH%" "-text" \ "Launch GRASS GIS 6.4.4 in text mode" 1 "%ICON_CMD%" 

rem xxmklink "%ALLUSERSPROFILE%\Desktop\GRASS GIS 6.4.4.lnk" "%BATCH%" "-wx" \ "Launch GRASS GIS 6.4.4 with wxGUI" 1 "%ICON%" 

del "%OSGEO4W_ROOT%"\bin\grass64.bat.tmpl
del "%OSGEO4W_ROOT%"\bin\grass64.tmpl
