# 上传项目到gitHub
### 1.首先确保已经安装git,如果未安装，请自行百度安装   
### 2.在gitHub上面创建一个New respository
### 3.进行如下配置![](img/1.png)
### 4.打开git-bash.exe
### 5.cd到你的项目目录
### 6.执行命令：
```
git init
```
> 该命令是在你的项目目录下初始化一个repository，执行成功后，会在你的目录下生成一个.git的隐藏文件。
### 7.执行命令：
```
git add .
```
> 注意该命令后面有一个“.”,小点。表示把该目录下的所有文件加入到本地暂存区中。执行成功后不会有任何提示：
### 8.执行命令：
```
git status
```
> 该命令会把你本地工作区和暂存区的版本进行比较，查看当前的状态。我下面的状态是已经把所有文件加入到了暂存区中，但是还没有提交到本地历史区。
### 9.执行命令：
```
git commit -m "这里是注释。。。"
```
> 该命令会把本地暂存区中的文件提交到本地历史区，注意只有在本地历史区中的内容才能提交到github。执行该命令后，我们所有的文件都只是在本地。没有github任何关系。
### 10.执行命令：
```
git remote add origin https://github.com/chenyufeng1991/NewsClient.git
```
> 注意：后面的地址是你在gitHub上面创建好了repository给出的地址        
>该命令是把本地历史区中的文件添加到github服务器的暂存区中。这一步是本地和远程服务器建立联系的一步。执行成功后不会显示任何结果：
### 11.执行命令：
> 注意：此命令分两种情况：
> *  1.往git上面上传代码：
> ```
> git push -u origin master
>```
> 到此往git上面上传代码就结束了，注意第十二步不用执行
> #   2.往gitHub上面上传代码，就是执行下面的命令
```
git pull origin master --allow-unrelated-histories
```
> 上述执行成功后，发现在项目目录下多了一个“README.md”文件，这个文件就是从github上拉下来的。因为我们在github上创建repository的时候就创建了这个“README.md”文件，该文件是对这个repository的说明。
### 12.执行命令：
```
git push -u origin master --force 
```
### 13.来到github下查看，上传代码已经成功了。
## 接下来讲一下如何更新项目
### 1.打开git-bash.exe
### 2.cd到你的项目目录
### 3.查看当前的git仓库状态，可以使用git status
```
git status
```
> 可以看到On branch master,这个说明已经在master分之上了
### 4.更新后使用git add * --代表更新全部
```
git add *
```
### 5.接着输入git commit -m "更新说明"，commit只是提交到缓存区域
```
git commit -m "更新说明”
```
### 6.如果多人同时开发维护代码，得先git pull,拉取当前分支最新代码
```
git pull
```
### 7.最后git push origin master,最后一步才是push到远程master分支上
```
git push -u origin master --force 
```
# 接下来讲解如何创建分支，合并分支，删除分支
## 1.查看分支
### 1.查看本地分支
> git branch
### 2.查看远程分支
> git branch -r
### 3.查看所有分支
> git branch -a
## 2.创建分支
### 1.本地创建新的分支
> git branch branchName
### 2.切换到新的分支
> git checkout [branch name]
### 3.创建+切换分支
> git checkout -b [branch name]
### 4.将新分支推送到github
> git push origin [branch name]
例如:
```
git push origin gh-dev
```
## 3.删除分支
### 1.删除本地分支
> git branch -d [branch name]
### 2.删除github远程分支
> git push origin :[branch name]
# 再接着学习从远程代码库克隆代码到本地的方式：
> * 1.cd到你要存放工程的目录
> * 2.git init
> * 3.git clone ssh://zhuxu@192.168.10.224:29418/lxyz/lxyz-rcs.git
# 从远程代码库更新本地代码
> * 1.git status（查看本地分支文件信息，确保更新时不产生冲突）
>  * 2.git checkout（查看文件是否有修改）
> * 3. git pull