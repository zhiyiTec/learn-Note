# 1.Spring Boot：
 
* server.session.cookie.comment = ＃注释会话cookie。
* server.session.cookie.domain = ＃会话cookie的域。
* server.session.cookie.http-only =＃“HttpOnly”标志为会话cookie。
* server.session.cookie.max-age = ＃会话cookie的最大年龄（以秒为单位）。
* server.session.cookie.name = ＃会话cookie名称。
* server.session.cookie.path = ＃会话cookie的路径。
* server.session.cookie.secure = ＃“Secure”标志为会话cookie。
* server.session.persistent = false ＃在重新启动之间持续会话数据。
* server.session.store-dir = ＃用于存储会话数据的目录。
*  server.session.timeout = ＃会话超时（秒）。
* server.session.tracking-modes =＃会话跟踪模式（以下一个或多个：“cookie”，“url”，“ssl”）。
# 2.Web容器中，如Tomcat里可以设置超时时间为30分钟 
# 3.在web.xml中的session-config配置 
session-timeout元素用来指定默认的会话超时时间间隔，以分钟为单位。该元素值必须为整数。如果session-timeout元素的值为零或负数，则表示会话将永远不会超时。如，设置session失效时间为30分钟： 
``` xml
<session-config> 
     <session-timeout>30</session-timeout> 
</session-config> 

```
# 4.4、在程序中调用session的setMaxInactiveInterval方法设置
``` java
session.setMaxInactiveInterval(30 * 60);  
```
注：setMaxInactiveInterval设置的是当前会话的失效时间，不是整个web的时间，单位为以秒计算。如果设置的值为零或负数，则表示会话将永远不会超时。常用于设置当前会话时间。