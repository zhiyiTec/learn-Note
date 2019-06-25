# 1.创建mave项目
> * 1.先创建一个maven项目，创建完成之后， 右单击项目->Build Path->Config Build Path->Java Build Path->Libaryies->Add Libary	->Server Runtime选择你安装tomcat 然后点击Apply;
> * 2.右单击项目->Build Path->Config Build Path->ProjectFacts->java(改为1,8版本)
> *3.右单击项目->Build Path->Config Build Path->ProjectFacts->Dynamic web module(先取消勾选，应用之后，再开它并且勾选，在下面的设置中设置为src/main/webapp)
> *4.在项目的pm.xml文件中引入项目依赖的jar包；
``` xml
	spring_jar:
	springmvc_jar:
	mybatis_jar:
	数据库连接池驱动包：
	其他jar包：
详情参考D:\ssm文件\pom.xml文件
```
# 2.引用bootStrap以及jquery
* 1.网络引用bootStrap
```html
<link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
	<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
```
当然也可以下载下来本地引用，但是要注意路径的配置   
* 2.引入jquery，可以使用本地的jqueery.js文件，也可在线引用
```
http://code.jquery.com/jquery-1.4.1.min.js
```
# 3.配置web.xml文件
### 1.配置web.xml文件：
#### <1>.先配置spring
```
  <!-- 此处是用于配置spring的配置文件 -->
    <param-name>contextConfigLocation</param-name>
    <param-value>
        <!-- 项目启动之后就会立刻加载这两个文件 -->
		classpath:conf/spring.xml;
		classpath:conf/spring-mybatis.xml
		</param-value>
```	
#### <2>.接下来配置springmvc前端控制器
```xml
 <!-- 配置spring-mvc的前端控制器，拦截所有请求 -->
	 <servlet>
    <servlet-name>sakila</servlet-name>
    <servlet-class>
			org.springframework.web.servlet.DispatcherServlet
	</servlet-class>
	</servlet>
	<servlet-mapping>
    <servlet-name>sakila</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>
```
#### <3>.配置好前端控制器之后顺手将字符编码拦截器,需要注意的是字符编码过滤器必须放在所有的过滤器之前
```xml
<filter>
    <filter-name>SpringEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <!-- 此处使用设置字符编码的初始属性 -->
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
    <init-param>
      <param-name>forceEncoding</param-name>
      <param-value>true</param-value>
    </init-param>
     <init-param>
      <param-name>forceRequestEncoding</param-name>
      <param-value>true</param-value>
    </init-param>
    <init-param>
      <param-name>forceResponseEncoding</param-name>
      <param-value>true</param-value>
    </init-param>
  </filter>
	 <filter-mapping>
    <filter-name>SpringEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
```
#### <4>.使用过滤器来使用reset风格的URI,目的是将页面发过来的post请求转换为我们指定的put/delete请求
```xml
<filter>
      <filter-name>HiddenHttpMethodFilter</filter-name>
     <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>
  </filter>
  <filter-mapping>
      <filter-name>HiddenHttpMethodFilter</filter-name>
      <url-pattern>/*</url-pattern>
  </filter-mapping>
```
# 4.配置spring-mvc
> spring-mvc包含网站的跳转，逻辑的控制等	
* 1.先在resources/conf下创建spring-mvc.xml文件；以下内容都是编写在此文件中
* 2.编写扫描器：
```xml
<!-- 用于扫描所有com包下面的业务逻辑组件 -->
	<context:component-scan
		base-package="com"  use-default-filters="false">
	    <!-- 此处的设置让它只扫描controller层 -->
	   <context:include-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
	</context:component-scan>
```		
* 3.配置视图解析器
```xml
<!-- 配置视图解析器 -->
	<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
	<property name="prrefix" value="/WEB-INF/view/"></property>
	<property name="suffix" value=".jsp"></property>
	</bean>
```
* 4.接下来就是两个标准配置，也就是将springMvc不能处理的请求交给tomcat
``` xml
<!-- 两个标准配置，也就是将springMvc不能处理的请求交给tomcat -->
	<mvc:default-servlet-handler/>
	<!-- 此处的设置是为了能支持springMvc更高级的一些功能，如JSr303校验，ajax请求等 -->
	<mvc:annotation-driven></mvc:annotation-driven>
```
# 5.配置spring
> spring主要是配置与业务逻辑有关的请求，比如数据源，业务控制等
* 1.先在resources/conf下创建spring.xml文件；一下内容都是编写在此文件中
* 2.配置c3p0连接池：
```xml
<!-- spring主要是配置与业务逻辑有关的请求，比如数据源，业务控制等 -->
	<bean id="ComboPooledDataSource"
		class="com.mchange.v2.c3p0.ComboPooledDataSource">
		<property name="jdbcUrl" value=""></property>
		<property name="driverClass" value=""></property>
		<property name="user" value=""></property>
		<property name="password" value=""></property>
	</bean>
```
* 3.为了能够以后方便操作数据库，把连接数据库的操作写在dbconflig.properties文件中，所以先在resources/conf下创建一个dbconflig.properties文件
```
	jdbc.jdbcUrl=jdbc:sqlserver://127.0.0.1:1433;DatabaseName=GXRLMis（jdbc:mysql://localhost:3306/ssm_crud  这个是mysql数据库的url）
		jdbc.driverClass=com.mysql.jdbc.Driver
		jdbc.user=root
		jdbc.password=123456
```
* 4.在spring,xml文件中引入该配置文件
``` xml
	<!-- 引入dbconflig.properties配置文件 -->
	  <context:property-placeholder location="classpath:dbconflig.properties"/>
```
注：这句话要写在步骤2上面
* 5.取dbconflig.properties中的值：
``` xml
<!-- spring主要是配置与业务逻辑有关的请求，比如数据源，业务控制等 -->
	<bean id="ComboPooledDataSource"
		class="com.mchange.v2.c3p0.ComboPooledDataSource">
		<property name="jdbcUrl" value="${jdbc.jdbcUrl}"></property>
		<property name="driverClass" value="${jdbc.driverClass}"></property>
		<property name="user" value="${jdbc.user}"></property>
		<property name="password" value="${jdbc.password}"></property>
	</bean>
```
* 6.加入扫描器，与spring-mvc不同的是，此扫描器除了controller不扫描，其余的全部需要扫描，此步骤写在最上面
``` xml
 <!-- 引入扫描器 -->
	  <context:component-scan base-package="com">
	      <!-- 除了controller不扫描，其余的全部需要扫描 -->
	      <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
	  </context:component-scan>
```	
* 7.配置和mybatis的整合
``` xml
<bean id="SqlSessionFactoryBean" class="org.mybatis.spring.SqlSessionFactoryBean">
	    <!-- 指定mybatis全局配置文件的位置 -->
	    <property name="configLocation" value="classpath:conf/mybatisconflig.xml"></property>
	    <!-- 配置数据源 -->
	     <property name="dataSource" ref="ComboPooledDataSource"></property>
	     <!-- 指定mybatis的mapper文件 -->
	      <property name="mapperLocations" value="classpath:mapper/*.xml"></property>
	</bean>
```
* 8.接下来配置扫描器，将mybatis接口的实现加入到ioc容器中
```xml
<!-- 配置扫描器，将mybatis接口的实现加入到ioc容器中 -->
	<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
	<!-- 注入sqlSessionFactory -->
		<property name="sqlSessionFactoryBeanName"
			value="SqlSessionFactoryBean" />
		<!--扫描所有的Mapper接口，加入到ioc容器中 -->
		<property name="basePackage" value="com.mapper"></property>
	</bean>
```	
* 9.接下来进行实物控制的配置
```xml
<!-- 事务控制 -->
	<bean id="DataSourceTransactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
	    <!-- 控制住数据源
	    所以先连接数据源ComboPooledDataSource
	     -->
	    <property name="dataSource" ref="ComboPooledDataSource"></property>
	</bean>
```	
* 10.开启事务：
> 开启基于注解的事务，使用xml的形式的事务（比较重要的事务都会用xml配置的方式） 
``` xml
 <!-- 事务控制 -->
	<bean id="DataSourceTransactionManager"
		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<!-- 控制住数据源 所以先连接数据源ComboPooledDataSource -->
		<property name="dataSource" ref="ComboPooledDataSource"></property>
	</bean>
	<!-- 开启基于注解的事务，使用xml的形式的事务（比较重要的事务都会用xml配置的方式） -->
	<aop:config>
		<!-- 切入点表达式 execution(* com.service..*()):所有com.service下的所有类以及所有方法,而（...）表示方法中的参数任意 -->
		<aop:pointcut
			expression="execution(* com.service..*(..))" id="txPoint" />
		<!-- 配置事务增强 -->
		<aop:advisor advice-ref="txAdvice" pointcut-ref="txPoint" />
	</aop:config>
	<!-- 配置事务增强，事务如何切入也就是事务增强之后如何进行切入 -->
	<tx:advice id="txAdvice" transaction-manager="DataSourceTransactionManager">
		<tx:attributes>
			<!-- 所有的方法都是事务方法 -->
			<tx:method name="*" />
			<!-- get开始的所有方法 -->
			<tx:method name="get*" read-only="true" />
		</tx:attributes>
	</tx:advice>
```
# 6.基础模块——修改Mapper
* 1.先在po中创建对应的bean
* 2.在mapper中创建mapper接口；（就举一个例子：在mapper中创建EmpMapper接口：
```java
public interface EmpMapper {
	public List<Emp> getEmpInfo();
}

```
* 3.在resource的mapper中创建对应的xml文件；EMpMapper.xml文件；
```xml
<mapper namespace="com.mapper.EmpMapper">
	<select id="getEmpInfo" resultMap="getEmpInfoReMap">
	select * from tbl_emp
	</select>
	<resultMap type="com.po.Emp" id="getEmpInfoReMap">
		<result column="emp_id" property="emp_id" />
		<result column="emp_name" property="emp_name" />
		<result column="gender" property="gender" /> 
		<result column="eamil" property="eamil" />
		<result column="dept_id" property="dept_id" />
	</resultMap>
</mapper>
```
# 7.基础模块的spring单元测试
* 1.如果不放心，可以在test文件中创建一个测试类
``` java
	public static void main(String[] args) {
		//1.创建springIoc容器/ssmProject/src/main/
		ApplicationContext ioc=new ClassPathXmlApplicationContext("../../resources/conf/spring.xml");
		//2,从容器中获取mapper
		EmpMapper bean=ioc.getBean(EmpMapper.class);
		List<Emp> lemp=bean.getEmpInfo();
		if(lemp.size()>=1) {
			for(Emp e:lemp) {
				System.out.println(e.getEmp_name()+"="+e.getEamil());
			}
		}
	}
```
* 2也可以进行单元测试：
> 1.先在pom.xml中导入spring test 这一单元测试类
> 2.在这个测试类上添加注解
```java 
/帮我们创建容器
			@RunWith(SpringJUnit4ClassRunner.class)
			//指定创建容器时使用哪个配置文件
			@ContextConfiguration(locations= {"classPath:spring.xml"})
```		
> 3.需要哪一个组件直接使用注解@Autowired进行自动装载(注：这个自动装载必须写在方法外面)
```java
@Autowired
			EmpMapper empMapper;
```		
> 4.需要测试哪一个方法就在这个方法上面添加注解@Test,测试的详细代码如下：
``` java
//帮我们创建容器
@RunWith(SpringJUnit4ClassRunner.class)
//指定创建容器时使用哪个配置文件
@ContextConfiguration(locations = { "classpath:conf/spring.xml" })

public class Test1 {
	@Autowired
	EmpMapper empMapper;

	@Test
	public void testEmpMaaper() {
		List<Emp> lEmps = empMapper.getEmpInfo();
		System.out.println(lEmps.size());
		if (lEmps.size() >= 1) {
			for (Emp em : lEmps) {
				System.out.println(em.getEmp_name() + "=" + em.getEamil());
			}
		}
	}
}
```
* 3.为了方便操作，我们要在spring.xml文件中进行配置一个可以批量执行的sqlSession
```
<!-- 配置一个可以批量执行的sqlSession -->
	<bean id="SqlSessionTemplate" class="org.mybatis.spring.SqlSessionTemplate">
	<constructor-arg name="sqlSessionFactory"  ref="SqlSessionFactoryBean"></constructor-arg>//此处的SqlSessionFactoryBean对应的是157行的SqlSessionFactoryBean
	<constructor-arg name="executorType"  value="BATCH"></constructor-arg>
	</bean>
```	
* 4.在刚刚我们创建的测试类中写测试语句，但是在写测试语句之前必须编写对应的mapper文件：
```java
EmpMapper：
		public interface EmpMapper {
	public List<Emp> getEmpInfo();
	public void  updateEmpById(Emp emp);
}
```
EmpMapper：对应的emp.xml文件：
``` xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
 PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!-- 先引入对应的扫描文件 -->
<mapper namespace="com.mapper.EmpMapper">
	<select id="getEmpInfo" resultMap="getEmpInfoReMap">
	select * from tbl_emp
	</select>
	<resultMap type="com.po.Emp" id="getEmpInfoReMap">
		<result column="emp_id" property="emp_id" />
		<result column="emp_name" property="emp_name" />
		<result column="gender" property="gender" /> 
		<result column="eamil" property="eamil" />
		<result column="dept_id" property="dept_id" />
	</resultMap>
	<!-- 用于更新数据库 -->
	<update id="updateEmpById" parameterType="com.po.Emp" >
	update tbl_emp 
	<set>
	<if test='emp_name != null and emp_name != "" '>
	emp_name=#{emp_name},
	</if>
	<if test='gender != null and gender != "" '>
	gender=#{gender},
	</if>
	<if test='eamil != null and eamil != "" '>
	eamil=#{eamil},
	</if>
	<if test='dept_id != null and dept_id != "" '>
	dept_id=#{dept_id},
	</if>
	</set> 
	 where emp_id=#{emp_id}
	</update>
</mapper>
```
测试语句：
```java
//帮我们创建容器
@RunWith(SpringJUnit4ClassRunner.class)
//指定创建容器时使用哪个配置文件
@ContextConfiguration(locations = { "classpath:conf/spring.xml" })

public class Test1 {
	@Autowired
	EmpMapper empMapper;
	@Autowired
	SqlSession sqlSession;
	//用于查询
	@Test
	public void getEmpInfo() {
		List<Emp> lEmps = empMapper.getEmpInfo();
		System.out.println(lEmps.size());
		if (lEmps.size() >= 1) {
			for (Emp em : lEmps) {
				System.out.println(em.getEmp_name() + "=" + em.getEamil());
			}
		}

	}
	//用于更新
	@Test
	public void updateEmpById() throws IOException {
		Emp m = new Emp(1,"zx", "female", "123@qq.com", 1);
		EmpMapper empMapper=sqlSession.getMapper(EmpMapper.class);
		empMapper.updateEmpById(m);
	}	
	//用于批量的插入数据
	@Test
	public void insertDeptByBATCH() {
		DeptMapper OCM=sqlSession.getMapper(DeptMapper.class);
		for(int i=0;i<10;i++) {
			String id=UUID.randomUUID().toString().substring(0, 5);
			OCM.insertByDept(new Dept(id));
		}
	}
}
```
注:对应的bean的构造方法没有添加，请自己添加
# 8.查询_分页后台代码的完成
* 1.主页面的执行流程：访问Index.jsp页面->index.jsp页面发送出查询信息列表的请求->EmpController来接受请求，然后查询出员工数据->跳转到list,jsp页面进行展示
* 2.在index.jsp中创建的内容：
```jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
	<!-- 直接请求emp，被控制器进行拦截转发 -->
<jsp:forward page="/emp"></jsp:forward>
```
* 3.创建对应的控制器EmpController：
```java
public class EmpController {
	public String getAllEmpInfo() {
		//我们有视图解析器所以返回的list，会自动给它添加前缀和后缀
		return "list";
	}}
```
* 4.由于视图解析对应的地址是
``` xml
<property name="prrefix" value="/WEB-INF/view/"></property>
<property name="suffix" value=".jsp"></property>
```
所以先在/WEB-INF/view/目录下创建list,jsp:
* 5.开始向数据库取数据，具体步骤是：先创建service接口->在serviceImpl中来实现具体的接口->在controller层中调用这个接口即可；
> <1>.创建EmpService:
```java
public interface EmpService {
	public List<Emp> getALlEmpInfo();
}
```
> <2>在serviceImpl中来实现具体的接口EmpServiceImpl:
```java
public class EmpServiceImpl implements EmpService {
	// service依赖于Dao
	@Autowired
	EmpMapper eMapper;
	@Override
	public List<Emp> getALlEmpInfo() {
		// TODO Auto-generated method stub
		return eMapper.getEmpInfo();
	}
}
```
但是如果数据较为庞大，每一次都查询所有的数据太过于繁琐，所以引入分页的组件PageHelper:
> 1.现在pom中引入pageHepler插件（直接在maven仓库中搜索pagehelper，选择对应的版本下载即可）
> 2.在mybatis的全局配置中注册分页组件：
```xml
<!-- 此标签的位置必须写在 <typeAliases>之后-->
	<plugins>
	    <plugin interceptor="com.github.pagehelper.PageInterceptor"></plugin>
	</plugins>
```
> 3.引用组件也特别简单，只需要在查询之前调用PageHelper.startPage方法即可；
> 在EmpController的getAllEmpInfo（）方法中调用，注意一定要写在查询之前，而且后面紧跟的这个查询就是分页查询；
> 接下来就对查询的分页结果进行包装,其中PageInfo中包含了这个页面的所有信息，所以只需要将pageInfo交给页面接收就行了：
> PageInfo page=new PageInfo(lemp,5);//5:表示每次只显示5页的导航菜单   
代码详情：
``` java
@Controller
	public class EmpController {
	@Autowired
	EmpService empService;
	//拦截emp请求
	@RequestMapping("/emp")
	public String getAllEmpInfo(@RequestParam(value="pn",defaultValue="1" ) Integer pn) {
		Map<String, Object> map = new HashMap<String, Object>(); 
		//为了方便快速查询，所以引入PageHelper分页查询
		//表示从第pn查，每一页显示5条数据
		PageHelper.startPage(pn, 5);//后面紧跟的这个查询就是分页查询
		List<Emp> lemp=empService.getALlEmpInfo();
		//将查询的分页结果进行包装,其中PageInfo中包含了这个页面的所有信息，所以只需要将pageInfo交给页面接受就行了
		PageInfo page=new PageInfo(lemp,5);//5:表示每次只显示5页的导航菜单
		map.put("pageInfo",page );
		//我们有视图解析器所以返回的list，会自动给它添加前缀和后缀
		return "list";
		
	}
}
```
# 9.查询_使用spring的单元测试测试分页请求
* 1.创建一个单元测试类,	代码如下：
``` java
package com.test;
//@RunWith帮我们创建容器
//@ContextConfiguration指定创建容器时使用哪个配置文件
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "classpath:conf/spring.xml", "classpath:conf/spring-mvc.xml" })
@WebAppConfiguration
public class Test2 {
	// 传入spring-mvc的ioc;
	// 注：@Autowired只能装配IOC里面的,所以在上面添加了一个WebAppConfiguration注解，拿到web的ioc容器
	@Autowired
	WebApplicationContext context;
	// 虚拟单元测试请求，获取处理结果
	MockMvc mocMvc;
	// 每次使用之前都要初始化一次，所以添加一个before注解
	@Before
	public void initMockMvc() {
		// 只有先创建才能使用
		mocMvc = MockMvcBuilders.webAppContextSetup(context).build();// 这个mocMvc就能模拟我的mvc请求
	}

	@Test
	public void testPage() throws Exception {
		// 模拟请求拿到返回值
		MvcResult result = mocMvc.perform(MockMvcRequestBuilders.get("/emp").param("pn", "1")).andReturn();
		// 请求成功以后，请求域中会有pageInfo,那么我们就可以去取出进行验证
		MockHttpServletRequest request = result.getRequest();
		PageInfo pageInfo = (PageInfo) request.getAttribute("pageInfo");
		System.out.println("当前页码=" + pageInfo.getPageNum());
		System.out.println("总页码=" + pageInfo.getPages());
		System.out.println("总记录数=" + pageInfo.getTotal());
		System.out.println("在页面需要连续显示的页码=");
		int pageNu[] = pageInfo.getNavigatepageNums();
		for (int nu : pageNu) {
			System.out.print(nu + "  ");
		}
		// 获取员工数据
		List<Emp> leEmps = pageInfo.getList();
		for (Emp e : leEmps) {
			System.out.println(e.toString());
		}
	}
}
```
# 10.查询_搭建BootStrap分页页面以及路径解析
### 1.路径的问题：
* 1.web路径，不以/开始的相对路径，找资源，以当前文件为基准，特别容易出问题
* 2.web路径以/开始的相对路径，找资源，以服务器为基准（http://localhost:3306/weservice/）
	也就是说在找资源时要加上http://localhost:3306/weservice/，但是为了避免是写错误或者麻烦，我们可以使用这种方法来自动获取路径：
