###4 在地图上显示纽约市的站点

想要显示所有的纽约市站点，需要获取所有站点的经纬度信息，纽约市在网上公开了这部分信息，具体的网址是`https://www.citibikenyc.com/system-data`，数据说明介绍网站为`https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson`，各类数据url列表为`http://gbfs.citibikenyc.com/gbfs/gbfs.json`

已经知道目标数据的url，希望在页面上动态请求数据，并且在获取到数据后，可以基于js动态改变html页面的样式，传统的请求方式无法满足这一需求，通用的解决方案是 **AJAX**

在页面中想要使用jQuery发送AJAX请求，首先需要引入jQuery文件。

	<script type="text/javascript" src="js/jquery-1.11.0.min.js"></script>

在`nymap2.html`中添加AJAX请求的代码，在页面刷新后直接发送请求，获取站点信息数据，并显示在浏览器的控制台上：

	// 发送AJAX请求，获取站点信息数据
	var infoUrl="https://gbfs.citibikenyc.com/gbfs/en/station_information.json";
		
	$.get(infoUrl,function(infoResult){
		// 封装收到响应之后执行的逻辑
		// infoResult代表收到的响应数据
		console.log(infoResult);
		
	});

注：如果直接在浏览器上访问本地的`nymap2.html`文件，是不允许通过AJAX获取外部数据的，浏览器的控制台会报`403`错误，需要将项目部署到Tomcat服务器，通过`http://localhost:8080/nybike/nymap2.html`访问页面，才可以发送AJAX请求

需求：在控制台输出所有的站点的id，经度和纬度

代码如下：

	// 发送AJAX请求，获取站点信息数据
	var infoUrl="https://gbfs.citibikenyc.com/gbfs/en/station_information.json";
		
	$.get(infoUrl,function(infoResult){
		// 封装收到响应之后执行的逻辑
		// infoResult代表收到的响应数据

		// 从结果数据中获取站点信息数组
		var stations=infoResult.data.stations;
		for(var index in stations){
			var id=stations[index].station_id;
			var lon=stations[index].lon;
			var lat=stations[index].lat;
			console.log(id+"~"+lon+"~"+lat);
		}
	});

获取了站点的经纬度之后，可以动态生成该站点对应的`Point`对象，再调用`addMarker()`方法，在地图上显示站点的标注，代码如下：

	// 发送AJAX请求，获取站点信息数据
	var infoUrl="https://gbfs.citibikenyc.com/gbfs/en/station_information.json";
		
	$.get(infoUrl,function(infoResult){
		// 封装收到响应之后执行的逻辑
		// infoResult代表收到的响应数据

		// 从结果数据中获取站点信息数组
		var stations=infoResult.data.stations;
		for(var index in stations){
			var id=stations[index].station_id;
			var lon=stations[index].lon;
			var lat=stations[index].lat;
			// 创建Point对象，封装站点经纬度
			var point=new BMap.Point(lon,lat);
			// 在地图上添加站点标注
			addMarker(point,"img/bi_0.png",new BMap.Size(41,50),new BMap.Size(20,50));
		}
	});

###5 使用不同的图标去显示站点

分析：先确定使用不同图标的标准

标注：

	nba=0 或 bike和dock都为0 	->	level 0	->红色
	nba<5	->	level 1	->黄色
	abi<0.5	->	level 2	->少绿
	0.5<= abi <1	->	level 3	->多绿
	abi=1	->	level 4	->全绿
	

	可用车指数(abi)=nba/(nba+nda)

首先，在`nymap.js`中添加一个方法`getBikeLevel()`,接收一个站点的可用车数量和可用桩数量，返回计算得到的bikeLevel，代码如下：

	function getBikeLevel(nba,nda){
		// nba=0 或 bike和dock都为0 	->	level 0	->红色
		if(nba==0 || (nba+nda)==0){
			return 0;    
		}
		// nba<5	->	level 1	->黄色
		if(nba<5){
			return 1;
		}
		// 可用车指数(abi)=nba/(nba+nda)
		var abi=nba/(nba+nda); // number
		// abi<0.5	->	level 2	->少绿
		if(abi<0.5){
			return 2;
		}
		// 0.5<= abi <1	->	level 3	->多绿
		if(abi>=0.5 && abi<1){
			return 3;
		}
		// abi=1	->	level 4	->全绿
		if(abi==1){
			return 4;
		}
	}

