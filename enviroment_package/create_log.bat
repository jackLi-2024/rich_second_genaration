@echo off
echo ****************************************
echo 自动创建C盘文件夹（Anaconda目录）
echo ****************************************

set Pan=C:\Anaconda

echo 开始执行------------
echo ...
echo ...
echo ...

if exist %Pan% (
	echo 文件夹已经存在，无需再进行创建!
)else (
	md %Pan%
	echo 文件夹创建成功!
)
pause

