## 实现纽约市地图服务功能

###1. 分析

当拿到一个复杂的需求时，应该按照“由易到难”的顺序将需求进行拆分。

	1. 显示纽约市地图
	2. 在地图上显示一个指定的标注
	3. 在地图上显示纽约市的站点
	4. 使用不同的图标去显示站点
	5. 当缩放级别改变时，修改站点图片的样式
	6. 当点击一个站点时，弹出一个信息窗
	7. 当点击一个站点时，显示站点的实时信息

###2. 显示纽约市地图

在html上显示地图，一般使用第三方提供的地图服务，也称为地图插件。常用的地图服务有 **百度地图**， **高德地图**, **腾讯地图**，本次实训中使用**百度地图**。

- 开发者如何使用百度地图？
百度官方提供了教程页面，在`http://lbsyun.baidu.com/index.php?title=jspopular3.0`可以学习

- 申请称为百度地图开发者，创建应用，获取对应的密钥(AK)

	xyHbWbqlRvxIMj9jytG5HknuA3pwygA5

####2.1 开发第一个地图用例

在Eclipse中创建一个maven项目，打包方式选择`war`包，项目名为`nybike`

点击自动生成`WEB-INF/web.xml`

在`webapp`下创建`firstmap.html`

将官方的Hello World示例代码复制到`firstmap.html`中，替换所有内容，并添加自己的密钥

将`firstmap.html`拖拽到浏览器页面上，查看能否正常显示地图

####2.2 代码解释

想要在页面上显示一个地图，需要满足几个条件：

- 页面上引入了百度地图的js文件

		<script type="text/javascript" src="http://api.map.baidu.com/api?v=3.0&ak=xyHbWbqlRvxIMj9jytG5HknuA3pwygA5">
		//v3.0版本的引用方式：src="http://api.map.baidu.com/api?v=3.0&ak=您的密钥"
		</script>

- 在页面上声明一个地图的容器，一般是`<div>`，通过控制该容器在页面上的位置和样式，可以控制地图显示的位置和样式

		<div id="container"></div> 

- 通过js调用百度地图API，生成地图

		// 创建地图实例，关联容器的id
		// BMap是百度地图API所有类的外部类，用于和其他API进行区分，例如高德地图API的所有类的外部类为AMap
		var map = new BMap.Map("container");
		
		// 创建点坐标，先经度，后纬度
		var point = new BMap.Point(116.404, 39.915);
		
		// 初始化地图，设置中心点坐标和地图级别  
		map.centerAndZoom(point, 15);


####2.3 显示纽约市地图

需求：在`webapp`目录下创建`nymap1.html`，在页面上显示纽约市地图，以纽约市帝国大厦为中心点，缩放级别使用14

代码实现：

	// 创建地图实例  
	var map = new BMap.Map("container");
	
	// 创建点坐标，先经度，后纬度 40.7482100000,-73.9856350000
	var point = new BMap.Point(-73.985635,40.748210);
	
	// 初始化地图，设置中心点坐标和地图级别  
	map.centerAndZoom(point, 14);

####2.4 开启滚轮缩放并添加平移缩放控件

需求1：在`nymap1.html`上开启地图的“滚轮缩放”功能，并添加“平移缩放控件”

需求2：将“平移缩放控件”在地图的右下角显示

代码如下：

	// 开启鼠标滚轮缩放
	map.enableScrollWheelZoom(true);
	
	// JSON opts =options
	var opts = {
				offset: new BMap.Size(15, 30),
				anchor: BMAP_ANCHOR_BOTTOM_RIGHT
				}
	
	// 开启平移缩放控件
	map.addControl(new BMap.NavigationControl(opts));

###3. 在地图上显示一个指定的标注

####3.1 在地图上显示一个指定的标注

需求1：在帝国大厦位置添加一个默认标注(Marker)

代码如下：

	// 创建标注    
	var marker = new BMap.Marker(point); 
	// 将标注添加到地图中
	map.addOverlay(marker);
	
	var marker2=new BMap.Marker(new BMap.Point(-73.9870, 40.7479));
	map.addOverlay(marker2);

