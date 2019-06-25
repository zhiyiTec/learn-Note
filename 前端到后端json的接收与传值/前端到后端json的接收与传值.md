## 前端传值：
> 通过将要传输的数据封装为json，然后再通过ajax接收:
``` html
JSON.stringify(data)
```
后端接收值只需要通过一句话即可实现：
```
@RequestBody String param
```
此处的param就是你所接收的值
具体如何解析：
``` java
JSONObject jo=new JSONObject();
List<Map> parseArray = jo.parseArray(param, Map.class);
System.out.println("parseArray="+parseArray);
```
只需要这几句话即可
下面举一个小demo：
前端：
``` html
		$("#excelOutput").click(function(){
            	console.log("传出的数据="+JSON.stringify(excelData))
				$.ajax({
					url : "${App_Path}/excel",
					data:JSON.stringify(excelData),
					type : "post",
					dataType: "json",
					contentType: "application/json; charset=utf-8",//此处不能省略
					success : function(data) {
                        alert("success")
							},
					error:function(){
                        alert("fail")
					}
				});
		})
```
后端：
``` java
	@ResponseBody
	@RequestMapping(value = "/excel", method = RequestMethod.POST)
	public Msg excel(@RequestBody String param) throws Exception {
		System.out.println("param="+param);
		JSONObject jo=new JSONObject();
		List<Map> parseArray = jo.parseArray(param, Map.class);
        System.out.println("parseArray="+parseArray);
        for (Map map:parseArray) {
		System.out.println("map="+map);
		}
		return null;	
	}
```
以上就是传值与接收值的具体情况，当然也可以封装一个bean对象，直接转为bean也行   
### 下面继续拓展一个springMvc的知识，如果前端传值是通过这种方式：
``` html 
$("#excelOutput").click(function(){
            	console.log("传出的数据="+JSON.stringify(excelData))
				$.ajax({
					url : "${App_Path}/excel/"+result,
					data:JSON.stringify(excelData),
					type : "post",
					dataType: "json",
					contentType: "application/json; charset=utf-8",//此处不能省略
					success : function(data) {
                        alert("success")
							},
					error:function(){
                        alert("fail")
					}
				});
		})
```
上面传了两个值，一个是result，一个是excelData，看后端怎么处理：
``` java
@ResponseBody
	@RequestMapping(value = "/excel/{result}", method = RequestMethod.POST)
	public Msg excel(@RequestBody String param,@PathVariable String result) throws Exception{
        System.out.println("param="+param);
        System.out.println("result="+result);//result就是url : "${App_Path}/excel/"+result中的result
		JSONObject jo=new JSONObject();
		List<Map> parseArray = jo.parseArray(param, Map.class);
        System.out.println("parseArray="+parseArray);
        for (Map map:parseArray) {
		System.out.println("map="+map);
		}
		return null;	
	}
```