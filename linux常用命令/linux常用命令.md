<!-- TOC -->

- [1.卸载软件](#1卸载软件)
- [2.解压文件](#2解压文件)
- [3.编辑文件](#3编辑文件)
- [4.安装软件-通过deb软件包格式安装](#4安装软件-通过deb软件包格式安装)
- [5.查看本机ip](#5查看本机ip)
- [6.创建文件](#6创建文件)
- [7.复制文件](#7复制文件)

<!-- /TOC -->
# 1.卸载软件
```
sudo apt-get --purge remove package_name
```
# 2.解压文件
``` 
sudo tar zxvf 压缩包名
```
# 3.编辑文件
``` 
sudo gedit 文件名
```
# 4.安装软件-通过deb软件包格式安装
```
sudo apt-get -f --fix-missing install
sudo dpkg -i 包名
```
# 5.查看本机ip
```
sudo ifconfig -a
```
# 6.创建文件
```
touch 文件名 比如：touch 1.txt
```
# 7.复制文件
```
cp -r /目录/* /目录2
```
> 比如：cp -r /home/soft/* /home/soft01表示复制soft目录下的所有文件到soft01目录下
