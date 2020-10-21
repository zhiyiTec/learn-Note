# 1.拉取nginx镜像
```
docker pull nginx
```
# 2.验证是否镜像拉取成功
```
docker images
```
![](1.png)
# 3.运行nginx镜像
```
sudo docker run -d --name nginx01  -p 3344:80 nginx
```
大致解释一下上面这个命令
> * -d 表示是以后台的方式运行
> * --name nginx01 说明此镜像的名称命名为nginx01，如果不加此参数默认为镜像的名称
> -p 3344:80 80是nginx镜像运行起来的端口号，3344是映射到公网可以供我们访问的端口

# 4.查看是否启动成功
```
docker ps
```
![](2.png)
# 5.在外部浏览器验证nginx的启动
![](3.png)