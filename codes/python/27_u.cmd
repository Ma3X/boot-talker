@echo off
set PYTHONHOME=g:\Programs\prog\python\2.7.3

rem REG ADD HKCR\Python.File\shell\open\command /ve /t REG_SZ /d ""D:\Programs\Devel\Python27\python.exe" "%1" %*"
rem ftype Python.File="D:\Programs\Devel\Python27\python.exe" "%1" %*
set PY_HOME=%PYTHONHOME%

set PYTHONPATH=%PYTHONHOME%;%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs;%PYTHONHOME%\Lib\lib-tk
set PYTHONPATH=%PYTHONPATH%;%PYTHONHOME%\Scripts
set PATH=%PYTHONPATH%;%PATH%
rem cd D:\Programs\Devel\Python27_tests\uncompyle2\
cmd
