### 9. 基于JavaEE，对请求第三方数据的过程进行优化，提高地图响应速度

分析：可以在web应用中添加功能，当服务器启动后，自动请求第三方的数据接口，获取站点信息数据和站点状态数据，并缓存在内存中。用户在页面上发送AJAX访问数据时，不再请求官方数据接口，而是请求web应用提供的数据接口，从缓存数据中读取数据，可以将约1000ms的耗时缩短为约20ms。

具体实现：

- 当前Web应用被加载后，自动周期性的发送http请求，获取站点信息数据和站点状态数据

		ServletContextListener

- 将获取到的数据使用JavaEE提供的标准组件缓存起来

		page/request/session/application

- Web应用需要对外提供一个url，供页面请求站点信息和站点状态数据

		Servlet

- 考虑并发读写缓存的线程安全问题

		同步代码库

常见的异常：

- station_info	404

	原因：检查Servlet映射的url是否是station_info

- json解析 unexcepted... S in json

	原因：Servlet中默认带的输出语句没有删除

- JSON.parse(infoResult)导致的问题

		如果服务器的Servlet没有通知浏览器本次响应的数据类型是json格式，那么浏览器的js中不能直接使用`infoResult.data.stations`来解析数据，会报错。

		解决方案：

		1. 页面解决：`infoResult = JSON.parse(infoResult)`，将返回的字符串变成JS对象

		2. 服务器端解决：response.setContentType("application/json;charset=utf-8");通知页面本次响应的数据类型是json，那么页面就不需要再添加 infoResult = JSON.parse(infoResult)，如果加了可能会报错

需求：参考info数据的实现过程，将status数据也实现缓存


### 10. 对站点状态数据进行初步的分析

####10.1 数据分析

数据分析是指用适当的统计分析方法对收集来的大量数据进行分析，提取有利于商业决策的信息。

大家学习的是如何为数据分析师提供一个分析的平台和环境。

需求：分析一条station_status.json数据，得到以下信息

	1. 该数据中有多少个站点

		select count(*) from tb_status;

	2. 所有的`num_bikes_avaliable`的总和

		select sum(nba) from tb_status;

	3. `num_bikes_avaliable`最多的站点的id

		select id from tb_status where nba=(select max(nba) from tb_tatus);

	4. `abi`在0.5以下的站点数量占总站点数量的比例

步骤：将一条statation_status.json数据存入数据库

- 安装一个数据库

		1. 从doc.tedu.cn下载MariaDB5.5安装包

		2. 在本机安装MariaDB5.5

			之前电脑中如果已经安装过Mysql，那么电脑中会有一个服务叫Mysql，在安装MariaDB时，使用的默认的服务名Mysql就会有冲突，因此需要将服务名改成MariaDB

			如果当前电脑中Mysql数据库正在运行，则会占用3306端口，安装MariaDB默认配置的也是3306端口，会冲突，因此无法继续安装。可以关闭当前电脑在运行的Mysql服务，解除它对3306端口的占用。
		
		3. 配置MariaDB5.5到环境变量中

- 建库建表

		-- 建库
		create database nybikedb;
		
		-- 使用库
		use nybikedb;
		
		-- 创建 tb_status
		create table tb_status(
		id int auto_increment,
		sid int comment '站点id',
		nba int comment '可用车数',
		nbd int comment '损坏车数',
		nda int comment '可用桩数',
		ndd int comment '损坏桩数',
		primary key (id)
		)default charset utf8;



- 基于JSON解析工具，将statation_status.json数据转变成结构化的数据

	在项目中引入fastjson的jar包，可以通过`http://maven.tedu.cn`搜索对应的依赖该怎么写

	maven的运行原理是从远程库中下载对应的jar包，下载完成后，不会进行文件完整性校验，可能出现项目列表中对应的jar包，结构也是完整的，但是一些类就是导不进来的情况。遇到这类情况，可以到本次的maven文件夹中(.m2)，找到对应的jar包的文件夹，直接删掉。在项目中使用`maven update`重新下载该jar包。
	

- 将数据存入数据库

- 使用SQL对数据库中的数据进行分析



### 数据的类型

常见的数据可以分为结构化数据、半结构化数据和非结构化数据。

结构化数据：就像excel表中数据，拥有行列结构，每一列的数据含义相同，数据类型相同，一行代表一条记录，不同行的数据共享同一个表头

半结构化的数据：就像json数据，数据有结构，但是结构不是那么清晰，不能简单的拆解成行列结构

非结构化数据：音频数据、视频数据、图片数据等


### 数据库

数据库的类型：网格型、层次型、关系型(主流)、非关系型(兴起)

关系型数据库的诞生：1970年左右，IBM的一名高级研究员通过论文，从数学的角度论证了关系型数据库的可行性。
	
关系型数据库的代表：

- Oracle：商业级，功能强大而完善，贵

- Mysql：轻量级，高效，开源免费

- MariaDB：Mysql的社区版，完全兼容Mysql，开源免费

### Iterator 迭代器

用于迭代访问一个集合中的所有元素



### 复习

结束了纽约市共享单车的地图服务

基于JavaEE对页面请求数据的速度进行优化
开发一个Web应用，当web应用加载完成后，自动周期性的请求第三方数据，缓存在内存中，对外提供2个接口，供页面访问

开发了`SCListener`，启动子线程，发送一个HTTP请求，获取站点信息数据，缓存到application作用域中



### -------------------------------

### 线程

什么是进程？
一个正在运行的程序。是计算机分配资源的最小单位。

什么是线程？
是运行在进程中的独立的代码片段(逻辑流)。是CPU调度的最小单位。
线程必须依赖于进程存在，同一个进程的所有线程，共享该进程被分配到的内存空间。

为什么会有线程？
一个程序在运行过程中，需要执行多个独立的逻辑流。
可以有效提高CPU的使用率

Java提供的线程API

	Thread t1=new Thread();
	t1.start();// 启动线程

	线程启动后，会争抢cup的时间片
	一个线程抢到时间片之后，执行的是run()方法中的逻辑
	开发者需要提供run()方法中的逻辑

	提供的方式：开发一个Runnable接口的实现类，实现run()方法

线程并发和同步问题

	如果多个线程每个都操作自己的变量，那么不会出现并发问题

	如果多个线程共同操作同一个变量，分2种情况：

	1. 如果所有的线程都是仅读取变量的值

	2. 多个线程对变量做更新(增、删、改)操作就有线程安全问题

	3. 一个线程读，一个线程改，可能有问题

如何解决线程并发问题？

- 加锁：同步代码块
	可以保证同一时间，只有一个线程能够执行同步代码块中的内容

	一写多读
	使用单纯的同步代码块，同一时间只能有1个线程读数据