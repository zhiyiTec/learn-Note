# 1.在controller层使用session的方式：之间在形参里面定义HttpSession session，下面会具体举一个详情，但是使用这种方法会有一个很大的弊端就是两个controller中的session并不是共享的，如果直接使用这种方法：
AController:
``` java
   	@ResponseBody
	@GetMapping(value="/confirm")
	public Map<String, Object>    confirmUser(@RequestParam("keySecretInfo") String keySecretInfo,HttpSession session) {
		Map<String, Object>map=new HashMap<String,Object>();
		session.setAttribute("keySecretInfo", keySecretInfo);
		return map;
	}
```
BController:
```java
    @ResponseBody
	@GetMapping("/get")
	public Map<String, Object> get(HttpSession session) {
		Map<String, Object> map = new HashMap<String, Object>();
		String user=String.valueOf(session.getAttribute("keySecretInfo"));
		return map;
	}
```
我们会发现BController接收到的值为空，因为BController与AController之间的session不共享，解决办法：
还是A,B两个Controller
AController:
```java
    @ResponseBody
	@GetMapping(value="/confirm")
	public ModelAndView    confirmUser(@RequestParam("keySecretInfo") String keySecretInfo,  HttpServletResponse response,HttpSession session) {
		response.setHeader("Access-Control-Allow-Origin", "*");
		ModelAndView mav = new ModelAndView("redirect:/get");
		String re[]=keySecretInfo.split("-");
		String user=re[0];
		String keySecret=re[1];
		session.setAttribute("user", user);
		session.setAttribute("keySecret", keySecret);
		return mav;
	}
```
AController返回的视图层，此时
> ModelAndView mav = new ModelAndView("redirect:/get");

这句话会重定向到get这个视图层，而且会将sessionId一同传过去，所以BController:
```java
    @ResponseBody
	@GetMapping("/get")
	public Map<String, Object> get( HttpServletResponse response,HttpServletRequest request,HttpSession session) {
		response.setHeader("Access-Control-Allow-Origin", "*");
		Map<String, Object> map = new HashMap<String, Object>();
		String user=String.valueOf(session.getAttribute("user"));
		String keySecret=String.valueOf(session.getAttribute("keySecret"));
		map.put("user", user);
		map.put("keySecret", keySecret);
		return map;
	}
```
这样的话两个session之间就会共享
# 如果不理解或者有什么问题可以在下面留言，我看到会及时回复