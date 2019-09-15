### 7. 当点击一个站点时，弹出一个信息窗

为实现该功能，应该为每个`marker`添加一个点击事件，在点击事件中弹出信息窗。

根据百度地图API，在`marker`上显示信息窗一共分3步：

- 以字符串的形式声明信息窗内部的样式，该字符串中可以包含html的标签，这些标签在显示时会以html的形式来显示。同时，也可以通过css为这些html标签指定样式

		var sContent="<h4>这是自定义信息窗</h4>";

- 创建一个信息窗对象，绑定第一步声明的信息窗样式

		var infoWindow=new BMap.InfoWindow(sContent);

- 为`marker`添加一个点击事件，在被单击之后，弹出信息窗

		marker.addEventListener("click", function(){          
			this.openInfoWindow(infoWindow);
		});

需求：为地图上所有的站点`marker`添加点击事件，被单击时弹出一个信息窗，内容是：XXX的信息窗

注：`marker.addEventListener()`代码必须在`map.addOverlay(marker)`之前调用，不然会有BUG（所有的`marker`会绑定完全一致的信息窗）

为了提高代码的可维护性，将为`marker`添加点击事件的逻辑封装到一个单独的方法中`addMarkerInfoWindow()`，然后在`addMarker()`中调用该方法。

为简化学习流程，我们提供了一个`mapbox.html`，其中是仿照官方的信息窗写的简化版的信息窗，同时提供了配套的`page.css`文件。可以将这2个文件拷贝到项目中。

需求：点击信息窗时，弹出类似官方的信息窗，其中的数据目前可以是写死的

具体操作：

- 在`nymap2.html`中引入page.css文件

		<link rel="stylesheet" href="css/page.css">

- 将`mapbox.html`中和信息窗相关的`div`复制到`nymap.js`的`addMarkerInfoWindow(marker)`方法中，作为`sContent`变量的值，这里注意添加必要的`"`和`"+`，将所有标签拼接成一个字符串:

		var sContent="<div class='mapbox-content'>"+
			"<div class='mapbox-content-top'>"+
				"<span class='window_lastUpdate'> 0 ms ago </span> " +
				"<span class='window_info_button'></span>"+
			"</div>"+
			"<div class='mapbox-content-header'>"+
				"<h1 class='mapbox-content-header-stationName'>info_stationName</h1>"+
			"</div>"+
			"<div class='mapbox-content-detail'>"+
				"<div class='mapbox-content-detail-bikes-available'>"+
					"<span class='mapbox-content-detail-bikes-available-val'> 20 </span>"+
					"<span class='mapbox-content-detail-bikes-available-lbl'>Bikes</span>"+
				"</div>"+
				"<div class='mapbox-content-detail-docks-available'>"+
					"<span class='mapbox-content-detail-docks-available-val'> 6 </span> " +
					"<span class='mapbox-content-detail-docks-available-lbl'>Docks</span>" +
				"</div>"+
			"</div>"+
			"<div class='mapbox-content-footer'>"+
				"<span class='mapbox-content-footer-shortName'> Bike station:"+
					"info_shortName </span>"+
			"</div>"+
		"</div>";

### 8. 当点击一个站点时，显示站点的实时信息

首先，需要在`nymap.js`中声明一个函数`StationDetail`，用来模拟封装站点详情的类。

	function StationDetail(){}

在`nymap2.html`中声明一个全部变量`detailMap`，是`Map`类型的，用于保存站点的`id`和`StationDetail`对象的对应关系。

在获取到站点状态数据的函数中，遍历站点状态数据，创建`StationDetail`的对象，封装该站点的`nba`和`nda`，并将`StationDetail`的对象保存到`detailMap`中。

	var sDetail=new StationDetail();
	sDetial.nba=nda;

在获取到站点信息数据的函数中，遍历站点信息数据，使用站点`id`从`detailMap`中获取对应的`StationDetail`对象，向其中添加站点的`name`和`short_name`属性的值。

修改`addMarker()`和`addMarkerInfoWindow()`2个方法的参数列表，新添加一个id参数。

在`addMarkerInfoWindow()`方法中，使用参数`id`从`detailMap`中查询对应的`StationDetail`对象，将获取到的数据拼接生成`infoWindow`的内容。


### 小总结

目前基于百度地图实现了纽约市官方的共享单车地图服务。

- 将复杂的问题拆分成可实现的步骤

- 学习第三方插件及API的能力

- 百度地图API
	给自己命题可以掌握的更好

- 对纽约市提供的站点信息数据和站点状态数据有了解

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





### 答辩必选的功能1

在地图上实现可用桩的信息提示。



### -----------------------------

### URL

统一资源定位符，用于定位互联网上的一个资源

URL的语法：

	协议://域名(ip)：端口号/项目路径/资源路径

	http://localhost:8080/nybike/nymap2.html

	jdbc:mysql://localhost:3306/mydb1

	ftp://10.6.6.2

	https://

	file://

id和域名的关系：
浏览器在访问一个互联网上的主机时，使用的是对方的ip地址，但是ip地址对人类来说非常难记，因此人们发明了域名。一个域名对应1到多个ip地址。

