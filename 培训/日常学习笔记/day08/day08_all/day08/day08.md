###12 走进大数据

####12.1 数据
数据(data)是事实或观察的结果，是对客观事物的逻辑归纳，是用于表示客观事物的未经加工的的原始素材。

数据是进行决策的重要依据。

信息技术和各类终端的普及。

#### 12.2 大数据

大数据的本质也是数据。

**大数据指的是数据量规模大到使用常规的工具，无法在合理的时间内，实现数据的抓取，存储，分析和管理的数据量**。

常规的工具：mysql，Excel，普通的服务器和程序...

合理的时间内：因具体场景而不同

#### 12.3 大数据3V

大数据相对于数据的3个核心特点：

volumes(大量)：大数据的数据量非常大，一般从TB级到PB不等，当前一些企业对大数据的数据量的起点约定是100TB

velocity(高速)：数据量的增长会带来处理时间上的消耗，对大数据的处理时间是有要求的，需要大大快于传统数据

variety(多样)：

- 结构化数据：像excel表一样的数据
- 半结构化数据：像json一样的数据
- **非结构化数据**：视频、音频、图像等等

IBM又提出一个V(真实、有效)

#### 12.4 大数据带来的挑战

主要的挑战来自于硬件，硬盘的读取速度没有随着数据量同比增长。

解决大数据挑战的核心思想是**分布式**。

真正使用分布式来解决问题时，会需要很多具体的挑战，例如数据的合理拆分、数据的备份、任务的并发执行、数据一致性的问题。

在当前的行业中，存在非常成熟的分布式解决方案，可以帮助使用者实现数据的分布式存储和数据的分布式计算。

这个解决方案就是以**hadoop**为核心的大数据平台。

开发者学习的是如何搭建和使用**hadoop**平台，来解决具体的大数据方法的挑战。

###13 Hadoop

####13.1 基本概念

当前最流行的开源大数据处理平台，由Apache基金会维护。

hadoop2.x版本由3个核心组件构成：HDFS，MapReduce，YARN

- HDFS：Hadoop的分布式文件系统，实现大数据的分布式存储，思想来自于google的GFS，相当于GFS的Java开源实现版本

- MapReduce：一个分布式计算引擎，由计算模型和计算库构成，可以实现海量数据的分布式计算(离线)，思想同样来自于google。

- YARN：Hadoop集群的资源调度平台，负责对集群的计算资源(cup和内存)进行管理，并对分布式计算任务进行管理。YARN大大提高了Hadoop的可扩展性，使得HDFS可以和各类的计算引擎(Tez, Spark)来配合。Hadoop2.x版本才有的

hadoop擅长做数据的离线分析

例如：猫眼票房，每天早上9点30分，公布截止到该时间的所有票房情况，今天后续的数据，不会自动添加到这个票房情况中

####13.2 基本概念

搭建hadoop平台的前提是安装Linux虚拟机。

学习中使用的是`centos7`版本，虚拟机软件使用`Virtual Box`

为节省时间，教学提供了一个.vdi文件，是已经最小化安装的`centos7`的硬盘文件，其中安装了`jdk1.8`和`mariadb5.5`，没有可视化界面，主机名为`master`，主机ip为`192.168.56.101`。学习中可以直接使用该.vid文件恢复一台虚拟机。

步骤：

- 安装VirtualBox

	将VirtualBox使用默认配置安装到本地电脑

- 创建一台虚拟机

	在d盘或e盘根目录下创建vfile文件夹，将smaster.vdi文件拷贝进去
	在VirtualBox中选择新建创建虚拟机，名字为master,位置选择d:/vfile或e:/vfile，类型是linux，版本是redhat(64)，内存设置2048MB，硬盘选择一个已有盘片，在右侧文件夹选项中选择注册vfile文件夹下的smaster.vdi

	启动该虚拟机，并登录用户，用户名和密码都是root

- 配置虚拟机网络

	将虚拟机网络类型使用 host-only

	将主机的网络共享给主机上的virtualBox网卡

	将virtualBox网卡的ip地址调整正确：从192.168.137.1改为192.168.56.1

- 安装shell工具，通过shell工具远程访问虚拟机

	安装xshell

	在xshell中新建连接，通过ssh协议远程访问虚拟机

