> 默认已经配置好了mybatis了     
>如果没有配置好，请参考 [springBoot&&mybatis](https://blog.csdn.net/zhiyikeji/article/details/85019689)
# 接下来开始我们的正文：
## 1.引入相关的jar包，在pom.xml文件中:
``` xml
<!-- https://mvnrepository.com/artifact/com.github.pagehelper/pagehelper-spring-boot-starter -->
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.2.10</version>
</dependency>
```
## 2.在application.properties文件中添加一下配置
``` yml
#pagehelper分页插件配置
pagehelper.helperDialect=mysql
pagehelper.reasonable=true
pagehelper.supportMethodsArguments=true
pagehelper.params=count=countSql
```
## 3.在controller层使用
``` java
@ResponseBody
	@RequestMapping(value="/getYoutube",method=RequestMethod.GET)
	public Map<String, Object> getYoutube(@RequestParam(value = "pn", defaultValue = "1") Integer pn,HttpServletResponse response) {
		response.setHeader("Access-Control-Allow-Origin", "*");
		Map<String, Object> map=new HashMap<String, Object>();
		// 表示从第pn查，每一页显示5条数据
		PageHelper.startPage(pn, 10);// 后面紧跟的这个查询就是分页查询
		List<Youtube>lYoutubes= YouTubeService.getYoutube();
		PageInfo page = new PageInfo(lYoutubes, 5);// 5:表示每次只显示5页的导航菜单
		map.put("cartoons",page);
		return map;
	}
```
前端接收解析即可