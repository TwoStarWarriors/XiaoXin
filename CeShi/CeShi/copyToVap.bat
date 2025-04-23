@REM 找到要拷贝的目标文件夹
@echo off
Setlocal ENABLEDELAYEDEXPANSION
set str1=%cd:~3%
set ch1=\

set str=%str1%
:loop00
if not "%str%"=="" (
set /a num+=1
if "!str:~0,1!"=="%ch1%" set /a pos=%num%+1

set "str=%str:~1%"
goto loop00
)

set str=%str1%

:loop01
if not %pos%==0 (
set /a pos-=1

set "str=%str:~1%"
goto loop01
)
@echo on

@REM 新能源目录  /sdcard/ZyDiagSys/CarInf/Ner/%str%
@REM 中国目录  /sdcard/ZyDiagSys/CarInf/Chn/%str%
@REM 美洲目录  /sdcard/ZyDiagSys/CarInf/America/%str%
@REM 亚洲目录  /sdcard/ZyDiagSys/CarInf/Asia/%str%
@REM 欧洲目录  /sdcard/ZyDiagSys/CarInf/Euro/%str%
@REM 特殊目录  /sdcard/ZyDiagSys/CarInf/Oth/%str%
@REM 将目标文件拷贝到新能源目录
adb push .\%str% /sdcard/ZyDiagSys/CarInf/Oth
pause