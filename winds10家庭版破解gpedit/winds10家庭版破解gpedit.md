# 1.首先我们打开记事本，并输入以下内容（注意空格）：
``` cmd
@echo off

pushd "%~dp0"

dir /b C:\Windows\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientExtensions-Package~3*.mum >List.txt

dir /b C:\Windows\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientTools-Package~3*.mum >>List.txt

for /f %%i in ('findstr /i . List.txt 2^>nul') do dism /online /norestart /add-package:"C:\Windows\servicing\Packages\%%i"

pause
```
名称随意，扩展名为“.cmd”把它保存下来
> 2.接下来右键以管理员身份运行这个文件,待运行结束后，再打开小娜输入“gpedit.msc”查看一下，你熟悉的组策略是不是又有了。