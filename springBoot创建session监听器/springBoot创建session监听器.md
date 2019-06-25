# 1.建立session监听，要实现HttpSessionListener接口,加上注解@WebListener
```java
 public class SessionListener implements HttpSessionListener { 
        public void sessionCreated(HttpSessionEvent httpSessionEvent) {  
            HttpSession session = httpSessionEvent.getSession();  
            myc.addSession(session);  
        }  

        public void sessionDestroyed(HttpSessionEvent httpSessionEvent) {  
            HttpSession session = httpSessionEvent.getSession();  
            myc.delSession(session);  
        }
 }
   
```
# 2.启动类加上注解@ServletComponentScan，这样才能扫描到监听器
### 简单说下，javaWeb中配置监听器在web.xml中加上
```xml
<listener> 
  <listener-class>zjq.listener.SessionListener</listener-class> 
 </listener>
```
# 3.下面举一个通过sessionId获取会话的例子来具体阐述
### 1.先新建一个MySessionContext类
``` java
package com.boot.zhiyi.util;

import java.util.HashMap;

import javax.servlet.http.HttpSession;

public class MySessionContext {
	private static MySessionContext instance;
	private HashMap<String, HttpSession> sessionMap;

	private MySessionContext() {
		sessionMap = new HashMap<String, HttpSession>();
	}

	public static MySessionContext getInstance() {
		if (instance == null) {
			instance = new MySessionContext();
		}
		return instance;
	}

	public synchronized void addSession(HttpSession session) {
		if (session != null) {
			sessionMap.put(session.getId(), session);
		}
	}

	public synchronized void delSession(HttpSession session) {
		if (session != null) {
			sessionMap.remove(session.getId());
		}
	}

	public synchronized HttpSession getSession(String sessionID) {
		if (sessionID == null) {
			return null;
		}
		return sessionMap.get(sessionID);
	}
}

```
这个代码可以直接拿来copy，不用做任何修改
### 2.在刚刚你创建的SessionListener监听器里面，修改你实现的两个方法：
* sessionCreated
* sessionDestroyed
具体如下：
```java
package com.boot.zhiyi.listerner;

import javax.servlet.annotation.WebListener;
import javax.servlet.http.HttpSession;
import javax.servlet.http.HttpSessionEvent;
import javax.servlet.http.HttpSessionListener;

import com.boot.zhiyi.util.MySessionContext;
@WebListener
public class SessionListener implements  HttpSessionListener{
	 private MySessionContext myc = MySessionContext.getInstance();  
	@Override
	public void sessionCreated(HttpSessionEvent se) {
		HttpSession session = se.getSession();  
        myc.addSession(session); //将你创建的session会话加入到map接口中
        //下面这句代码用于设置session的声明周期
        session.setMaxInactiveInterval(3);//以秒为单位，即在没有活动30分钟后，session将失效
	}

	@Override
	public void sessionDestroyed(HttpSessionEvent se) {
		// TODO Auto-generated method stub
		 HttpSession session = se.getSession();  
         myc.delSession(session);  //此处用于将你的session对象从map中移除
	}
	
}

```
### 3.具体获取sessionId的方法：在Controller中：
```java
@ResponseBody
	@GetMapping("/get")
	public Map<String, Object> get(@RequestParam("sid") String sid, HttpServletResponse response,HttpServletRequest request) {
		response.setHeader("Access-Control-Allow-Origin", "*");
		Map<String, Object> map = new HashMap<String, Object>();
		MySessionContext myc= MySessionContext.getInstance();  
//		HttpSession session = request.getSession().getSessionContext().getSession(sid); 这个方法已经被废弃
		HttpSession session = myc.getSession(sid);  //此处就是通过sessionId获取session信息
		if(session!=null) {
			String user=String.valueOf(session.getAttribute("user"));
			String keySecret=String.valueOf(session.getAttribute("keySecret"));
			map.put("user", user);
			map.put("keySecret", keySecret);
		}
				
		return map;
	}
```