- 安装hadoop

	hadoop有3种部署方式：

		1. 单机模式：使用一个进程模拟所有进程，一般不用
		2. 伪分布：使用一台主机，同时充当主节点和从节点
		3. 完全分布：使用多台主机，分别充当主节点和从节点(商业应用)

	hadoop安装步骤：
		
		1. 获取安装文件
		2. 解压缩
		3. 配置环境变量
		4. 配置hadoop的配置文件
		5. 格式化(只做一次)
		6. 启动hadoop

启动hdfs之后，可以使用`jps`命令查看当前主机运行的所有`java进程`，其中主节点应该运行`namenode`进程和`SecondaryNameNode`进程，从节点应该运行`datanode`进程。如果是伪分布模式，则当前主机应该同时包含以上3个进程。

启动yarn之后，使用`jps`查看，主节点应该运行`ResourceManager`，从节点应该运行`NodeManager`，如果是伪分布模式，则当前主机应该同时包含以上2个进程。

###14 HDFS

HDFS(Hadoop Distributed File System)，是Hadoop的分布式文件系统，可以实现海量数据的分布式存储

####14.1 Block的概念

HDFS对于上传的数据，默认按照128MB(2.x版本)的大小切分成多个Block，这些Block会被保存在集群不同的节点上。

BLock的大小可以根据具体业务的需求进行调整。Block越大，硬盘的寻址开销越小，但是可能造成的存储空间的浪费越多，因为一个Block中即使仅包含1MB的内容，占用的硬盘空间也是128MB。

因此，HDFS是面向大文件的，小文件使用HDFS存储效率较低。如果一定要保存小文件，可以先将多个小文件的内容汇总生成一个大文件，再上传HDFS。

####14.2 核心进程的作用

- NameNode
是HDFS的核心管理进程

	1. 运行在Master(主节点)上
	2. 负责接受用户对上传文件和下载文件的请求
	3. 负责计算上传文件的切分策略和存储策略
	4. 负责保存一个文件和切分的所有Block的对应关系
	5. 负责保存Block和Slave(从节点)的对应关系
	6. 负责监控整个集群所有Slave的硬盘资源情况和运行情况

NameNode所在的master如果宕机，Hadoop集群存在单点故障的风险。Hadoop1.x版本就存在这个问题。Hadoop2.x修复了这个问题，可以为NameNode设置一个热备。

Master因为运行NameNode，对内存的需求非常大，对硬盘的需求相对小。

- DataNode

	1. 运行在一个Slave的进程
	2. 负责接收用户对Block的上传和下载请求
	3. 对当前Slave的硬盘空间和Block存储情况进行管理
	4. 定时向NameNode汇报自己的情况

- SecondaryNameNode

	1. 负责定时对NameNode上保存的数据(文件与Block的对应关系及Block和节点的对应关系)进行备份(CheckPoint机制)
	2. 也可以作为NameNode的热备

HDFS在设计上充分考虑了整个提供的稳定性和问题的自我修复能力，对于HDFS来说，某一个节点宕机是常态而非意态。

####14.3 文件上传和文件下载的执行流程

####14.4 HDFS的基本命令

通用的语法是: hdfs dfs -命令 参数

具体命令和linux的命令非常相似

常用命令：

	-put	文件上传
	-ls		文件/文件夹查看
	-cat	文件内容查看
	-get	文件下载
	-mkdir	创建文件夹
	-rm		删除
	-cp		拷贝

**上传到HDFS的数据是不支持对文件的内容进行修改的，原因是在设计时牺牲了这部分功能，来保证海量数据的吞吐量**

####14.5 HDFS的JavaAPI(略)

####14.6 HDFS的配置和调优(略)

###15 分布式计算

核心思想：移动算法比移动数据更高效

将需要执行的计算逻辑，通过网络发送到保存了被计算数据的节点上，在该节点上对这部分数据进行计算，之后再将所有节点的计算结果进行汇总，以得到最终的结果。

优势：
1. 不需要通过网络传输大量的原始数据，而是将算法通过网络发送到有数据的节点，在该节点上直接运算
2. 所有节点的运算是并行执行的
3. 不存在一个节点无法保存所有汇总数据的问题

挑战：
1. 分布式计算的核心计算逻辑较为简单，但是将这些计算逻辑准确发送到有数据的节点上执行计算，并对结果进行汇总的逻辑比较难
2. 如果某一个节点上的计算任务失败，该如何重启该任务也是需要考虑的
3. 每个节点上的临时计算结果如何保存，最终的数据如何高效汇总的逻辑也比较难

