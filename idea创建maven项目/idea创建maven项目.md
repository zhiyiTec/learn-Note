# 默认配置好了maven，如果没有配置好，请参考我的这一篇博客 [点击查看]()
# 1.file->new->project->maven,如图：
![](1.png)
# 2.输入groupId,Artifacid，点击next,如图：
![](2.png)
![](3.png)
点击finish
# 3.file->Project Structure,如图
![](4.png)
project无需设置，看下一步,点图中的“+”:
![](5.png)
选择web
![](6.png)
接下来双击双击Web Resource Directory
![](7.png)
![](8.png)
![](9.png)
> 在后面加上webapp。好了，点OK，Web的资源目录便设置好了。
![](10.png)
# 4.现在设置Web的描述文件的目录
![](11.png)
设置成如下的格式：设置在webapp目录下
![](12.png)
Facts: 表示当前项目的适配服务组件。可看到此项目已是一个Web项目了。
![](13.png)
# 5. 进行Aftifacts设置，这个Aftifacts描述了当前项目发布的信息。现在进行添加，从Modeles中选择。
![](14.png)
![](15.png)
# 6.行成如下的目录结构
![](18.png)
# 7.如有需要，添加lib包
![](19.png)
# 8.部署服务器
### run->Edit Configurations
![](20.png)
![](21.png)
![](22.png)
# 9.添加tomcat环境
### file->Project Structure
![](23.png)
![](24.png)
![](25.png)