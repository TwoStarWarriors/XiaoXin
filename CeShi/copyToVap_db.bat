@REM �ҵ�Ҫ������Ŀ���ļ���
cd db
call getDb.bat
cd ..
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

@REM ����ԴĿ¼  /sdcard/ZyDiagSys/CarInf/Ner/%str%
@REM �й�Ŀ¼  /sdcard/ZyDiagSys/CarInf/Chn/%str%
@REM ����Ŀ¼  /sdcard/ZyDiagSys/CarInf/America/%str%
@REM ����Ŀ¼  /sdcard/ZyDiagSys/CarInf/Asia/%str%
@REM ŷ��Ŀ¼  /sdcard/ZyDiagSys/CarInf/Euro/%str%
@REM ����Ŀ¼  /sdcard/ZyDiagSys/CarInf/Oth/%str%
@REM ��Ŀ���ļ�����������ԴĿ¼
adb push .\%str% /sdcard/ZyDiagSys/CarInf/Oth/%str%
pause