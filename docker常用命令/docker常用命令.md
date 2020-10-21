<!-- TOC -->

- [1.停止镜像](#1停止镜像)
    - [1.通过  docker ps -a 查看所有的运行的进程](#1通过-docker-ps--a-查看所有的运行的进程)
    - [2. 通过运行 docker stop id  停止运行](#2-通过运行-docker-stop-id-停止运行)
    - [3.进程停止后就可以t通过 docker rm id  删除 承载改进程的容器了](#3进程停止后就可以t通过-docker-rm-id-删除-承载改进程的容器了)
    - [4.最后通过运行 docker rmi id  删除镜像](#4最后通过运行-docker-rmi-id-删除镜像)
- [2.拉取镜像](#2拉取镜像)
    - [1.不指定版本（默认获取最新版本）](#1不指定版本默认获取最新版本)
    - [2.指定版本](#2指定版本)
- [3.查看镜像](#3查看镜像)
- [4.运行容器](#4运行容器)
- [5.启动镜像](#5启动镜像)
- [6.查看当前正在运行镜像](#6查看当前正在运行镜像)
- [7.查看所有镜像](#7查看所有镜像)
- [8.停止镜像服务](#8停止镜像服务)
- [9.查看日志](#9查看日志)
- [10.进入当前正在运行的容器](#10进入当前正在运行的容器)
- [11.从容器内拷贝文件到主机上](#11从容器内拷贝文件到主机上)
- [12.查看docker状态](#12查看docker状态)
- [13.提交容器成为一个新的副本](#13提交容器成为一个新的副本)
- [14.查看容器详细信息](#14查看容器详细信息)
- [15.数据卷的挂载](#15数据卷的挂载)

<!-- /TOC -->
# 1.停止镜像
### 1.通过  docker ps -a 查看所有的运行的进程
``` shell
docker ps -a
```
### 2. 通过运行 docker stop id  停止运行
```
docker stop 进程id
```
### 3.进程停止后就可以t通过 docker rm id  删除 承载改进程的容器了
```
docker rm 进程id
```
### 4.最后通过运行 docker rmi id  删除镜像
```
docker rmi 进程id/进程名
```
# 2.拉取镜像
### 1.不指定版本（默认获取最新版本）
``` 
docker pull 镜像名称
```
### 2.指定版本
```
docker pull 镜像名称：版本号
```
# 3.查看镜像
``` 
docker images
```
# 4.运行容器
```
docker run [可选参数] 镜像名
```
其中可选参数有：
> --name="容器名字"  用来区分容器 
> -d 后台方式运行
> -it 使用交互方式运行，进入容器查看内容
> -p 指定容器端口 -p 8080:2000 主机端口映射容器端口
比如：
> docker run -it centos /bin/bash
> sudo docker run -d --name nginx01  -p 3344:80 nginx
# 5.启动镜像
```
docker start 镜像名
```
# 6.查看当前正在运行镜像
``` 
docker ps
```
# 7.查看所有镜像
```
docker ps -a
```
# 8.停止镜像服务
```
docker stop 
```
# 9.查看日志
```
docker logs -f -t --tail 条数 容器名称
```
# 10.进入当前正在运行的容器
```
docker exec  -it 容器id 比如docker exec -it 0d65014fa49d /bin/bash
```
# 11.从容器内拷贝文件到主机上
```
docker cp 容器id:容器内路径  目的主机路径
```
比如：
>  sudo docker cp a121e690a3b1:/1.java /home
将a121e690a3b1容器内的根目录下的1.java文件拷贝到宿主机的home目录下
# 12.查看docker状态
```
docker stats
或
docker stats 镜像id 比如：docker stats 77c7c394723b
```
# 13.提交容器成为一个新的副本
```
docker commit -m="提交的描述信息" -a='作者' 容器id 目标镜像名：[Tag]
```
# 14.查看容器详细信息
```
docker inspect 容器id
```
# 15.数据卷的挂载
```
sudo docker run -it -v /home/docker/centos_mout:/home centos /bin/bash
```
下面解释一下命令的意思：
> 该命令是将centos镜像下的/home目录同步至我们主机上的/home/docker/centos_mout上面，即我们在centos镜像下做任何操作均会同步至我们本地主机上的/home/docker/centos_mout目录上面 ，且这种行为是 双向的，也就是说我们在自己主机上的/home/docker/centos_mout目录下面做任何 操作也会同步至centos镜像下的/home文件下