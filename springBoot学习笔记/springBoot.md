# 1.springBoot前期准备
* 1.环境配置：jdk,maven
* 2.编写工具：sts(Spring Tool Suite)
* 3.在sts里面配置maven   
以上百度自行解决   
# 2.使用springBoot APi自动创建第一个maven项目
* 1.进入这个网址：https://start.spring.io/
* 2.进行如下配置：[点击查看](https://pan.baidu.com/s/1RpD7RtyQ65ghRCPiZnor-g)
* 3.下载好刚刚创建的Maven项目止之后进行导入：   
    右单击->import->maven->exsiting Maven projects->选中项目文件夹  点击导入即可     
### 判断是否导入成功的标志是：
#####    打开java目录下的.java文件，运行，控制台出现以下内容即视为导入成功  [点击查看运行结果](https://pan.baidu.com/s/1Y6H7Fzw_MtXH1DdU3xNwcQ)
### 下面讲一下创建的项目每一个文件夹所存放以及用于存放的内容     
* [点击查看](https://pan.baidu.com/s/1kWpLCtUfLstMSLIPU4Fviw)
#### springBoot运行程序时如果发现端口号被占用的问题，请参考文档    
* [解决端口号被占用的问题.docx](https://pan.baidu.com/s/1ejUnMbOWO9VOwhkOhfK9OQ)
#### 如果在浏览器上运行时出现：
```
Whitelabel Error Page This application has no explicit mapping for /error, so you are seeing this as a fallback. Tue Jun 30 17:24:02 CST 2015 There was an unexpected error (type=Not Found, status=404). No message available
```
那么就是因为你所创建的包不在springboot的主配置类所在包内，[点击查看详情](https://stackoverflow.com/questions/31134333/this-application-has-no-explicit-mapping-for-error)
* 什么叫做springboot的主配置类
  >含有注解@SpringBootApplication的类，比如默认创建好的主配置类是这样子的：
```
package com.test.HelloWord;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class HelloWordApplication {
	public static void main(String[] args) {
		SpringApplication.run(HelloWordApplication.class, args);
	}
}
```
要想使用注解，创建的包必须全部在package com.test.HelloWord内部
### 举一个例子
* 有效的包名：package com.test.HelloWord.controller;
* 无效的包名：package com.test.controller;
#### 下面讲一下常见的一些注解：
* @SpringBootApplication:springboot的主配置类，该注解包含:
> 1.@SpringBootConfiguration  ------- 2. @EnableAutoConfiguration
      
>  1.@SpringBootConfiguration
> 
这个注解又包含：
> @Configuration,它表示配置类:
> * 该类是一个配置类
> * 加了这个注解会自动放入spring 容器

> 2. @EnableAutoConfiguration：使用springBoot可以自动配置，摆脱了ssm中使用spring.xml,mybatis.xml,以及springmvc.xml文件配置的繁琐，工作原理就是就是找到主配置类所在的包，并将该包以及所在的子包纳入控制器

> spring 在启动时会根据D:\MAVENRes\org\springframework\boot\spring-boot-autoconfigure\2.1.0.RELEASE\spring-boot-autoconfigure-2.1.0.RELEASE.jar下面的/META-INF/spring.factories自动加载第三方jar包

@Conditional注解：
* @ConditionalOnBean（仅仅在当前上下文中存在某个对象时，才会实例化一个Bean）
* @ConditionalOnClass（某个class位于类路径上，才会实例化一个Bean）
* @ConditionalOnExpression（当表达式为true的时候，才会实例化一个Bean）
* @ConditionalOnMissingBean（仅仅在当前上下文中不存在某个对象时，才会实例化一个Bean）
* @ConditionalOnMissingClass（某个class类路径上不存在的时候，才会实例化一个Bean）
* @ConditionalOnNotWebApplication（不是web应用）
* 更多注解请参考 [@Controller扩展注解](https://pan.baidu.com/s/1uRKS5GLMVD9OjPZ_Bt1Bfw)
### 如何知道系统中开启了那些自动装配，或者禁止了哪些自动装配
> 在application.properties加入debug=true即可
* Positive matches:中包含了所有开启的配置
* Negative matches:中包含了所有未开启的配置
# 3.配置文件以及ymls使用
> 1.配置文件的作用：就是对默认的配置进行修改   

> 2.默认的全局配置文件：   
* 1.application.properties 如何使用：key=value的形式
* 2.application.yml key:空格value(注意yml不是文本标记语言，什么是文本标记语言：xml文件就是文本标记语言，因为xml文件符合下面这种格式：)
```
<server>
    <port>8888</port>
    </server>
```
而yml如何实现更改端口，参考下面代码：
```
server:
       port: 8888   注意‘:’与8888之间存在空格
```
要注意port要与server垂直对齐
> 3.具体如何修改默认配置举一个小例子：
```
默认端口是8080,如果我想修改成其他的端口号只需要这步操作即可：
server.port=8081，只需要这一句话即可以把端口号改为8081
```
> 4.在yml文件中对象属性进行操作：   

直接看代码：
```
package com.test.HelloWord.po;
@Component//作用是将此bean放入spring容器
@ConfigurationProperties(prefix="StudentPo")//作用是将StudentPo能够被yml文件识别，并能对其进行属性的注入
public class StudentPo {
	private String name;
	private int age;
	private boolean sex;
	private Data birthday;
	private Map<String, Object> location;
	private String hobbbies[];
	private List<String> skills;
	private PetPo pet;
	此处省略构造函数以及get set方法
}
```
而yml文件中的内容如下：
```
StudentPo:
 name: zx
 age: 21
 sex: true 
 birthday: 2018/11/21
 location: {province: 江苏省,city: 南京市,zone: 玄武区}//注：这种是对map函数的赋值方法,此处虽然没有加引号，但是如果字段里面有转意符，比如\n,\t等，要想使转意生效，就必须加双引号
 hobbbies: 
  - 唱歌
  - 运动         //这种是对数组进行赋值的方法
 skills:
  - 计算机
  - 软件开发    //这种是对数组进行赋值的方法
 pet:
  nickName: luckliy
  strain: 哈士奇      //这种是对属性为对象的赋值方法
```
测试语句如下：
```
@RunWith(SpringRunner.class)
@SpringBootTest
public class HelloWordApplicationTests {
	@Autowired
	StudentPo stu;//由于已经将student加上注解：@Component//作用是将此bean放入spring容器，所以可以进行自动注入
	@Test
	public void contextLoads() {
		System.out.println(stu.toString());
	}

}
```
# 4.yml通过@ConfigurationProperties 和@Value方式注入值
* @ConfigurationProperties:是为了能够让配置文件识别这个对象
* @Value:是给单个属性赋值
@Value用法：
```
public class StudentPo {
	@Value("zx")//加上这条注解之后name的值就变为zx
	private String name;
	@Value("23")//age就变为23
	private int age;
	}
```
#|@ConfigurationProperties|@Value                      
:----|:----:|----
注值|批量注入|单个                     
spEL|不支持|支持
JSR303|支持|不支持
注入复杂类型|支持|不支持
复杂类型：除了（8个基本类型，String,Date类型以外的都是复杂类型）
>下面重点讲解一下JSR303校验的用法：
```
@Component//作用是将此bean放入spring容器
@ConfigurationProperties(prefix="student")//作用是将StudentPo能够被yml文件识别，并能对其进行属性的注入
@Validated//开启jsr303数据校验
public class StudentPo {
	@Email
	private String emial
	}
```
通过注解@PropertySource来加载不是默认配置文件的文件，注：默认配置文件只有两种：           

* application.properties
* application.yml
* 除此之外都不是默认配置文件
具体如何使用@PropertySource，参考下面代码
>先看看conf.properties
```
student.age=66
```
再接着看如何使用:
```
@Component//作用是将此bean放入spring容器
@ConfigurationProperties(prefix="student")//作用是将StudentPo能够被yml文件识别，并能对其进行属性的注入
@Validated//开启jsr303数据校验
@PropertySource(value= {"classpath:conf.properties"})//作用是引入配置文件
public class StudentPo {
	private int age
	}
```
但是这个注解有个缺陷就是仅支持.properties文件
# 5.@ImportResource，配置类 ，占位符表达式
### 1.@ImportResource的使用：
* 用于引入xml配置文件，由于springBoot已经帮我们配置好了类似于spring.xml类型的配置文件，所以当我们直接获取spring容器时就会出现错误，但是如果我们就是想使用自己的配置文件，此时只有在主程序中加入@ImportResource注解，详情如下：
```
@SpringBootApplication
@ImportResource({"classpath:spring.xml"})//此处是新加入的
public class HelloWordApplication {
	public static void main(String[] args) {
		SpringApplication.run(HelloWordApplication.class, args);
	}
}
```
具体如何调用这个xml文件，我们先看看这个xml文件的内容：
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:p="http://www.springframework.org/schema/p"
	xmlns:context="http://www.springframework.org/schema/context"
	xsi:schemaLocation="
   http://www.springframework.org/schema/beans 
   http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
   http://www.springframework.org/schema/aop 
   http://www.springframework.org/schema/aop/spring-aop-3.0.xsd
   http://www.springframework.org/schema/tx 
   http://www.springframework.org/schema/tx/spring-tx-3.0.xsd
   http://www.springframework.org/schema/context      
   http://www.springframework.org/schema/context/spring-context-3.0.xsd">
	<bean id="PetPo" class="com.test.HelloWord.po.PetPo">
	<property name="nickName" value="zhuxu"></property>
	<property name="strain" value="哈士奇"></property>
	</bean>
</beans>
```
对应的PetPo对象：
```
package com.test.HelloWord.po;

public class PetPo {
	private String nickName;
	private String strain;
	对应的get set方法已经省略，但是一定要加进去，否则属性就无法注入
}
```
对应的测试程序：
```
@RunWith(SpringRunner.class)
@SpringBootTest
public class HelloWordApplicationTests {
	@Autowired
	ApplicationContext ac;//此处是为了获取spring容器
	@Test
	public void test1() {
		PetPo petPo= (PetPo)ac.getBean("PetPo");
		System.out.println(petPo.toString());
	}}
```
但是并不推荐这种方式进行属性的注入，太麻烦，推荐使用配置类
### 2.配置类
>配置类就是配置文件（.xml文件）配上注解的形式,如何创建配置类：
* 在原来普通的类的基础上加上注解：@Configuration
* 但是一般配置类要和@Bean同时使用，@Bean就是为了能够像spring.xml中<bean></bean>标签一样，能够创建多个
具体怎么使用参考下面代码：
```
@Configuration//加上他之后这个类就是配置类
public class AppConfig {
	@Bean//加上它之后就相当于创建了一个<bean></bean>标签
	public PetPo ppp() {/*ppp相当于<bean id="" class=""></bean>中的id*/
		PetPo p=new PetPo();
		return p;
	/*返回的结果类型就相当于<bean id="" class=""></bean>中的class*/
	}
}
```
下面写一个测试方法自己感受一下
```
@RunWith(SpringRunner.class)
@SpringBootTest
public class HelloWordApplicationTests {
	@Autowired
	ApplicationContext ac;//此处是为了获取spring容器
	@Test
	public void test1() {
		PetPo petPo= (PetPo)ac.getBean("p");
		System.out.println(petPo.toString());
	}
}
```
### 3.占位符表达式
* 常见的占位符[点击查看](https://pan.baidu.com/s/1rAg10AWjiagHs_15poeWCA)
```
student.age=${}
```
# 6.springBoot多环境设置及切换
* 默认情况下boot会读取application.properties环境下的端口
* 多个环境:application-环境名.properties,比如：
```
application-dev.properties
application-test.properties
```
至于具体怎么切换：就是在主配置文件(application.properties)中加入：
```
spring.profiles.active=dev
```
表示切换到dev下的端口环境
### 通过yml文件切换环境：
```
server:
  port: 1234
---
server:
  port: 8880
spring:
  profiles: dev//用于声明环境名为dev
---
server:
  port: 8881
spring:
  profiles: test  //用于声明环境名test
```
这样的话就创建好了三个环境，但是至于使用哪一个环境，就得使用这样的配置：
```
在主端口中这样声明：
server:
  port: 1234
spring:
  profiles:
    active: dev    //切换到端口到dev环境
```
### 如何动态切换环境：
* 1.使用命令行：
```
右单击 ->Run As->RunConfigurations->Arguments->在里面输入--spring.profiles.active=环境名
比如：--spring.profiles.active=dev
```
* 2.打成jar在cmd里面执行，下面先讲解一下如何打成jar包
```
右单击项目->Run As->maven build,进入之后在package即可
```
下面再接着叙述如何在cmd中运行打成的jar包
* 进入cmd
* 先进入这个jar包所在的目录  然后输入指令
```
java -jar HelloWord-0.0.1-SNAPSHOT.jar --spring.profiles.active=dev
```
* 3.通过jvm参数指定
```
右单击 ->Run As->RunConfigurations->Java Application->HellowdApplication(此处为项目名，项目不同名字也不一样)->右边的Argument,
输入 -Dspring.profiles.active=dev
```
# 7.SpringBoot配置文件位置
>springBoot能够默认读取的文件有两种，一个是application.properties以及application.yml文件   
>但是这两个文件可以存放在哪一个位置，就是在
* file:项目根目录/config
* file:项目根目录
* classpath:项目根目录/config
* classpath:项目根目录
file与classpath的区别就是
* file指普通目录
* classpath指构建路径（构建路径的文件夹上面有一个小标识）
如果项目配置冲突，优先级从上往下
# 8.外部配置文件以及加载顺序问题
### 配置项目运行名
在主配置文件application.properties中加入：
```
server.servlet.context-path=/springBoot
```
注意：此处的springBoot就是新加入的项目名，在未加入之前访问是这样的：
```
http://localhost:8888/HelloWord?name=zhuxu
```
加了之后就变成了这样的：
```
http://localhost:8888/springBoot/HelloWord?name=zhuxu
```
## 如何使用外部的配置文件
比如说在我的这个路径下C:\Users\17732\Desktop\test\application.properties有一个application.properties文件，那么怎么使用里面的配置：
```
右单击 ->Run As->RunConfigurations->Arguments->在里面输入--spring.config.location=路径名
比如：--spring.config.location=C:\Users\17732\Desktop\test\application.properties
```
如果内部外部配置有冲突，优先选择外部的
> 接着学习一下如何通过cmd命令调用外部配置文件
```
java -jar HelloWord-0.0.1-SNAPSHOT.jar --spring.config.location=C:\Users\17732\Desktop\test\application.properties
```
> 设置某一个参数，还是按照这个步骤（右单击 ->Run As->RunConfigurations->Arguments）到Arguments下
> 比如说只更改端口：--server.port=8882
# 9.springBoot的日志处理
### 目前springBoot用的是slf4j以及logback日志
具体如何使用日志参照下面代码：
```
@RunWith(SpringRunner.class)
@SpringBootTest
public class HelloWordApplicationTests {
	Logger logger=LoggerFactory.getLogger(HelloWordApplicationTests.class);
	@Test
	public void testLog() {
		logger.trace("测试Logger_Trace");
		logger.debug("测试Logger_debug");
		logger.info("测试Logger_Info");
		logger.warn("测试Logger_warn");
		logger.error("测试logger_error");
	}}
```
但是在测试时发现只能输出info warn 以及error中的内容，其他的内容均为输出，这是由于日志级别的问题
日志级别有：
```
trace debug info warn error fail off 
```
其中默认的级别是 info，只打印info以后的，而Info以前的不给予打印
### 下面继续认识一下如何自定义日志级别
在主配置文件application.properties中设置：
```
logging.level.com.test.HelloWord=debug
其中com.test.HelloWord是主配置类的包名
```
这样的话就把日志的默认级别也就是最低级别调到debug
## 继续深入————如何把日志输出信息打印到文件中呢
```
在主配置文件application.properties中设置：
logging.file=D:/program/springBoot/HelloWord/log/springBoot.Log
这样的话就可以把日志信息加入到上面目录下的springBoot.Log文件中
当然还有logging.path=D:/
这样的话就直接把日志输出指定的文件夹中，默认的文件名是spring.log
```
### 下面接着看如何更改日志输出的格式
> 指定日志显示格式：
* 1.日志显示在控制台：
```
在主配置文件application.properties中设置：
logging.pattern.console=%d{yyyy-MM-dd} [%thread] %-5level %logger{50} -%msg%n
```
>下面解释一下上面这串代码的意思：
* %d:日期时间
* %thread:打印线程名
* %-5level:显示日志级别，-5表示从左显示5个字符宽度
* %logger{50}：设置日志宽度，50表示最多只能有50个日志
* %msg：日志消息
* %n:表示显示完自动换行
* 2.日志显示在文件中：
```
在主配置文件application.properties中设置：
logging.pattern.file=%d{yyyy-MM-dd} ** [%thread] **  %-5level **  %logger{50} **  %msg%n
```
# 10.springBoot处理web静态资源
## 1.先pom.xml文件中导入jquery，Bootstrap等静态资源文件：
* jquery:
```
<dependency>
		<groupId>org.webjars</groupId>
		<artifactId>jquery</artifactId>
		<version>3.3.1-1</version>
	</dependency>
```
* BootStrap
```
<!-- https://mvnrepository.com/artifact/org.webjars/bootstrap -->
<dependency>
    <groupId>org.webjars</groupId>
    <artifactId>bootstrap</artifactId>
    <version>4.1.3</version>
</dependency>
``` 
下面简单的进行对jquery.js进行访问：
```
http://localhost:1234/zhiyi/webjars/jquery/3.3.1-1/jquery.js
```
注意：开始的是从webjars开始的
### 下面在看一下怎么引入自己写的静态资源，自己写的静态资源放在哪里
* 首先自定义的资源只能放在构建路径下的static或者resources目录下面
* 在访问静态资源时不用写前缀目录，比如有一个文件a.html在resources目录下，那么在访问时：
```
http://localhost:1234/zhiyi/Hello.html
```
### 欢迎页的实现：
> 在任意静态资源目录下，只要文件名叫做index.html，它就是主页,直接访问即可：
```
http://localhost:1234/zhiyi
```
### 下面接着看看如何更改网站的logo，任何一个网站中的logo都有一个固定名字：favicon.ico
那么如何进行更改favicon.ico呢
> 我们只需要将favicon.ico放在任何静态资源目录中即可
如何自定静态资源位置：
```
在主配置文件application.properties中设置：
spring.resources.static-locations=classpath:/res/
```
然后在src/main/resources下创建对应的res目录，这样的话静态资源目录除了默认的resources以及static目录，res现在也是静态资源目录了
同样访问的时候也不需要加前缀res，直接输入文件名即可：
```
http://localhost:1234/zhiyi/res.html
```
如果创建多个资源路径就这样：
```
spring.resources.static-locations=classpath:/res/ ,classpath:/img/
```
注意：一旦自定义了，默认的静态资源文件夹就会全部失效
# 11.引入模板引擎thymeleaf
### 上面学习了如何引入静态资源，那么如何引入动态资源
> springBoot是不支持动态页面jsp，但是如何来替换jsp页面呢，那么就使用我们的动态模板引擎thymeleaf
那么到底什么是模板引擎：
> 模板引擎就是将一个网友分为两部分：
* 模板
* 数据   
如何引用这个数据引擎:   
##### 在pom文件中添加依赖，这个依赖可以在maven里面直接搜索，也可以在这个网址：
> https://docs.spring.io/spring-boot/docs/2.1.0.RELEASE/reference/htmlsingle/#using-boot-starter
```
<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter</artifactId>
		</dependency>
		<dependency>
			<groupId>org.thymeleaf</groupId>
			<artifactId>thymeleaf-spring5</artifactId>
		</dependency>
		<dependency>
			<groupId>org.thymeleaf.extras</groupId>
			<artifactId>thymeleaf-extras-java8time</artifactId>
		</dependency>
```
导入之后我们来研究第一个问题：引入thymeleaf 代码应该往哪里写
> thymeleaf的代码全部放在构建路径(src/main/resources/)下的templete目录下
下面先看一个模板：
templete目录下的html:
```
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
<title>Thymleaf</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head> 
<body>
<p th:text="${welcome}">Welcome to thymeleaf!</p>
</body>
</html>
```
> 先看一下上面这个代码片段，其他的都是模板，以后直接拿着用，但是p中有一个th:text="${welcome}，会优先显示welcome中的内容   
那么总结一下：th：就是替换的意思,比如：
```
<p id="aaa" class="aaa" th:id="${welcome}" th:class="${welcome}"  th:text="${welcome}">Welcome to thymeleaf!</p>
```
那么如果${welcome}中有值，那么就就会有优先使用welcome中的值
在写一个controller：
```
@Controller
public class BootController {
	@RequestMapping("/wecome")
	public String wecome(Map<String, Object> map) {
		map.put("welcome", "welcome_Thymeleaf");
		return "result";
	}}
```
th后面到底可以存放哪些内容呢：
Order| Feature| Attributes                        
:----|:----:|----:         
1| Fragment inclusion| th:insert th:replace
2| Fragment| iteration| th:each
3|Conditional evaluation| th:if th:unless th:switch th:case
4| Local variable definition |th:object th:with
5| General attribute modification| th:attr th:attrprepend th:attrappend
6| Specific attribute modification |th:value th:href th:src ...
7 |Text (tag body modification)| th:text th:utext
8|Fragment specification |th:fragment
9| Fragment removal| th:remove
下面重点讲一下 th:text,th:untext
* th:text:表示转义，何为转义，举一个小小的例子：
```
th:text="<h1>hello</h1>"
th:untext="<h1>hello</h1>"
```
第一个显示的是大大的标题hello,而第二个显示的是‘《h1》hello《/h1》’
下面写一个关于th：each的用法：
html页面：
```
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
<title>Thymleaf</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link rel="stylesheet"
	href="webjars/bootstrap/4.1.3/css/bootstrap.min.css">
<link rel="stylesheet"
	    href="webjars/bootstrap/4.1.3/css/css/bootstrap-theme.min.css">
<script src="webjars/jquery/3.3.1-1/jquery.js"></script>
<script src="webjars/bootstrap/4.1.3/css/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="container">
		<table class="table table-striped table-bordered">
			<thead>
				<tr>
					<th>姓名</th>
					<th>年龄</th>
				</tr>
			</thead>
			<tbody>
				<tr th:each="student : ${Students}">
					<td th:text="${student.name}">姓名</td>
					<td th:text="${student.age}">年龄</td>
				</tr>
			</tbody>
		</table>
	</div>
</body>
</html>
```
对应的controller:
```
@Controller
public class BootController {
	@RequestMapping("/wecome")
	public String wecome(Map<String, Object> map) {
		map.put("welcome", "welcome_Thymeleaf");
		List<Student> lStudents = new ArrayList<Student>();
		lStudents.add(new Student("zx", 21));
		lStudents.add(new Student("zx1", 22));
		lStudents.add(new Student("zx3", 23));
		lStudents.add(new Student("zx4", 24));
		map.put("Students", lStudents);
		return "result";
	}}
```
对应的Po：
```
public class Student {
	private String name;
	private Integer age;
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public Integer getAge() {
		return age;
	}
	public void setAge(Integer age) {
		this.age = age;
	}
	public Student() {
		super();
	}
	public Student(String n,Integer a) {
		super();
		this.name=n;
		this.age=a;
	}}
```
# 12.SpringBoot整合外置tomcat以及使用jsp开发
> springBoot是不支持jsp开发的，因为jsp页面需要打成war包部署到tomcat，但是springBoot是不用打成war包就能运行，这个时候就需要使用外置的tomcat

下面接着讲一个maven的小知识：     
##### 如果pom中的依赖中有provided字样，那么在打包时不会将q以对应的插件或者文件一起打包
接着进入我们的主题：如何使用外置的tomcat，参考 [点击此处](https://pan.baidu.com/s/1G9xXbqOxcINSDSCnjDqDQQ)
然后进行下面几个步骤：   

* 1.建立基本的web目录结构：在src/main/webapp里面建立一个目录：WEB-INF
* 2.在src/main/webapp下面写jsp页面
下面讲一下如何在springBoot中配置视图解析器；   
在主配置文件application.properties中添加如下代码:
```
spring.mvc.view.prefix=/
spring.mvc.view.suffix=.jsp
```
index.jsp:
```
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Insert title here</title>
</head>
<body>
Hello ${requestScope.name} Welcome to Index.jsp
</body>
</html>
```
Controller:
```
@Controller
public class WebController {
	@RequestMapping("/welcome")
	public String welcome(Map<String, Object>map) {
		map.put("name", "朱旭");
		return "index";
	}}
```