需求2：在显示marker时使用的是自定义的图片(`img/bi_0.png`)

从 **2前端组件及素材包** 文件夹中拷贝 **img** 文件夹到项目的`webapp`目录下，**img** 文件夹中是本项目中可能用到的一些图片资源。

代码如下：

	function addMarker(point){  // 创建图标对象   
	    var imgUrl = "img/bi_0.png"; // 图片的url
		var iconSize = new BMap.Size(41, 50); // Icon的大小
		var opts={
				anchor: new BMap.Size(20, 50), // Marker定位点相对于Icon左上角的偏移量
				imageSize : iconSize // Icon内部图片的大小
					};
		
		var myIcon = new BMap.Icon(imgUrl,iconSize,opts);
		
	    // 创建标注对象并添加到地图   
	    var marker = new BMap.Marker(point, {icon: myIcon});    
	    map.addOverlay(marker);    
	} 
	
	addMarker(point);

####3.2 提高代码规范性

复制`nymap1.html`，生成`nymap2.html`

在`webapp`目录下创建`js/nymap.js`，在该文件中保存页面中用到的js方法

从`nymap2.html`中剪切`addMarker()`方法的代码，粘贴到
`js/nymap.js`中，然后对方法进行修改，将其中所有写死的变量以参数的形式传进来，代码如下：

	// 在地图上添加一个marker的方法
	// point marker在地图上的位置
	// imgUrl Icon使用的图片的url
	// iconSize Icon的大小，即可视区域大小
	// anchorSize point相对于Icon左上角的偏移量
	function addMarker(point,imgUrl,iconSize,anchorSize){  // 创建图标对象   
		var opts={
				anchor: anchorSize,
				imageSize : iconSize // Icon内部图片的大小
					};
		var myIcon = new BMap.Icon(imgUrl,iconSize,opts);
	    // 创建标注对象并添加到地图   
	    var marker = new BMap.Marker(point, {icon: myIcon});    
	    map.addOverlay(marker);    
	}

在`nymap2.html`中引用`js/nymap.js`文件

	<script type="text/javascript" src="js/nymap.js"></script>

修改`nymap2.html`中的代码，调用信息的`addMarker()`方法

	addMarker(point,"img/bi_0.png",new BMap.Size(41,50),new BMap.Size(20,50));

###4 在地图上显示纽约市的站点

想要显示所有的纽约市站点，需要获取所有站点的经纬度信息，纽约市在网上公开了这部分信息，具体的网址是`https://www.citibikenyc.com/system-data`，数据说明介绍网站为`https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson`，各类数据url列表为`http://gbfs.citibikenyc.com/gbfs/gbfs.json`

已经知道目标数据的url，希望在页面上动态请求数据，并且在获取到数据后，可以基于js动态改变html页面的样式，传统的请求方式无法满足这一需求，通用的解决方案是 **AJAX**


#### AJAX

AJAX是异步的JS和XML，用于在浏览器上发送异步请求，并在获取到结果之后实现页面的布局刷新。

AJAX并不是一项新的技术或者独立的语言，是引用已有技术实现的解决方案。

- 异步请求

- 布局刷新


#### JSON

JSON是现在非常流行的一种数据格式，用于保存具有结构性的数据，也用于在JS中作为对象存在


### 作业

需求：选择一个你旅行去过的地点，在地图上显示，并且在该地点显示你自己的照片

#### -------------------------------------

#### maven

- 解压缩

- 配置
	
	1. 本地库的路径
	2. 镜像：达内内网镜像+阿里云镜像


#### ftp
用于下载每天的笔记和其他内容的地方
操作方法：
- windows文件夹地址栏中输入：ftp://10.6.6.2/

- 文件夹空白处右键-> 登录 -> 输入用户名和密码
老师和学生通用：
账号：admin
密码：tedu.cn

- 本次实训所有资料在`1洛阳理工`文件夹下
每天的笔记、图片、代码会以`dayXX`压缩文件存放，如`day01.zip`


注：因公用一个账号，都有修改和删除权限，请同学们仅下载资料，不要修改或删除任何ftp上的文件