常用的域名和ip:

	127.0.0.1	localhost	本机
	0.0.0.0					本机

人类在记网站时，记住域名就可以`www.baidu.com`，浏览器会使用 **DNS解析** 服务，将域名转换成对应的ip地址，再访问网络

**DNS解析**就是将域名转变成对应的ip地址的服务

**DNS解析**首先提供服务的是本机的缓存和`hosts`文件


端口号：

用于区别一台主机对外提供服务的不同的程序。

常见的端口号：

	8080:Tomcat

	3306:Mysql

	80：当前主机的默认端口，当Url中不包含端口号时，默认访问的就是80端口


### 项目的搜索/查询速度如何优化？

从2000条数据中快速查询某条数据

	List<Student> list=new ArrayList();
	//...

	for(Student st:list){
		if(st.getName().equals("张三")){
			...
		}
	}

	优化：创建一个Map集合<String name, Student st>
	一次遍历，将name和Student存入map集合
	后续多次查询，直接从map中获取

	Map map=new HashMap();

### 缓存

将需要频繁使用的数据保存在内存中

### JavaEE提供的监听器

监听者模式

23种软件设计模式之一，可以实现事件监听与事件处理逻辑的分离。事件的监听往往需要底层组件的支持，开发难度较大。因此通过运用监听者模式，对于事件的监听一般由平台或者组件来实现(大神帮你写完了)，开发者仅需要提供具体事件的处理逻辑就行了。

	<button id="bt1" value="点我！">

	<script>
		$("#bt1").click(function(){
			alert(666);
		});
	</script>


JavaEE提供了多种监听器(Listener)，号称是JavaEE的三大组件之一。这些监听器可以监听一个Web应用在运行过程中的各类事件，例如：

- 特殊对象的创建和销毁：
			
		ServletRequestListener：监听Request对象被创建和销毁

		HttpSessionListener：监听session对象被创建和销毁

		ServletContextListener：监听ServletContext对象被创建和销毁

- 特殊对象中添加了值、更新了值和删除了值：

		ServletRequestAttributeListener

		HttpSessionAttributeListener

		ServletContextAttributeListener

JavaEE监听器的开发步骤：

- 自定义一个类，并实现对应的监听器接口

- 实现接口中定义的所有抽象方法，在对应的方法中添加事件发生之后的处理逻辑

- 在web.xml中配置该监听器

	  	<!-- 配置监听器 -->
		  <listener>
		  	<listener-class>cn.tedu.nybike.listener.SCListener</listener-class>
		  </listener>



面试题：简述ServletContext的生命周期(创建，活多久，销毁)

ServletContext代表的是一个Web应用，当Tomcat启动后，每加载完成一个Web应用，就会创建一个ServletContext对象，唯一代表该Web应用。ServletContext对象被创建后，会一直驻留在内存中，直到当前服务器关闭或者当前Web应用被移出容器时。


- 简述线程的生命周期
- 简述Servlet的生命周期
- 简述Request的生命周期
- 简述Session的生命周期





Java提供了3个版本，JavaSE(桌面应用程序,java..)，JavaEE(Web应用程序,javax..)，JavaME(很少用)


### 复习

实现纽约市地图的服务功能

- 显示纽约市地图

	1. 引入百度地图的js文件，使用密钥
	2. 页面上提供一个地图的容器`<div>`
	3. 百度地图API

		var map=new BMap.Map("container");

		var point=new BMap.Point(经度，纬度);

		map.centerAndZoom(point,15);

- 在地图上显示所有的纽约市站点

	1. 通过AJAX请求站点信息`station_infomation.json`数据
	2. 通过js获取json中的`stations`数组，遍历该数据，获取每个站点的经纬度
	3. 调用百度地图API，创建Marker,并且将marker显示在地图上

	var marker=new BMap.Marker(point,...);

- 使用不同图标显示纽约市站点

	1. 通过AJAX请求站点状态数据`station_status.json`
	2. 通过js获取`stations`数组
	3. 遍历该数组，获取每个站点的`nba`和`nda`，然后计算该站点的`bikeLevel`
	4. 将站点的id和`bikeLevel`保存到一个Map集合中
	5. 在生成站点标注时，根据id获取`bikeLevel`，动态拼接成imgUrl

- 在地图缩放时，修改站点的图标

	1. 当地图缩放级别大于14且正在使用小图标时，将图标换为大图标`img/bi_N.png`
	2. 当地图缩放级别小于15且正在使用大图标时，将图标换为小图标`img/si_N.png`
	3. 在页面上添加一个缩放级别改变的监听,在监听器中获取当前页面缩放级别，判断是否需要改变图标，如果需要，调用`switchIcon()`方法修改图标
		
		map.addEventListener("zoomend",function(){
			
		})
	4. `switchIcon()`中需要先判断是将大图标改成小图标，还是相反

	遍历所有的marker,获取它的Icon的imageUrl，替换成对应的图标的imageUrl，生成新的Icon，并调用marker的setIcon()方法，设置新Icon