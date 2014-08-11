@echo off
set PYTHONHOME=d:\Programs\Python\2.7.3

rem    REG ADD HKCR\Python.File\shell\open\command /ve /t REG_SZ /d ""D:\Programs\Devel\Python27\python.exe" "%1" %*"
rem    ftype Python.File="D:\Programs\Devel\Python27\python.exe" "%1" %*
set PY_HOME=%PYTHONHOME%

rem set PYTHONPATH=%PYTHONHOME%;%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs;%PYTHONHOME%\Lib\lib-tk
rem set PYTHONPATH=%PYTHONPATH%;%PYTHONHOME%\Scripts

set PYTHONPATH=%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs
set PATH=%PYTHONPATH%;%PYTHONHOME%;%PYTHONHOME%\Scripts;%PYTHONHOME%\PyMOL;%PATH%

rem cd D:\Programs\Devel\Python27_tests\uncompyle2\
cmd.exe

