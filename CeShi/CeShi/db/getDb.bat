
copy menuData.txt MENU.DB
copy sysData.txt DIAG.DB
copy dtcData.txt DTC.DB
copy tipsData.txt TIPS.DB

@rem gb to utf8
D:\VpadExe\gbToUtf8 MENU.DB
D:\VpadExe\gbToUtf8 DIAG.DB
D:\VpadExe\gbToUtf8 DTC.DB
D:\VpadExe\gbToUtf8 TIPS.DB


@rem 整理菜单
D:\VpadExe\NODEADDR MENU.DB

@rem 整理转意标识
D:\VpadExe\NODEADDR TIPS.DB

@rem 整理被调系统库
D:\VpadExe\NODEADDR DIAG.DB

@rem 整理故障码库
D:\VpadExe\DTC DTC.DB

@rem 获取@地址列表追加在末尾
D:\VpadExe\StartA DTC.DB


@rem 加密
D:\VpadExe\EnZY MENU.DB zl 1
D:\VpadExe\EnZY TIPS.DB zl 1
D:\VpadExe\EnZY DIAG.DB zl 1
D:\VpadExe\EnZY DTC.DB zl 1

@rem 创建目录，目录民为上上的文件夹名,不会覆盖原来的目录

@echo off 
Setlocal ENABLEDELAYEDEXPANSION
set str1=%cd:~3,-3%
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
md ..\%str%

@echo on

copy MENU.DB ..\%str%\
copy TIPS.DB ..\%str%\
copy DIAG.DB ..\%str%\
copy DTC.DB  ..\%str%\


@rem 删除无用数据
del *.db
del *.bbb
del *.bak

pause