```
<%
	pageContext.setAttribute("App_Path", request.getContextPath());
	%>
```	
取值：${App_Path}/资源路径：     
比如我的要找/ssmProject/src/main/webapp/js/jquery_3.3.1.js文件，那么就可以直接写：${App_Path}/js/jquery_3.3.1.js
### 2.由于所有的操作都是对list.jsp的操作，所以直接给出源码：
list.jsp文件：
```jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="http://code.jquery.com/jquery-latest.js"></script>
</head>
<body>
	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1>SSM-CRUD</h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary">新增</button>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于显示表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<tr>
						<th>emp_id</th>
						<th>emp_name</th>
						<th>gender</th>
						<th>eamil</th>
						<th>dept_id</th>
						<th>操作</th>
					</tr>
					<tr>
						<td>emp_id</td>
						<td>emp_name</td>
						<td>gender</td>
						<td>eamil</td>
						<td>dept_id</td>
						<td>
							<button class="btn btn-primary btn-sm">
								<span class="glyphicon glyphicon-pencil " aria-hidden="true"></span>
								编辑
							</button>
							<button class="btn btn-danger btn-sm">
								<span class="glyphicon glyphicon-trash " aria-hidden="true"></span>
								删除
							</button>
						</td>
					</tr>
				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6">当前记录数:XXXX</div>
			<!-- 分页条-->
			<div class="col-md-6">
				<nav aria-label="Page navigation">
					<ul class="pagination">
					<li><a href="#">首页</a></li>
						<li><a href="#" aria-label="Previous"> <span
								aria-hidden="true">&laquo;</span>
						</a></li>
						<li><a href="#">1</a></li>
						<li><a href="#">2</a></li>
						<li><a href="#">3</a></li>
						<li><a href="#">4</a></li>
						<li><a href="#">5</a></li>
						<li><a href="#" aria-label="Next"> <span
								aria-hidden="true">&raquo;</span>
						</a></li>
						<li><a href="#">末页</a></li>
					</ul>
				</nav>
			</div>
		</div>
	</div>
</body>
</html>
```
# 11.查询_显示分页数据
### 1.由于表格的行数都是根据后台数据自动产生，所以我们要使用遍历：目前推荐c:foreach语句：
> 使用此语句，先引入核心标签库：<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
> 注：如果报错，就先在pom中引入jstl标签库
``` xml
<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>jstl</artifactId>
			<version>1.2</version>
		</dependency>
```			
目前就只有这一个版本，不要引用错了
### 2.话不多说直接看代码：
> 同样是list.jsp文件“
``` jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<%
	pageContext.setAttribute("App_Path", request.getContextPath());
%>
</head>
<body>
	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1><font style="font-family: STXingkai">致一科技@<span style="font-family: STXingkai;color: graytext;">Zhiyi Technology</span></font></h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary">新增</button>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于存放表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<tr>
						<th>emp_id</th>
						<th>emp_name</th>
						<th>gender</th>
						<th>eamil</th>
						<th>dept_id</th>
						<th>操作</th>
					</tr>
					<c:forEach items="${pageInfo.list }" var="emp">
						<tr>
							<td>${emp.emp_id}</td>
							<td>${emp.emp_name}</td>
							<td>${emp.gender}</td>
							<td>${emp.eamil}</td>
							<td>${emp.dept_id}</td>
							<td>
								<button class="btn btn-primary btn-sm">
									<span class="glyphicon glyphicon-pencil " aria-hidden="true"></span>
									编辑
								</button>
								<button class="btn btn-danger btn-sm">
									<span class="glyphicon glyphicon-trash " aria-hidden="true"></span>
									删除
								</button>
							</td>
						</tr>
					</c:forEach>
				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6">当前第${pageInfo.pageNum}页
				,总共${pageInfo.pages}页,共${pageInfo.total}条记录</div>
			<!-- 分页条-->
			<div class="col-md-6">
				<nav aria-label="Page navigation">
					<ul class="pagination">
						<li><a href="${App_Path }/emp?pn=1">首页</a></li>
						<c:if test="${pageInfo.hasPreviousPage }">
						<li><a href="${App_Path }/emp?pn=${pageInfo.pageNum-1}" aria-label="Previous"> <span
								aria-hidden="true">&laquo;</span>
						</a></li>
						</c:if>
						<c:forEach items="${pageInfo.navigatepageNums }" var="num">
							<c:if test="${num==pageInfo.pageNum}">
								<li class="active"><a href="${App_Path }/emp?pn=${num}">${num}</a></li>
							</c:if>
							<c:if test="${num!=pageInfo.pageNum}">
								<li><a href="${App_Path }/emp?pn=${num}">${num}</a></li>
							</c:if>
						</c:forEach>
						<c:if test="${pageInfo.isHasNextPage() }">
							<li><a href="${App_Path }/emp?pn=${pageInfo.pageNum+1}" aria-label="Next"> <span
								aria-hidden="true">&raquo;</span>
						</a></li>
						</c:if>
						<li><a href="${App_Path }/emp?pn=${pageInfo.pages}">末页</a></li>
					</ul>
				</nav>
			</div>
		</div>
	</div>
</body>
</html>
```
# 12.查询_返回分页json数据
* 1.由于上面的方式只适用于客户端浏览器的交互，所以将返回的数据封装成json，前台进行接收，并进行解析就可以了
>具体流程：index.jsp发送json请求进行员工分页的数据查询->服务器将查出的数据以json字符串的形式返回浏览器——>浏览器收到js字符串，使用js进行解析
* 2.为了方便放回json，所以重新写一个方法直接返回pageInfo,要返回json必须添加一个注解@ResponseBody,但是要返回jason,就先导入jackson的包
> maven下：搜索jackson->jackson DataBind->选择你需要的版本
* 3.导入完成之后，在原来EmpConntroller层中添加一个新的方法，直接返回pageInfo对象：
> 为了让浏览器知道查询或者修改等成功与否，需要添加一个状态类来显示状态信息,在po里新创建一个msg对象，通用的返回类
``` java
public class Msg {
	private Integer code;//状态码（规定100：成功，200：失败）
	private String msg;//提示信息
	private Map<String, Object> extend=new HashMap<String, Object>();//用户要返回给浏览器的数据
	public Msg() {}
	public Integer getCode() {
		return code;
	}
	public void setCode(Integer code) {
		this.code = code;
	}
	public String getMsg() {
		return msg;
	}
	public void setMsg(String msg) {
		this.msg = msg;
	}
	public Map<String, Object> getExtend() {
		return extend;
	}
	public void setExtend(Map<String, Object> extend) {
		this.extend = extend;
	}
	
	public static Msg success() {
		Msg result=new Msg();
		result.setCode(100);
		result.setMsg("deal success");
		return result;
		
	}
	public static Msg fail() {
		Msg result=new Msg();
		result.setCode(200);
		result.setMsg("deal failure");
		return result;
		
	}
}
```
* 4.EmpController中修改的内容：
``` java
@Controller
public class EmpController {
	@Autowired
	EmpService empService;
	@ResponseBody
	@RequestMapping("/emp")
	public Msg getEmps(@RequestParam(value="pn",defaultValue="1" ) Integer pn) {
		//为了方便快速查询，所以引入PageHelper分页查询
				//表示从第pn查，每一页显示5条数据
				PageHelper.startPage(pn, 5);//后面紧跟的这个查询就是分页查询
				List<Emp> lemp=empService.getALlEmpInfo();
				//将查询的分页结果进行包装,其中PageInfo中包含了这个页面的所有信息，所以只需要将pageInfo交给页面接受就行了
				PageInfo page=new PageInfo(lemp,5);//5:表示每次只显示5页的导航菜单
				return Msg.success().add("pageInfo",page );//返回的不仅有状态消息，其中由于add方法，也将
				
		
	}
}
```
# 13.查询_构建员工列表
### 1.重新改造Index页面，让它发出ajax请求：
> 代码详情如下：
``` jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<%
	pageContext.setAttribute("App_Path", request.getContextPath());
%>
</head>
<body>
	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1>
					<font style="font-family: STXingkai">致一科技@<span
						style="font-family: STXingkai; color: graytext;">Zhiyi
							Technology</span></font>
				</h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary">新增</button>
				<span>  </span>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于存放表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<thead>
						<tr>
							<th>emp_id</th>
							<th>emp_name</th>
							<th>gender</th>
							<th>eamil</th>
							<th>dept_id</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>

					</tbody>

				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6">当前第页 ,总共页,共条记录</div>
			<!-- 分页条-->
			<div class="col-md-6"></div>
		</div>
	</div>
	<script type="text/javascript">
		//1.页面加载完成之后直接发送一个ajax请求，来获取分页数据：
		$(function() {
			$.ajax({
				url : "${App_Path}/emp",
				data : "pn=1",
				type : "get",
				success : function(data) {
					//获取成功之后要做的第一件事情就是：解析并显示员工数据
					showEmpMesage(data);
					//获取成功之后要做的第二件事情就是：解析并显示分页数据
				}
			});
		});
		function showEmpMesage(data) {
			//此处的写法应该根据浏览器显示的数据进行编写
			var emp = data.extend.pageInfo.list;
			$.each(emp, function(index, item) {
				$("tbody").append("<tr id='tr"+index+"'></tr>");
				$("#tr"+index).append("<td>"+item.emp_id+"</td>");
				$("#tr"+index).append("<td>"+item.emp_name+"</td>");
				$("#tr"+index).append("<td>"+item.gender+"</td>");
				$("#tr"+index).append("<td>"+item.eamil+"</td>");
				$("#tr"+index).append("<td>"+item.dept_id+"</td>");
				$("#tr"+index).append("<td id='bu"+index+"'></td>");
				$("#bu"+index).append("<button class='btn btn-primary btn-sm'><span class='glyphicon glyphicon-pencil ' aria-hidden='true'></span>编辑</button>");
				$("#bu"+index).append("  ");

				$("#bu"+index).append("<button class='btn btn-danger btn-sm'><span class='glyphicon glyphicon-trash ' aria-hidden='true'></span>删除</button>");

			});
		}
	</script>
</body>
</html>
```
# 14.查询_构建分页条
* 1.在第十三步中我们已经动态创建好了员工信息列表，接下来就是创建分页导航条：
> 对应的代码如下：
```jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<%
	pageContext.setAttribute("App_Path", request.getContextPath());
%>
</head>
<body>
	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1>
					<font style="font-family: STXingkai">致一科技@<span
						style="font-family: STXingkai; color: graytext;">Zhiyi
							Technology</span></font>
				</h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary">新增</button>
				<span> </span>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于存放表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<thead>
						<tr>
							<th>emp_id</th>
							<th>emp_name</th>
							<th>gender</th>
							<th>eamil</th>
							<th>dept_id</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>

					</tbody>

				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6" id="PageInfo"></div>
			<!-- 分页导航条-->
			<div class="col-md-6" id="PageNav"></div>
		</div>
	</div>
	<script type="text/javascript">
		//1.页面加载完成之后直接发送一个ajax请求，来获取分页数据：
		$(function() {
			$.ajax({
				url : "${App_Path}/emp",
				data : "pn=2",
				type : "get",
				success : function(data) {
					//获取成功之后要做的第一件事情就是：解析并显示员工数据
					showEmpMesage(data);
					//获取成功之后要做的第二件事情就是：解析并显示分页信息
					showPageInfo(data);
					//获取成功之后要做的第三件事情就是：解析并显示分页条
					showPageNav(data)
				}
			});
		});
		//解析显示员工信息
		function showEmpMesage(data) {
			//此处的写法应该根据浏览器显示的数据进行编写
			var emp = data.extend.pageInfo.list;
			$.each(emp, function(index, item) {
				$("tbody").append("<tr id='tr"+index+"'></tr>");
				$("#tr"+index).append("<td>"+item.emp_id+"</td>");
				$("#tr"+index).append("<td>"+item.emp_name+"</td>");
				$("#tr"+index).append("<td>"+item.gender+"</td>");
				$("#tr"+index).append("<td>"+item.eamil+"</td>");
				$("#tr"+index).append("<td>"+item.dept_id+"</td>");
				$("#tr"+index).append("<td id='bu"+index+"'></td>");
				$("#bu"+index).append("<button class='btn btn-primary btn-sm'><span class='glyphicon glyphicon-pencil ' aria-hidden='true'></span>编辑</button>");
				$("#bu"+index).append("  ");

				$("#bu"+index).append("<button class='btn btn-danger btn-sm'><span class='glyphicon glyphicon-trash ' aria-hidden='true'></span>删除</button>");

			});
		}
		//解析显示分页信息
		function showPageInfo(data) {
			 $("#PageInfo").append("当前第"+data.extend.pageInfo.pageNum+"页 ,总共"+data.extend.pageInfo.pages+"页,共"+data.extend.pageInfo.total+"条记录");
			
		}
		//解析显示分页条,并且能够可以点击下一页并跳转到对应的页面
		function showPageNav(data) {
			 $("#PageNav").append("<nav aria-label='Page navigation'><ul class='pagination'></ul></nav>");
			 $(".pagination").append("<li><a href='${App_Path }/emp?pn=1'>首页</a></li>");
			if(data.extend.pageInfo.hasPreviousPage){
			 $(".pagination").append("<li><a href='${App_Path }/emp?pn=${pageInfo.pageNum-1}' aria-label='Previous'> <span aria-hidden='true'>&laquo;</span></a></li>");
			}
			$.each(data.extend.pageInfo.navigatepageNums,function(index,item){
				if(item==data.extend.pageInfo.pageNum){
					$(".pagination").append("<li class='active'><a href='${App_Path }/emp?pn=${num}'>"+item+"</a></li>");
				}
				if(item!=data.extend.pageInfo.pageNum){
					$(".pagination").append("<li><a href='${App_Path }/emp?pn=${num}'>"+item+"</a></li>");
				}
			});
			if(data.extend.pageInfo.hasNextPage){
				$(".pagination").append("<li><a href='${App_Path }/emp?pn=${pageInfo.pageNum+1}' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");

			}
			$(".pagination").append("<li><a href='${App_Path }/emp?pn=${pageInfo.pages}'>末页</a></li>");

		}
	</script>
</body>
</html>
```
# 15.查询_优化完整分页条
* 1.在上一步骤，基本流程已经走完，但是点击页面跳转问题并未解决，接下来进行解决；
>代码如下：	
``` jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<%
	pageContext.setAttribute("App_Path", request.getContextPath());
%>
</head>
<body>
	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1>
					<font style="font-family: STXingkai">致一科技@<span
						style="font-family: STXingkai; color: graytext;">Zhiyi
							Technology</span></font>
				</h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary">新增</button>
				<span> </span>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于存放表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<thead>
						<tr>
							<th>emp_id</th>
							<th>emp_name</th>
							<th>gender</th>
							<th>eamil</th>
							<th>dept_id</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>

					</tbody>

				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6" id="PageInfo"></div>
			<!-- 分页导航条-->
			<div class="col-md-6" id="PageNav"></div>
		</div>
	</div>
	<script type="text/javascript">
		//1.页面加载完成之后直接发送一个ajax请求，来获取分页数据：
		$(function() {
			//默认跳转到首页
			toPage(2);
		});
		//用于跳转页面
		function toPage(pn){
			$.ajax({
				url : "${App_Path}/emp",
				data : "pn="+pn,
				type : "get",
				success : function(data) {
					//获取成功之后要做的第一件事情就是：解析并显示员工数据
					showEmpMesage(data);
					//获取成功之后要做的第二件事情就是：解析并显示分页信息
					showPageInfo(data);
					//获取成功之后要做的第三件事情就是：解析并显示分页条
					showPageNav(data);
				}
			});
		}
		//解析显示员工信息
		function showEmpMesage(data) {
			//每一次构建之前先把数据清空
			$("tbody").empty();
			//此处的写法应该根据浏览器显示的数据进行编写
			var emp = data.extend.pageInfo.list;
			$.each(emp, function(index, item) {
				$("tbody").append("<tr id='tr"+index+"'></tr>");
				$("#tr"+index).append("<td>"+item.emp_id+"</td>");
				$("#tr"+index).append("<td>"+item.emp_name+"</td>");
				$("#tr"+index).append("<td>"+item.gender+"</td>");
				$("#tr"+index).append("<td>"+item.eamil+"</td>");
				$("#tr"+index).append("<td>"+item.dept_id+"</td>");
				$("#tr"+index).append("<td id='bu"+index+"'></td>");
				$("#bu"+index).append("<button class='btn btn-primary btn-sm'><span class='glyphicon glyphicon-pencil ' aria-hidden='true'></span>编辑</button>");
				$("#bu"+index).append("  ");

				$("#bu"+index).append("<button class='btn btn-danger btn-sm'><span class='glyphicon glyphicon-trash ' aria-hidden='true'></span>删除</button>");

			});
		}
		
		//解析显示分页信息
		function showPageInfo(data) {
			//每一次构建之前先把数据清空
			$("#PageInfo").empty();
			 $("#PageInfo").append("当前第"+data.extend.pageInfo.pageNum+"页 ,总共"+data.extend.pageInfo.pages+"页,共"+data.extend.pageInfo.total+"条记录");
			
		}
		//解析显示分页条,并且能够可以点击下一页并跳转到对应的页面
		function showPageNav(data) {
			//每一次构建之前先把数据清空
			$("#PageNav").empty();
			 $("#PageNav").append("<nav aria-label='Page navigation'><ul class='pagination'></ul></nav>");
			 if(data.extend.pageInfo.pageNum>1){
				 $(".pagination").append("<li onclick='toPage("+1+")'><a href='#'>首页</a></li>");
			 }
			//上一页的值
			var prevoiuePage=data.extend.pageInfo.pageNum-1;
			if(data.extend.pageInfo.hasPreviousPage){
			 $(".pagination").append("<li onclick='toPage("+prevoiuePage+")'><a href='#' aria-label='Previous'> <span aria-hidden='true'>&laquo;</span></a></li>");
			}
			$.each(data.extend.pageInfo.navigatepageNums,function(index,item){
				if(item==data.extend.pageInfo.pageNum){
					$(".pagination").append("<li class='active '><a href='#'>"+item+"</a></li>");
				}
				if(item!=data.extend.pageInfo.pageNum){
					$(".pagination").append("<li onclick='toPage("+item+")'><a href='#'>"+item+"</a></li>");
				}
			});
			//下一页的值
			var nextPage=data.extend.pageInfo.pageNum+1;
			if(data.extend.pageInfo.hasNextPage){
				$(".pagination").append("<li onclick='toPage("+nextPage+")'><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");
				//末页的值
				var lastPage=data.extend.pageInfo.pages;
				$(".pagination").append("<li onclick='toPage("+lastPage+")'><a href='#'>末页</a></li>");
			}
			

		}
	</script>
</body>
</html>
```
# 16.新增_创建员工——新增模态框
### 1. 这个模态框是引用bootStrap中的javaScript组件中模态框的案例
> 具体代码详情如下：
``` jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>

<%
	pageContext.setAttribute("App_Path", request.getContextPath());
%>
</head>
<body>
	<!-- 员工添加的模态框 -->
	<div class="modal fade" id="empAddModal" tabindex="-1" role="dialog"
		aria-labelledby="myModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal"
						aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
					<h4 class="modal-title" id="myModalLabel">新增员工信息</h4>
				</div>
				<div class="modal-body">
					<form class="form-horizontal">
						<div class="form-group">
							<label for="inputName" class="col-sm-2 control-label">emp_Name</label>
							<div class="col-sm-10">
								<input type="text" class="form-control" id="inputName"
									placeholder="姓名">
							</div>
						</div>

						<div class="form-group">
							<label for="inputGender" class="col-sm-2 control-label">gender</label>
							<div class="col-sm-10">
								<label class="radio-inline"> <input type="radio"
									name="inlineRadioOptions" id="genderMan" value="男" checked="checked"> 男
								</label> <label class="radio-inline"> <input type="radio"
									name="inlineRadioOptions" id="genderGirl" value="女"> 女
								</label> <label class="radio-inline"> <input type="radio"
									name="inlineRadioOptions" id="genderOthers" value="女">
									女
								</label>
							</div>
						</div>

						<div class="form-group">
							<label for="inputEmail" class="col-sm-2 control-label">Email</label>
							<div class="col-sm-10">
								<input type="email" class="form-control" id="inputEmail"
									placeholder="Email@gmail.com">
							</div>
						</div>
						<div class="form-group">
							<label for="inputDeptName" class="col-sm-2 control-label">DeptName</label>
							<div class="col-sm-4">
							<select class="form-control" id="inputDeptName">
								
							</select>
							</div>
							

						</div>
					</form>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-default" data-dismiss="modal" id="Close">Close</button>
					<button type="button" class="btn btn-primary" id="Save">Save changes</button>
				</div>
			</div>
		</div>
	</div>


	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1>
					<font style="font-family: STXingkai">致一科技@<span
						style="font-family: STXingkai; color: graytext;">Zhiyi
							Technology</span></font>
				</h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary" id="empAddBtn" onclick="addEmp()">新增</button>
				<span> </span>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于存放表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<thead>
						<tr>
							<th>emp_id</th>
							<th>emp_name</th>
							<th>gender</th>
							<th>eamil</th>
							<th>dept_id</th>
							<th>dept_Name</th>

							<th>操作</th>
						</tr>
					</thead>
					<tbody>

					</tbody>

				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6" id="PageInfo"></div>
			<!-- 分页导航条-->
			<div class="col-md-6" id="PageNav"></div>
		</div>
	</div>
	<script type="text/javascript">
		//1.页面加载完成之后直接发送一个ajax请求，来获取分页数据：
		$(function() {
			//默认跳转到首页
			toPage(2);
		});
		//用于跳转页面
		function toPage(pn) {
			$.ajax({
				url : "${App_Path}/emp",
				data : "pn=" + pn,
				type : "get",
				success : function(data) {
					//获取成功之后要做的第一件事情就是：解析并显示员工数据
					showEmpMesage(data);
					//获取成功之后要做的第二件事情就是：解析并显示分页信息
					showPageInfo(data);
					//获取成功之后要做的第三件事情就是：解析并显示分页条
					showPageNav(data);
				}
			});
		}
		//解析显示员工信息
		function showEmpMesage(data) {
			//每一次构建之前先把数据清空
			$("tbody").empty();
			//此处的写法应该根据浏览器显示的数据进行编写
			var emp = data.extend.pageInfo.list;
			$
					.each(
							emp,
							function(index, item) {
								$("tbody").append("<tr id='tr"+index+"'></tr>");
								$("#tr" + index).append(
										"<td>" + item.emp_id + "</td>");
								$("#tr" + index).append(
										"<td>" + item.emp_name + "</td>");
								$("#tr" + index).append(
										"<td>" + item.gender + "</td>");
								$("#tr" + index).append(
										"<td>" + item.eamil + "</td>");
								$("#tr" + index).append(
										"<td>" + item.dept_id + "</td>");
								$("#tr" + index).append(
										"<td>" + item.dept_name + "</td>");
								$("#tr" + index).append(
										"<td id='bu"+index+"'></td>");
								$("#bu" + index)
										.append(
												"<button class='btn btn-primary btn-sm'><span class='glyphicon glyphicon-pencil ' aria-hidden='true'></span>编辑</button>");
								$("#bu" + index).append("  ");

								$("#bu" + index)
										.append(
												"<button class='btn btn-danger btn-sm'><span class='glyphicon glyphicon-trash ' aria-hidden='true'></span>删除</button>");

							});
		}

		//解析显示分页信息
		function showPageInfo(data) {
			//每一次构建之前先把数据清空
			$("#PageInfo").empty();
			$("#PageInfo").append(
					"当前第" + data.extend.pageInfo.pageNum + "页 ,总共"
							+ data.extend.pageInfo.pages + "页,共"
							+ data.extend.pageInfo.total + "条记录");

		}
		//解析显示分页条,并且能够可以点击下一页并跳转到对应的页面
		function showPageNav(data) {
			//每一次构建之前先把数据清空
			$("#PageNav").empty();
			$("#PageNav")
					.append(
							"<nav aria-label='Page navigation'><ul class='pagination'></ul></nav>");
			if (data.extend.pageInfo.pageNum > 1) {
				$(".pagination").append(
						"<li onclick='toPage(" + 1
								+ ")'><a href='#'>首页</a></li>");
			}
			//上一页的值
			var prevoiuePage = data.extend.pageInfo.pageNum - 1;
			if (data.extend.pageInfo.hasPreviousPage) {
				$(".pagination")
						.append(
								"<li onclick='toPage("
										+ prevoiuePage
										+ ")'><a href='#' aria-label='Previous'> <span aria-hidden='true'>&laquo;</span></a></li>");
			}
			$.each(data.extend.pageInfo.navigatepageNums,
					function(index, item) {
						if (item == data.extend.pageInfo.pageNum) {
							$(".pagination").append(
									"<li class='active '><a href='#'>" + item
											+ "</a></li>");
						}
						if (item != data.extend.pageInfo.pageNum) {
							$(".pagination").append(
									"<li onclick='toPage(" + item
											+ ")'><a href='#'>" + item
											+ "</a></li>");
						}
					});
			//下一页的值
			var nextPage = data.extend.pageInfo.pageNum + 1;
			if (data.extend.pageInfo.hasNextPage) {
				$(".pagination")
						.append(
								"<li onclick='toPage("
										+ nextPage
										+ ")'><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");
				//末页的值
				var lastPage = data.extend.pageInfo.pages;
				$(".pagination").append(
						"<li onclick='toPage(" + lastPage
								+ ")'><a href='#'>末页</a></li>");
			}

		}
		//用于弹出新增员工的模态框的点击事件
		function addEmp() {
			$('#empAddModal').modal({
				backdrop : "static"
			})
		}
	</script>
</body>
</html>
```	
# 17.新增_ajax显示部门信息
### 1.每一次点击应该新增一次ajax请求来获取部门信息到添加的下拉框中
### 2.在编写此功能之前要先有一个方法专门返回部门信息数据，故在Controller层添加一个控制器DepController：
``` java
@Controller
public class DepController {
	@Autowired
	DepService depService;
	@ResponseBody
	@RequestMapping("/depts")
	public Msg getDepts() {
		List<Dept> lDepts=depService.getALlDeptInfo();
		
		return Msg.success().add("depts", lDepts);
	}
}
```
但是缺少相应的服务层，以及dao层   
对应的service：
```java 
	public interface DepService {
	public List<Dept> getALlDeptInfo();
}
```
对用的serviceImpl层：
```java
@Service
public class DeptServiceImpl implements DepService {
	// service依赖于Dao
	@Autowired
	DeptMapper deptMapper;
	public DeptMapper getDeptMapper() {
		return deptMapper;
	}
	public void setDeptMapper(DeptMapper deptMapper) {
		this.deptMapper = deptMapper;
	}
	@Override
	public List<Dept> getALlDeptInfo() {
		// TODO Auto-generated method stub
		return deptMapper.getDeptInfo();
	}
}
```
对应的mapper文件：
```java
public interface DeptMapper {
	public void insertByDept(Dept dept);
	public List<Dept> getDeptInfo();
}
```
对应的mapper,xml文件：（Dept.xml）
``` xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
 PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!-- 先引入对应的扫描文件 -->
<mapper namespace="com.mapper.DeptMapper">
	<!-- 查询列表所有内容 -->
	<select id="getDeptInfo" resultMap="getDeptInfoReMap">
		select * from tbl_dept
	</select>
	<resultMap type="com.po.Dept" id="getDeptInfoReMap">
		<id column="dept_id" property="dept_id" />
		<result column="dept_name" property="dept_name" />
	</resultMap>
	<insert id="insertByDept" parameterType="com.po.Dept">
		insert into tbl_dept (dept_name)
		values(#{dept_name})

	</insert>
</mapper>
```
index.jsp页面：
```jsp
<%@ page language="java" contentType="text/html; charset=utf-8"
	pageEncoding="utf-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>员工列表</title>
<link rel="stylesheet"
	href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script
	src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>

<%
	pageContext.setAttribute("App_Path", request.getContextPath());
%>
</head>
<body>
	<!-- 员工添加的模态框 -->
	<div class="modal fade" id="empAddModal" tabindex="-1" role="dialog"
		aria-labelledby="myModalLabel">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal"
						aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
					<h4 class="modal-title" id="myModalLabel">新增员工信息</h4>
				</div>
				<div class="modal-body">
					<form class="form-horizontal">
						<div class="form-group">
							<label for="inputName" class="col-sm-2 control-label">emp_Name</label>
							<div class="col-sm-10">
								<input type="text" class="form-control" id="inputName"
									placeholder="姓名">
							</div>
						</div>

						<div class="form-group">
							<label for="inputGender" class="col-sm-2 control-label">gender</label>
							<div class="col-sm-10">
								<label class="radio-inline"> <input type="radio"
									name="inlineRadioOptions" id="genderMan" value="男"
									checked="checked"> 男
								</label> <label class="radio-inline"> <input type="radio"
									name="inlineRadioOptions" id="genderGirl" value="女"> 女
								</label> <label class="radio-inline"> <input type="radio"
									name="inlineRadioOptions" id="genderOthers" value="女">
									女
								</label>
							</div>
						</div>

						<div class="form-group">
							<label for="inputEmail" class="col-sm-2 control-label">Email</label>
							<div class="col-sm-10">
								<input type="email" class="form-control" id="inputEmail"
									placeholder="Email@gmail.com">
							</div>
						</div>
						<div class="form-group">
							<label for="inputDeptName" class="col-sm-2 control-label">DeptName</label>
							<div class="col-sm-4">
								<select class="form-control" id="inputDeptName">

								</select>
							</div>


						</div>
					</form>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-default" data-dismiss="modal"
						id="Close">Close</button>
					<button type="button" class="btn btn-primary" id="Save">Save
						changes</button>
				</div>
			</div>
		</div>
	</div>


	<div class="container">
		<!-- 用于显示标题栏 -->
		<div class="row">
			<div class="col-md-12">
				<h1>
					<font style="font-family: STXingkai">致一科技@<span
						style="font-family: STXingkai; color: graytext;">Zhiyi
							Technology</span></font>
				</h1>
			</div>
		</div>
		<!-- 用于放按钮 -->
		<div class="row">
			<div class="col-md-4 col-md-offset-8">
				<button class="btn btn-primary" id="empAddBtn" onclick="addEmp()">新增</button>
				<span> </span>
				<button class="btn btn-danger">删除</button>
			</div>
		</div>
		<!-- 用于存放表格数据 -->
		<div class="row">
			<div class="col-md-12">
				<table class="table table-striped table-bordered table-hover">
					<thead>
						<tr>
							<th>emp_id</th>
							<th>emp_name</th>
							<th>gender</th>
							<th>eamil</th>
							<th>dept_id</th>
							<th>dept_Name</th>

							<th>操作</th>
						</tr>
					</thead>
					<tbody>

					</tbody>

				</table>
			</div>
		</div>
		<!-- 用于显示分页信息 -->
		<div class="row">
			<!-- 分页文字信息 -->
			<div class="col-md-6" id="PageInfo"></div>
			<!-- 分页导航条-->
			<div class="col-md-6" id="PageNav"></div>
		</div>
	</div>
	<script type="text/javascript">
		//1.页面加载完成之后直接发送一个ajax请求，来获取分页数据：
		$(function() {
			//默认跳转到首页
			toPage(2);
		});
		//用于跳转页面
		function toPage(pn) {
			$.ajax({
				url : "${App_Path}/emp",
				data : "pn=" + pn,
				type : "get",
				success : function(data) {
					//获取成功之后要做的第一件事情就是：解析并显示员工数据
					showEmpMesage(data);
					//获取成功之后要做的第二件事情就是：解析并显示分页信息
					showPageInfo(data);
					//获取成功之后要做的第三件事情就是：解析并显示分页条
					showPageNav(data);
				}
			});
		}
		//解析显示员工信息
		function showEmpMesage(data) {
			//每一次构建之前先把数据清空
			$("tbody").empty();
			//此处的写法应该根据浏览器显示的数据进行编写
			var emp = data.extend.pageInfo.list;
			$
					.each(
							emp,
							function(index, item) {
								$("tbody").append("<tr id='tr"+index+"'></tr>");
								$("#tr" + index).append(
										"<td>" + item.emp_id + "</td>");
								$("#tr" + index).append(
										"<td>" + item.emp_name + "</td>");
								$("#tr" + index).append(
										"<td>" + item.gender + "</td>");
								$("#tr" + index).append(
										"<td>" + item.eamil + "</td>");
								$("#tr" + index).append(
										"<td>" + item.dept_id + "</td>");
								$("#tr" + index).append(
										"<td>" + item.dept_name + "</td>");
								$("#tr" + index).append(
										"<td id='bu"+index+"'></td>");
								$("#bu" + index)
										.append(
												"<button class='btn btn-primary btn-sm'><span class='glyphicon glyphicon-pencil ' aria-hidden='true'></span>编辑</button>");
								$("#bu" + index).append("  ");

								$("#bu" + index)
										.append(
												"<button class='btn btn-danger btn-sm'><span class='glyphicon glyphicon-trash ' aria-hidden='true'></span>删除</button>");

							});
		}

		//解析显示分页信息
		function showPageInfo(data) {
			//每一次构建之前先把数据清空
			$("#PageInfo").empty();
			$("#PageInfo").append(
					"当前第" + data.extend.pageInfo.pageNum + "页 ,总共"
							+ data.extend.pageInfo.pages + "页,共"
							+ data.extend.pageInfo.total + "条记录");

		}
		//解析显示分页条,并且能够可以点击下一页并跳转到对应的页面
		function showPageNav(data) {
			//每一次构建之前先把数据清空
			$("#PageNav").empty();
			$("#PageNav")
					.append(
							"<nav aria-label='Page navigation'><ul class='pagination'></ul></nav>");
			if (data.extend.pageInfo.pageNum > 1) {
				$(".pagination").append(
						"<li onclick='toPage(" + 1
								+ ")'><a href='#'>首页</a></li>");
			}
			//上一页的值
			var prevoiuePage = data.extend.pageInfo.pageNum - 1;
			if (data.extend.pageInfo.hasPreviousPage) {
				$(".pagination")
						.append(
								"<li onclick='toPage("
										+ prevoiuePage
										+ ")'><a href='#' aria-label='Previous'> <span aria-hidden='true'>&laquo;</span></a></li>");
			}
			$.each(data.extend.pageInfo.navigatepageNums,
					function(index, item) {
						if (item == data.extend.pageInfo.pageNum) {
							$(".pagination").append(
									"<li class='active '><a href='#'>" + item
											+ "</a></li>");
						}
						if (item != data.extend.pageInfo.pageNum) {
							$(".pagination").append(
									"<li onclick='toPage(" + item
											+ ")'><a href='#'>" + item
											+ "</a></li>");
						}
					});
			//下一页的值
			var nextPage = data.extend.pageInfo.pageNum + 1;
			if (data.extend.pageInfo.hasNextPage) {
				$(".pagination")
						.append(
								"<li onclick='toPage("
										+ nextPage
										+ ")'><a href='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>");
				//末页的值
				var lastPage = data.extend.pageInfo.pages;
				$(".pagination").append(
						"<li onclick='toPage(" + lastPage
								+ ")'><a href='#'>末页</a></li>");
			}

		}
		//用于弹出新增员工的模态框的点击事件
		function addEmp() {
			//在模态框弹出之前，先发送ajax请求查出部门信息，添加的下拉框中
			addDeptInfoToList();

			//此处弹出模态框
			$('#empAddModal').modal({
				backdrop : "static"
			})
		}
		//用于送ajax请求查出部门信息，添加的下拉框中
		function addDeptInfoToList() {
			$.ajax({
				url : "http://localhost:8080/wxservice/depts",
				type : "GET",
				success : function(data) {
					//接下来就是添加部门信息到下拉列表 
					$.each(data.extend.depts, function(index,item) {
						$("#inputDeptName").append("<option>" + item.dept_name + "</option>");
					});

				}
			});
		}
	</script>
</body>
</html>
```
# 18.新增_新增的基本完成
### 1.为了规范开发，固定：
Url发出：
```java
/emp/{id} get  ：用于查询员工信息
			/emp/ Post  ：用于保存员工信息
			/emp/{id} put  ：用于修改员工信息
			/emp/{id} delete  ：用于删除员工信息
```			
中间遇到了很多问题，暂时还未解决，先暂时使用servlet提交的方式完成此任务；等解决之后在进行补充
# 19.新增_jquery的前端校验
* 1.这次的功能全部操作在index.jsp中，所以核心代码如下：
```jsp
	//用于给提交按钮添加事件,用于在提交时可以校验你所提交的数据
		$("#submit").click(function(){
		    //1.拿到校验的数据，使用正则表达式进行校验
			var emp_name=$("#inputName").val();
			var regName=/(^[a-zA-Z0-9_-]{1,16}$)|(^[\u2E80-\u9FFF]{2,5})/;
			if(!regName.test(emp_name)){
				alert("用户名输入a-z或者A-Z或者2-5位中文");
				return false;
			};
		})
```
# 20.新增_jquery的前端校验优化
### 1.alert提示太丑，我们可以给其输入框增加样式来完成提示
> 添加 .has-warning、.has-error 或 .has-success 类到这些控件的父元素即可
> 每次添加之前先清除之前的样式和内容     
核心代码：
``` jsp
//用于给提交按钮添加事件,用于在提交时可以校验你所提交的数据
		$("#submit").click(function(){
		    //1.拿到校验的数据，使用正则表达式进行校验
			var emp_name=$("#inputName").val();
			var regName=/(^[a-zA-Z0-9_-]{1,16}$)|(^[\u2E80-\u9FFF]{2,5})/;
			if(!regName.test(emp_name)){
				//alert("用户名输入a-z或者A-Z或者2-5位中文");
				//alert提示太丑，我们可以给其输入框增加样式来完成提示
				//添加 .has-warning、.has-error 或 .has-success 类到这些控件的父元素即可
				//每次添加之前先清除之前的样式和内容
					$("#inputName").parent().removeClass("has-error has-warning has-success");
					$("#helpSpanToInputName").text("");
				$("#inputName").parent().addClass("has-error");
				$("#helpSpanToInputName").text("用户名输入a-z或者A-Z或者2-5位中文");
				return false;
			}
			else{
				$("#inputName").parent().addClass("has-success");
			}
		})
```
# 21.新增_ajax校验用户名是否重复
* 1.首先要判断书写的用户名是否在数据库中已经存在
``` jsp
//用于给提交按钮添加事件,用于在提交时可以校验你所提交的数据
		$("#submit").click(function(){
		    //1.拿到校验的数据，使用正则表达式进行校验
			var emp_name=$("#inputName").val();
			var regName=/(^[a-zA-Z0-9_-]{1,16}$)|(^[\u2E80-\u9FFF]{2,5})/;
			var email = $("#inputEmail").val();
	        var regEmail = /^([a-zA-Z0-9_.-]+)@([da-z.-]+).([a-z.]{2,6})$/;
			if(!regName.test(emp_name)){
				//alert("用户名输入a-z或者A-Z或者2-5位中文");
				//alert提示太丑，我们可以给其输入框增加样式来完成提示
				//添加 .has-warning、.has-error 或 .has-success 类到这些控件的父元素即可
				//每次添加之前先清除之前的样式和内容
					$("#inputName").parent().removeClass("has-error has-warning has-success");
					$("#helpSpanToInputName").text("");
				$("#inputName").parent().addClass("has-error");
				$("#helpSpanToInputName").text("用户名输入a-z或者A-Z或者2-5位中文");
				return false;
			}
			else{
				$("#inputEmail").parent().addClass("has-success");
			}
			if(!regEmail.test(email)){
				//alert("用户名输入a-z或者A-Z或者2-5位中文");
				//alert提示太丑，我们可以给其输入框增加样式来完成提示
				//添加 .has-warning、.has-error 或 .has-success 类到这些控件的父元素即可
				//每次添加之前先清除之前的样式和内容
					$("#inputEmail").parent().removeClass("has-error has-warning has-success");
					$("#helpSpanToinputEmail").text("");
				$("#inputEmail").parent().addClass("has-error");
				$("#helpSpanToinputEmail").text("email格式不正确");
				return false;
			}
			else{
				$("#inputEmail").parent().addClass("has-success");
			}
			var ajaxValidate=$(this).attr("data-m");
			alert(ajaxValidate);
			if(ajaxValidate=='fail'){
				return false;
			}else{
				return true;
			}
		})
		
		//给员工姓名的输入框绑定事件来检测其内容是否发生改变
		$("#inputName").change(function(){
			//获取当前输入框中的值
			var emp_name=this.value;
		   //一旦改变就立刻发送ajax请求来判断用户名是否可用
		   $.ajax({
			   url:"http://localhost:8080/wxservice/checkUser",
			   data:"emp_name="+emp_name,
			   type:"POST",
			   success:function(data){
				   if(data.extend.result){
					 //每次添加之前先清除之前的样式和内容
					$("#inputName").parent().removeClass("has-error has-warning has-success");
					$("#helpSpanToInputName").text("");
					$("#inputName").parent().addClass("has-success");
					$("#helpSpanToInputName").text("用户名可用");
					$("#submit").attr("data-m","success");
				   }else{
					   //每次添加之前先清除之前的样式和内容
						$("#inputName").parent().removeClass("has-error has-warning has-success");
						$("#helpSpanToInputName").text("");
						$("#inputName").parent().addClass("has-error");
						$("#helpSpanToInputName").text("用户名已经注册");   
						//此处就是为了在提交时判断会否可以提交
						$("#submit").attr("data-m","fail");
				   }
			   }
		   });
		})
```	
* 2.在controllwer层中处理ajax请求：   
但是在编写controller曾之前首先要写好相对应的service以及serviceImpl,mapper,mapper.xml;   
先写mapper:
> 1.empMapper:
``` java
public interface EmpMapper {
	public List<Emp> checkUserAlreadyUseByUserName(String emp_name);
}
```
> 2.empMapper.xml：
```xml
<!-- 通过员工姓名查询员工信息 -->
	<select id="checkUserAlreadyUseByUserName" resultMap="getEmpInfoReMap" parameterType="String">
	select *
	 from tbl_emp
	 where emp_name=#{emp_name}
	</select>
	<resultMap type="com.po.Emp" id="getEmpInfoReMap">
		<result column="emp_id" property="emp_id" />
		<result column="emp_name" property="emp_name" />
		<result column="gender" property="gender" /> 
		<result column="eamil" property="eamil" />
		<result column="dept_id" property="dept_id" />
	</resultMap>
```		
> 3.service:
```java
public interface EmpService {
	public Boolean checkUser(String name);
}
```
> 4.serviceImpl:
```java
@Service
public class EmpServiceImpl implements EmpService {
	// service依赖于Dao
	@Autowired
	EmpMapper eMapper;
	@Autowired
	DeptMapper deptMapper;
	@Override
	public Boolean checkUser(String name) {
		// TODO Auto-generated method stub
		Boolean result=null;
		List<Emp> lemps=eMapper.checkUserAlreadyUseByUserName(name);
		if(lemps.size()>=1) {
			result=false;
		}else {
			result=true;
		}
		return result;
	}
}
```
> 5.controller:
``` java
@Controller
public class EmpController {
	@Autowired
	EmpService empService;
	//用于检验用户名是否可用
	@ResponseBody
	@RequestMapping("/checkUser")
	public Msg checkUse(@RequestParam(value="emp_name") String  emp_name) {
		Boolean result=empService.checkUser(emp_name);
		return Msg.success().add("result", result);
	
	}
}
```
注：以上都是代码片段，请注意！！！！！！！！！！！！！！！！！
# 22.新增_ajax校验用户名细节处理
1.由于时间太过仓促，先不进行优化
# 23.新增_JSR303校验
>1.此校验是后台校验,先导入Hibernate validator  jar包，maven仓库直接搜索Hibernate validator，点击进入Hibernate validator Engine Relocation	Artifact
# 24.新增分页插件的合理化
### 1.由于上面的pageHelper插件中，分页显示出现了一些问题，比如当总页码超过最后一页，同样会进行跳转的问题：
> 此时引入pageHelper中的一个属性：reasonable：   
> 分页合理化参数，默认值为false。当该参数设置为 true 时，pageNum<=0 时会查询第一页， pageNum>pages（超过总数时），会查询最后一页。
> 默认false 时，直接根据参数进行查询。
> 打开mybatis,xml文件，找到plugins下的 <plugin interceptor="com.github.pagehelper.PageInterceptor">
> 在里面新增property属性；
```java
<plugin interceptor="com.github.pagehelper.PageInterceptor">
	        <property name="reasonable" value="true"/>
	    </plugin>
```
# 25.修改的基本实现
* 1.首先在springMvc中配置一个拦截器来处理put以及delete请求，否则的话就请求不到
> 打开web.xml文件：
``` xml
新增过滤器：
			<!-- 用于处理put以及delete请求 -->
  <filter>
      <filter-name>HttpPutFormContentFilter</filter-name>
      <filter-class>org.springframework.web.filter.HttpPutFormContentFilter</filter-class>
  </filter>
  <filter-mapping>
      <filter-name>HttpPutFormContentFilter</filter-name>
      <url-pattern>/*</url-pattern>
  </filter-mapping>
```
2.具体代码参考index3.jsp
# 26.删除_删除单一员工
* 1.先创建mapper:
> public void deleteEmpById(Integer emp_id);
* 2.在创建对应的xml文件：
``` xml
<!-- 删除单个员工信息 -->
	<delete id="deleteEmpById" parameterType="Integer">
	 	delete from tbl_emp where emp_id=#{emp_id}
	 </delete>
```
* 3.创建service层：
> public void deleteEmpOnlyOne(Integer emp_id);
* 4.创建对应的serviceImpl：
``` java
	@Override
	public void deleteEmpOnlyOne(Integer emp_id) {
		// TODO Auto-generated method stub
		eMapper.deleteEmpById(emp_id);
	}
```
* 5.创建对应的controller
```
//用于删除单一员工
	//用于保存员工信息
		@ResponseBody
		@RequestMapping(value="/deleteEmp" ,method=RequestMethod.POST)
		public Msg deleteEmp(@RequestParam(value="emp_id") String emp_id) {
			Integer id=Integer.valueOf(emp_id);
			System.out.println("deleteEmp_emp_id="+id);
			
			empService.deleteEmpOnlyOne(id);
			return Msg.success();
		}
```
* 6.对应的index3.jsp文件：
```jsp
	//用于给动态产生的删除按钮添加点击事件
		$(document).on("click",".delete",function(){
			var emp_id=$(this).attr("data-delete");
			var emp_Name=$(this).attr("data-delete_Emp_Name")
			var re=confirm("确认要删除【"+emp_Name+"】这条用户的信息");
			if(!re){
				return false;
			}
			 $.ajax({
			      url: "${App_Path}/deleteEmp",
			      type: "POST",
			      data:"emp_id="+emp_id,
			      success: function (data) {
			    	  
			    	  alert("删除成功");
			    	  //关闭模态框
			    	  $('#empUpdateModal').modal("hide");
			    	  //跳转到当前页面
			    	 toPage(pageNumber);
			      }
			});
		});
```
# 27.完成全选/全不选的功能
1.index3.jsp:
``` jsp
//完成全选/全不选的功能
		$("#check_ALl").click(function(){
			//使用attr获取checked的值是undifined,所以定义原声的属性使用pop获取值
			//$(this).attr("checked");
			$(".check_item").prop("checked",$(this).prop("checked"));
		});
		$(document).on("click",".check_item",function(){
			//先判断当前选中的元素是否是5个
			var checkBoxNu_Checked=$(".check_item:checked").length;//此处用于获取选中的复选框的个数
			var checkBoxNu_Item=$(".check_item").length;//此处用于获取当前页面的复选框的个数
			
			if(checkBoxNu_Checked>=checkBoxNu_Item){
				$("#check_ALl").prop("checked",true);
			}else{
				$("#check_ALl").prop("checked",false);
			}
		});
```
创建的过程就不添加了，请参考index3.jsp
		
		
		
		
		
								