在`nymap2.html`上添加发送AJAX的代码，请求站点状态数据，计算bikeLevel，并添加到bikeLevelMap中，代码如下：

	// 发送AJAX请求，获取站点的状态数据
	$.get(statusUrl,function(statusResult){
		// 从结果数据中获取stations数组
		var stations=statusResult.data.stations;
		// 遍历stations数组
		for(var index in stations){
			// 获取一个站点的id
			var id=stations[index].station_id;
			// 获取一个站点的nba
			var nba=stations[index].num_bikes_available;
			// 获取一个站点的nda    
			var nda=stations[index].num_docks_available;
			// 调用方法，计算站点的bikeLevel
			var bikeLevel=getBikeLevel(nba,nda);
			// 将站点的id和bikeLevel存入bikeLevelMap
			bikeLevelMap.set(id,bikeLevel);
			// 将站点的id,bikeLevel,nba,nda输入到控制台
			console.log(id+"~"+bikeLevel+"~"+nba+"~"+nda);
		}
	});

在`nymap2.html`上修改请求到站点信息数据后执行的逻辑，从bikeLevelMap中查询站点的bikeLevel，拼接生成imgUrl，调用`addMarker()`生成站点标注。另外，因为2个AJAX是异步执行的，可能出现后一个请求先返回的情况，为保证逻辑顺序，应该将请求站点信息的AJAX代码放到请求站点状态的AJAX的callback函数中，代码如下：

	var infoUrl="https://gbfs.citibikenyc.com/gbfs/en/station_information.json";
	var statusUrl="https://gbfs.citibikenyc.com/gbfs/en/station_status.json";
	
	// 用于保存站点的bikeLevel的Map集合
	var bikeLevelMap=new Map();	
	
	// 发送AJAX请求，获取站点的状态数据
	$.get(statusUrl,function(statusResult){
		// 从结果数据中获取stations数组
		var stations=statusResult.data.stations;
		// 遍历stations数组
		for(var index in stations){
			// 获取一个站点的id
			var id=stations[index].station_id;
			// 获取一个站点的nba
			var nba=stations[index].num_bikes_available;
			// 获取一个站点的nda    
			var nda=stations[index].num_docks_available;
			// 调用方法，计算站点的bikeLevel
			var bikeLevel=getBikeLevel(nba,nda);
			// 将站点的id和bikeLevel存入bikeLevelMap
			bikeLevelMap.set(id,bikeLevel);
			// 将站点的id,bikeLevel,nba,nda输入到控制台
			console.log(id+"~"+bikeLevel+"~"+nba+"~"+nda);
		}
		
		// 发送AJAX请求，获取站点信息数据
		$.get(infoUrl,function(infoResult){
			// 从结果数据中获取站点信息数组
			var stations=infoResult.data.stations;
			for(var index in stations){
				var id=stations[index].station_id;
				var lon=stations[index].lon;
				var lat=stations[index].lat;
				// 创建Point对象，封装站点经纬度
				var point=new BMap.Point(lon,lat);
				// 从bikeLevelMap中查询当前站点的bikeLevel
				var bikeLevel=bikeLevelMap.get(id);
				// 拼接生成imgUrl
				var imgUrl="img/bi_"+bikeLevel+".png";
				// 在地图上添加站点标注
				addMarker(point,imgUrl,new BMap.Size(41,50),new BMap.Size(20,50));
			}
		});
	});

###6. 当缩放级别改变时，修改站点图片的样式

分析：当地图的缩放级别大于等于15时，应该使用大图标，当缩放级别小于15时，应该使用小图标

在`nymap.js`中添加一个方法`switchIcon()`，当缩放级别合适时，调用`switchIcon()`,弹出缩放级别改变的提示


使用方案二或者方案三的前提是保存了所有的`Marker`，因此需要一个全局变量，是`Marker`的数组，并修改`addMarker()`方法的逻辑，将创建好的`marker`添加到数组中：

	// 将marker对象添加到marker的数组中
    markerArr.push(marker);

