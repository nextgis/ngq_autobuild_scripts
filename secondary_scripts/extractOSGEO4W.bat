@echo off
rem cd /D %2
for /r %1 %%g in (*.tar.bz2) do (
   tar xjvf %%g --force-local
   )
