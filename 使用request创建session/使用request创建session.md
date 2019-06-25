# 1.创建session的两种方式：
* HttpSeesion session;
* request.getSession();
我们着重讲一下第二种方式：request.getSession();
# 2.request.getSession()：
* 1、无请求参数
``` java
request.getSession()
```
这种方式会获取当前request关联的session,如果当前request没有session,创建一个session.
* 2.有请求参数
```java
request.getSession(boolean b);
```
> * b=true:获取当前request关联的session,如果当前request没有session,创建一个session.
> * b=false:获取当前request关联的session,如果当前request没有session,就设置session=null