因此，需要使用成熟的分布式计算引擎来实现。

####15.1 MapReduce

Hadoop内置的分布式计算引擎，用于对海量数据执行分布式计算(离线)

MapReduce由**计算模型**和**计算库**构成，开发者需要使用计算模型来向MapReduce平台提供要执行的分布式计算的**具体逻辑**，MapReduce平台会使用**计算库**来解决分布式计算的复杂性问题。

MapReduce的**计算模型**非常简单，有2个核心方法构成，一个是`map()`方法，另一个是`reduce()`。

`map()`方法用于封装在所有有数据的节点上执行的并行计算的逻辑。

`reduce()`方法用于封装对分布式计算结果进行汇总的逻辑。

###16 Hive

Hadoop生态系统中的数据仓库工具，允许用户使用SQL对HDFS上的数据进行操作，常见的操作如查询和分析。

原生的Hive是将用户的SQL语句翻译成MapReduce任务，在集群上执行。

Hive使用Facebook开发之后，共享给Apache，主要是让不懂Java编程的使用者可以基于SQL进行大数据分析。

Hive提供了一种类SQL的操作语言HiveQL

###16.1 安装Hive

- 获取安装文件
- 解压缩
- 配置环境变量
- 配置Hive的配置文件
- 启动Hive
启动Hive的前提是已经启动了Hadoop

###16.2 使用Hive

用户基于HiveQL对Hive进行操作，进而操作HDFS上的数据，HiveQL与SQL非常类似，因此操作Hive就像在操作关系型数据库。

- 建库

在hive中如果没有使用`use`命令选择库，所有的操作是默认基于`default`库的

- 建表

- 使用HiveQL操作表

从ftp上的车次数据文件夹下载20190601.zip文件并解压缩，可以得到一个`20190601.csv`文件

.csv格式的数据是标准的结构化数据，每行文本是一条数据，一条数据的多个字段使用逗号进行分割。文件的最上方一行一般是表头。

该文件最好不要使用excel等工具进行打开，因为这些软件会自动修改文件的内容以适合操作。

需求：将20190601.csv的数据导入到hive中，基于hiveQL进行分析

将文件从windows上传linux 

	cd /opt
	rz -y
	对话框中选中20190601.csv，选择上传

将文件从Linux上传hdfs

	hdfs dfs -put /opt/20190601.csv /
	查询
	hdfs dfs -ls /

在Hive中建库和建表

	-- 创建库
	create database nybikedb;
	
	-- 使用库
	use nybikedb;
	
	-- 创建表
	create table tb_trip_1(
	tripduration int,
	starttime string,
	stoptime string,
	start_station_id int,
	start_station_name string,
	start_station_latitude double,
	start_station_longitude double,
	end_station_id int,
	end_station_name string,
	end_station_latitude double,
	end_station_longitude double,
	bikeid int,
	usertype string,
	birth_year int,
	gender int
	)ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
	-- hive关联的原始数据字段的分隔符使用逗号 
	
	-- 导入hdfs上的数据
	load data inpath 'hdfs://master:8020/20190601-3.csv' 
	overwrite into table tb_trip_1;

	-- 检查导入的数据条数 (76419)
	select count(*) from tb_trip_1;

	-- 检查一条数据的字段是否正确 
	select * from tb_trip_1 limit 1;

	-- 统计数据中所有男性骑行者的数量 (45072)
	select count(*) from tb_trip_1 where gender=1;

当我们将文件数据导入到Hive中后，原来在hdfs本目录下的`20190601-3.csv`会被自动放入以下路径`/hive/warehouse/nybikedb.db/tb_trip_1/`，相当于该文件交给hive来管理

####hadoop启动遇到问题----------------------------

启动hadoop的命令
start-dfs.sh
start-yarn.sh

如果`jps`命令后发现少进程，应该到hadoop的logs目录下，查找对应的日志文件，阅读日志文件中的异常信息，来锁定问题的原因。




关闭hadoop的命令
stop-dfs.sh
stop-yarn.sh

####----------------------------

作业提交格式：

压缩文件，文件名是自己的姓名，里面是作业要求的内容

注意不要拿别人的内容来提交

目录：ftp上的作业提交文件夹