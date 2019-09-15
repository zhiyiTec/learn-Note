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

	在项目中添加dbcp-1.4.jar的依赖

	将`DBUtils.java`拷贝到`cn.tedu.nybike.util`包下

	从ftp上下载`jdbc.properties`文件，拷贝到项目的`src/main/resources`文件夹下

	在`DBUtils.java`中添加一个`main`方法，通过`ds`获取一个连接对象，并输出，测试连接是否正常

	将JSON解析得到的数据以对象的形式来封装，使用的类是`cn.tedu.nybike.pojo.StationStatusDO`

	`parseObject(String text, TypeReference<T> type, Feature... features) `可以对一个JSON字符串进行解析，并将解析到的数据自动封装成`TypeReference<T>`指定的类型

	JSON -> 变量 -> 使用T对应的对象封装变量 ->方法返回T的对象，里面就是封装好的数据

- 使用SQL对数据库中的数据进行分析

需求：`abi`在0.5以下的站点数量占总站点数量的比例

1. 通过JDBC将分析的结果从数据库查询出来，并显示在控制台

2. 自学Echarts(数据可视化工具)，网址是`https://www.echartsjs.com/zh/index.html`

### 11. 数据可视化

以图形的形式来展示数据，使人类可以更好的读懂和理解数据

例：2016年程序员中的男女比例是91:9

当前行业中有很多成熟的实现数据可视化的工具，适用于不同的应用场景。

传统：excel

浏览器端： Echarts(html+css+js)

编程语言自带可视化插件：R，Python

商用：BI(商业智能)

#### 11.1 第一个可视化图标

- 在页面中引入echarts.js

		<script type="text/javascript" src="js/echarts.min.js"></script>

- 在页面中声明一个图表的容器

		<div id="div1" style='height: 400px;width: 600px' ></div>

- 通过js设定图标的样式

		1. 声明一个图表对象，绑定容器

			var myChart = echarts.init(
				document.getElementById('div1'));

		2. 声明一个图表样式对象`option`

			可以从官方示例中下载

		3. 将样式对象绑定到图表对象上，显示图表

			// 使用刚指定的配置项和数据显示图表。
        	myChart.setOption(option);




### --------------------------
### 数据库连接池(pool)

概念：提供一个容器来管理连接，在连接池初始化之后一次性创建指定数量的连接，用户使用连接时，从连接池获取，用户使用完毕时，不关闭连接，而是将连接归还给连接池

工具：以上逻辑不需要开发者自己写，可以使用成熟的第三方jar包(c3p0.jar/dbcp.jar)

### try with close

语法：

	try(变量声明){

	}catch(Exception e){
		处理异常
	}

当`try-catch`语句块执行完毕后，系统会默认调用所有在`try()`中声明的变量的`close()`方法，自动关闭这些资源。

限制：在`try()`中声明的变量必须实现`AutoCloseable`接口
