mkdir "%OSGEO4W_STARTMENU%"
xxmklink "%OSGEO4W_STARTMENU%\MSYS Shell.lnk"       "%OSGEO4W_ROOT%\apps\msys\msys.bat" " " \ "Minimal SYStem" 7 "%OSGEO4W_ROOT%\apps\msys\msys.ico"

rem xxmklink "%ALLUSERSPROFILE%\Desktop\MSYS Shell.lnk" "%OSGEO4W_ROOT%\apps\msys\msys.bat" " " \ "Minimal SYStem" 7 "%OSGEO4W_ROOT%\apps\msys\msys.ico"

textreplace -std -t apps/msys/etc/fstab
