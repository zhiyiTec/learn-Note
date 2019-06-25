# 1.先解释一下为何使用ajax进行跨域访问controller层时所定义的session无法共享：
> Session:在计算机中，尤其是在网络应用中，称为“会话控制”。Session 对象存储特定用户会话所需的属性及配置信息。即服务端用于区分特定用户的数据结构。
> 一般的做法都是在客户端通过验证后，服务端将一个sessionId告诉客户端，在随后的通讯中，客户端将sessionId告诉服务端，
> 服务端通过验证sessionId的方法来确认客户端的身份。这里面的核心就是session是在服务端管理的，将id交给客户端用作区分。 
> 因此在跨域时，需要在各个环节上都要保证客户端的sessionid不能丢失，否则就会被服务端拦截，无法获取服务的问题。
# 2.具体如何解决：
### 1.首先自己配置一个拦截器，当然也可以不配置拦截器，自己在每个接口处添加解决跨域的方法：
先写一下拦截器的内容，如果自己手动在每个Controller的接口处自己定义的话就忽略这段内容：
```java
public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletResponse res = (HttpServletResponse) servletResponse;
        HttpServletRequest request=(HttpServletRequest)servletRequest;
        res.setContentType("textml;charset=UTF-8");
        res.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));//设置允许跨域请求地址即为当前请求地址
        res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
        res.setHeader("Access-Control-Max-Age", "0");
        res.setHeader("Access-Control-Allow-Headers", "Origin, No-Cache, X-Requested-With, If-Modified-Since, Pragma, Last-Modified, Cache-Control, Expires, Content-Type, X-E4M-With,userId,token");
        res.setHeader("Access-Control-Allow-Credentials", "true");//允许服务器向浏览器跨域响应时更改浏览器（客户端）的cookie
        res.setHeader("XDomainRequestAllowed","1");
        filterChain.doFilter(servletRequest,servletResponse);
    }
```
如果不用拦截器，请仔细阅读下面的代码：
```java
@ResponseBody
	@RequestMapping("/getUser")
	public Map<String, Object> getUser(HttpServletResponse response, HttpServletRequest request) {
		response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
		response.setHeader("Access-Control-Allow-Credentials", "true");//允许服务器向浏览器跨域响应时更改浏览器（客户端）的cookie
		Map<String, Object> map = new HashMap<String, Object>();

		HttpSession session = request.getSession(false);
		if (session != null) {
			String user = String.valueOf(session.getAttribute("user"));
			String keySecret = String.valueOf(session.getAttribute("keySecret"));
			map.put("status", true);
			map.put("user", user);
			map.put("keySecret", keySecret);

		} else {	
			map.put("status", false);
		}

		return map;
	}
```
这里我要说明一点，如果经常使用跨域的小伙伴可能熟悉这串代码：
```java
response.setHeader("Access-Control-Allow-Origin", "*");
```
正常情况下这串代码没有任何问题，但是一旦在ajax的访问请求中加上：
```js
xhrFields: {
           withCredentials: true
       },
crossDomain: true,
```
这是在使用通配符 “*”就会访问不到接口，会被CORS所拦截，所以改为：
```java
response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
```
到此后端的内容就结束了，再看一下ajax的写法：
```js
 $.ajax({
                url: "http://localhost:8080/getUser",
                // data: "sid=" + sid,
                type: "get",

                //加上这句话,允许浏览器向服务器跨域请求时携带cookie
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,

                success: function(data) {
                    console.log(data);
                },
                error: function() {
                    alert("非法登录");
                    // window.location.href = 'index.html';
                    throw "登录异常";
                }
            });
```
到此跨域导致的sessionId不一致从而导致Controller层中的sessio无法共享的问题就解决了，欢迎在下放讨论