为了方法调用方便，并增加页面的可维护性，分别将小图标的Size和锚点Size，大图标的Size和锚点Size以全局变量的形式保存：

	var bigIconSize = new BMap.Size(41,50);// 大图标的Size
	var bigAnchorSize = new BMap.Size(20,50);// 大图标的锚点Size
	var smallIconSize = new BMap.Size(10,10);// 小图标的Size
	var smallAnchorSize = new BMap.Size(5,10);// 小图标的锚点Size

完成`switchIcon()`方法的逻辑：

	function switchIcon(isBigIcon){ // isBigIcon代表当前应该使用什么图标
		// 遍历markerArr
		for(var index in markerArr){
			// 获取marker的icon的imageUrl
			var imageUrl=markerArr[index].getIcon().imageUrl;
			// 声明2个临时变量
			var iconSize;
			var anchorSize;
			// 针对当前应该使用的图标类型，获取对应的imageUrl，iconSize和anchorSize
			if(isBigIcon == true){
				imageUrl=imageUrl.replace(/s/,"b");
				iconSize=bigIconSize;
				anchorSize=bigAnchorSize;
			}
			if(isBigIcon == false){
				imageUrl=imageUrl.replace(/b/,"s");
				iconSize=smallIconSize;
				anchorSize=smallAnchorSize;
			}
			// 创建新的Icon
			var opts={
					anchor: anchorSize,
					imageSize : iconSize // Icon内部图片的大小
						};
			var myIcon = new BMap.Icon(imageUrl,iconSize,opts);
		   
			// 调用Marker的setIcon方法，设置新的Icon
			markerArr[index].setIcon(myIcon);
		}
	}
	
在`nymap2.html`中为地图添加缩放级别变化监听：

	// 为地图添加缩放结束事件
	map.addEventListener("zoomend", function(){ 
		var zoomLevel=this.getZoom();
		
		if(zoomLevel>14 && isBigIcon == false){
			isBigIcon=true;// 当前应该使用大图标
			switchIcon(isBigIcon);
		}
		if(zoomLevel<15 && isBigIcon == true){
			isBigIcon=false;
			switchIcon(isBigIcon);
		}
	});

###作业

创建一个`nymap3.html`和`nymap3.js`，将目前实现的功能重新实现一遍，做到不参考之前的代码。



#### ----------------------------------
#### JavaScript
JavaScript是一门基于对象的，事件驱动的脚本语言

JavaScript来自网景公司，网景公司是浏览器的鼻祖

网景公司开发JavaScript这门语言的目的，就是在浏览器上与用户进行互动，最初起名叫“liveScript”，热度不高，后来网景公司吸收了Java的面向对象的思想，将"liveScript"改名为"JavaScript"，热度很高

#### AJAX

AJAX是异步的JS和XML，用于在浏览器上发送异步请求，并在获取到结果之后实现页面的布局刷新。

AJAX并不是一项新的技术或者独立的语言，是引用已有技术实现的解决方案。

- 异步请求
同步请求：一次请求发出后，在收到响应之前，页面出于阻塞状态，不能进行其他操作，在收到响应后，才能继续执行

异步请求：一次请求发出后，在收到响应之前，页面可以执行其他操作，甚至可以发送多次请求

异步请求：
- 优点：用户体验高
- 缺点：并不适用于所有场景

实现页面发送AJAX的方式：

- 原生JS：代码量较大，现在用的比较少

- 基于jQuery：

		语法：一共提供了4种发送AJAX请求的方式

		第一种：

			$.get(url,data,callback);
			url: 本次请求的目标路径
			data： 本次请求携带的请求参数
			callback: 当收到响应之后，所执行的逻辑


#### jQuery

是JavaScript的函数库，里面是大量写好的JavaScript的方法，一些复杂的功能不再需要开发者自己写，可以在页面上引入jQuery文件，然后直接调用它的方法。

口号：写的更少，做的更多

注：jquery.1.11.0.min.js文件中是没有注释和缩进的，原因是实际使用中，这样的文件大小较小，可以减少文件传输的消耗。如果想查看其中的内容，可以下载文件名中不含min的文件。