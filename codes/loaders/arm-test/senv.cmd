@echo off
@echo Set environment for Computer name: %computername%

if %COMPUTERNAME% == ACER-C0077A3C37 goto asus-notebook
if %COMPUTERNAME% == PC-006 goto work-comp
if %COMPUTERNAME% == MA3X goto ma3x-pc

:unknown
echo Computer name: %computername% is unknown. Environment not set
goto run-cmd

:ma3x-pc
echo Environment for %computername% is set successful (MA3X)
set PATH=G:\Programs\prog\yagarto\bin;G:\Programs\prog\yagarto-tools-20100703\bin;%PATH%
goto run-cmd

:work-comp
echo Environment for %computername% is set successful (PC-006)
set PATH=D:\Programs\Devel\yagarto\bin;D:\Programs\Devel\yagarto-tools-20100703\bin;%PATH%
goto run-cmd

:asus-notebook
echo Environment for %computername% is set successful (ACER-C0077A3C37)
set PATH=D:\Programs\Devel\yagarto-4.7.1\bin;D:\Programs\Devel\yagarto-tools-20100703\bin;%PATH%

:run-cmd
echo _
rem sh
cmd.exe
