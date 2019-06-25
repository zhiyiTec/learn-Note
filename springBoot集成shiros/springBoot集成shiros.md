# 在使用 springBoot 集成 shiro 之前要先具备 shiro 的基础知识，我大概先给大家梳理一下:

> Authentication：身份认证/登录，验证用户是不是拥有相应的身份；

> Authorization：授权，即权限验证，验证某个已认证的用户是否拥有某个权限；即判断用户是否能做事情，常见的如：验证某个用户是否拥有某个角色。或者细粒度的验证某个用户对某个资源是否具有某个权限；

> Session Manager：会话管理，即用户登录后就是一次会话，在没有退出之前，它的所有信息都在会话中；会话可以是普通 JavaSE 环境的，也可以是如 Web 环境的；

> Cryptography：加密，保护数据的安全性，如密码加密存储到数据库，而不是明文存储；

> Web Support：Web 支持，可以非常容易的集成到 Web 环境；

> Caching：缓存，比如用户登录后，其用户信息、拥有的角色/权限不必每次去查，这样可以提高效率；

> Concurrency：shiro 支持多线程应用的并发验证，即如在一个线程中开启另一个线程，能把权限自动传播过去；

> Testing：提供测试支持；

> Run As：允许一个用户假装为另一个用户（如果他们允许）的身份进行访问；

> Remember Me：记住我，这个是非常常见的功能，即一次登录后，下次再来的话不用登录了。

```
记住一点，Shiro不会去维护用户、维护权限；这些需要我们自己去设计/提供；然后通过相应的接口注入给Shiro即可。
```

> Subject：主体，代表了当前“用户”，这个用户不一定是一个具体的人，与当前应用交互的任何东西都是 Subject，如网络爬虫，机器人等；即一个抽象概念；所有 Subject 都绑定到 SecurityManager，与 Subject 的所有交互都会委托给 SecurityManager；可以把 Subject 认为是一个门面；SecurityManager 才是实际的执行者；

> SecurityManager：安全管理器；即所有与安全有关的操作都会与 SecurityManager 交互；且它管理着所有 Subject；可以看出它是 Shiro 的核心，它负责与后边介绍的其他组件进行交互，如果学习过 SpringMVC，你可以把它看成 DispatcherServlet 前端控制器；

> Realm：域，Shiro 从从 Realm 获取安全数据（如用户、角色、权限），就是说 SecurityManager 要验证用户身份，那么它需要从 Realm 获取相应的用户进行比较以确定用户身份是否合法；也需要从 Realm 得到用户相应的角色/权限进行验证用户是否能进行操作；可以把 Realm 看成 DataSource，即安全数据源。也就是说对于我们而言，最简单的一个 Shiro 应用：

- 1、应用代码通过 Subject 来进行认证和授权，而 Subject 又委托给 SecurityManager；

- 2、我们需要给 Shiro 的 SecurityManager 注入 Realm，从而让 SecurityManager 能得到合法的用户及其权限进行判断。

> 从以上也可以看出，Shiro 不提供维护用户/权限，而是通过 Realm 让开发人员自己注入。

---

> Subject：主体，可以看到主体可以是任何可以与应用交互的“用户”；

> SecurityManager：相当于 SpringMVC 中的 DispatcherServlet 或者 Struts2 中的 FilterDispatcher；是 Shiro 的心脏；所有具体的交互都通过 SecurityManager 进行控制；它管理着所有 Subject、且负责进行认证和授权、及会话、缓存的管理。

> Authenticator：认证器，负责主体认证的，这是一个扩展点，如果用户觉得 Shiro 默认的不好，可以自定义实现；其需要认证策略（Authentication Strategy），即什么情况下算用户认证通过了；

> Authrizer：授权器，或者访问控制器，用来决定主体是否有权限进行相应的操作；即控制着用户能访问应用中的哪些功能；

> Realm：可以有 1 个或多个 Realm，可以认为是安全实体数据源，即用于获取安全实体的；可以是 JDBC 实现，也可以是 LDAP 实现，或者内存实现等等；由用户提供；注意：Shiro 不知道你的用户/权限存储在哪及以何种格式存储；所以我们一般在应用中都需要实现自己的 Realm；

> SessionManager：如果写过 Servlet 就应该知道 Session 的概念，Session 呢需要有人去管理它的生命周期，这个组件就是 SessionManager；而 Shiro 并不仅仅可以用在 Web 环境，也可以用在如普通的 JavaSE 环境、EJB 等环境；所有呢，Shiro 就抽象了一个自己的 Session 来管理主体与应用之间交互的数据；这样的话，比如我们在 Web 环境用，刚开始是一台 Web 服务器；接着又上了台 EJB 服务器；这时想把两台服务器的会话数据放到一个地方，这个时候就可以实现自己的分布式会话（如把数据放到 Memcached 服务器）；

> SessionDAO：DAO 大家都用过，数据访问对象，用于会话的 CRUD，比如我们想把 Session 保存到数据库，那么可以实现自己的 SessionDAO，通过如 JDBC 写到数据库；比如想把 Session 放到 Memcached 中，可以实现自己的 Memcached SessionDAO；另外 SessionDAO 中可以使用 Cache 进行缓存，以提高性能；

> CacheManager：缓存控制器，来管理如用户、角色、权限等的缓存的；因为这些数据基本上很少去改变，放到缓存中后可以提高访问的性能

> Cryptography：密码模块，Shiro 提高了一些常见的加密组件用于如密码加密/解密的。

以上就是 shiro 的大概，具体更多的 shiro 学习 [点击此处](https://jinnianshilongnian.iteye.com/blog/2049092)

# 2.接下来进入正式的 shiro 集成到 springBoot 中，下面先看一下引入的 maven 依赖:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.1.3.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.zhiyi</groupId>
    <artifactId>shiro</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>shiro</name>
    <description>Demo for Shiro Learn</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-starter-logging</artifactId>
                </exclusion>
            </exclusions>

        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>2.0.0</version>
        </dependency>

        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>

        </dependency>
        <!--集成shiro-->
        <!-- https://mvnrepository.com/artifact/org.apache.shiro/shiro-spring -->
        <dependency>
            <groupId>org.apache.shiro</groupId>
            <artifactId>shiro-spring</artifactId>
            <version>1.4.0</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.shiro/shiro-web -->
        <dependency>
            <groupId>org.apache.shiro</groupId>
            <artifactId>shiro-web</artifactId>
            <version>1.4.0</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.shiro/shiro-core -->
        <dependency>
            <groupId>org.apache.shiro</groupId>
            <artifactId>shiro-core</artifactId>
            <version>1.4.0</version>
        </dependency>

        <!--引入log4j-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-log4j</artifactId>
            <version>1.3.8.RELEASE</version>
        </dependency>
        <!-- MySQL 连接驱动依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.13</version>
        </dependency>

        <!-- druid -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.9</version>
        </dependency>
    <!--引入servlet-->
        <!-- https://mvnrepository.com/artifact/javax.servlet/javax.servlet-api -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>

<!--配置热部署-->

        <!--添加热部署-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <optional>true</optional>
            <scope>true</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>

            <plugin>
                <!--热部署配置-->
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <!--fork:如果没有该项配置,整个devtools不会起作用-->
                    <fork>true</fork>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>

```

## 2.1 编写自己定义规则，即编写自己的 realm

```java
package com.zhiyi.shiro.config;

import com.zhiyi.shiro.mapper.GetMapper;
import com.zhiyi.shiro.model.Shiro_User;
import com.zhiyi.shiro.model.Shiro_User_Role;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.LinkedList;
import java.util.List;

public class MyShiroRealm    extends AuthorizingRealm {
    private JdbcTemplate jdbcTemplate;
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    private GetMapper getMapper;

    @Override
    public String getName() {
        return "MyShiroRealm";
    }
    @Override
    public boolean supports(AuthenticationToken token) {
        //仅支持UsernamePasswordToken类型的Token
        return token instanceof UsernamePasswordToken;
    }
    /**
     * 用于获取登录成功后的角色、权限等信息
     * @param principals
     * @return
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principals) {
        //先通过用户名查询角色
        SimpleAuthorizationInfo info=new SimpleAuthorizationInfo();
        Shiro_User user=(Shiro_User) (principals.getPrimaryPrincipal());//获取当前与系统交互的对象
        List<String> roles=getMapper.getUserRolesByName(user.getUserName());//通过用户名获取该用户对应的角色
        //下面用于通过角色名获取对应的权限名
        for (String role:roles){
            List<String> lpermissions=getMapper.getPermissionByRoleName(role);
            info.addStringPermissions(lpermissions);
        }


        //将查询出的结果封装在权限信息里面
        info.addRoles(roles);
        return info;
    }
    /**
     * 验证当前登录的Subject
     * @param token
     * @return
     * @throws AuthenticationException
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        String username = (String) token.getPrincipal();
        Shiro_User user=getMapper.getShiroUserByName(username);
        if (user==null){
            logger.info("数据库中不存在该用户");
            return null;
        }
        SimpleAuthenticationInfo info = new SimpleAuthenticationInfo(user,user.getPassword(),getName());
        return info;
    }
}

```

我大概解释一下上面的代码:

> realm 可以写在配置文件中（ini 文件中）也可以自定义，一般均采用这种自定义规则，也可以同时写多个 realm，只需将你的 realm 装配到你的 securityMa

GetMapper 对应的代码以及其他代码都已存到 git 上面，大家可以在文章末尾进行下载:

## 2.2 接着配置 shiro 的配置类，添加监听器，与过滤器，springBoot 与普通的 springmvc 模式不同

- springMvc 下的
  监听器，过滤器只需在 web.xml 文件中添加

```xml
<listerner></listerner>
<filter></filter>
<filterMapping></fliterMapping>
```

在 springBoot 中只需添加一个配置类，在每个配置上加上@Bean 即可，何为配置类，所有的类只要加上@Configuration 就变成了一个配置类，大家可以参考我下面的配置类自己再用时可以直接 copy，稍作修改即可

```java
package com.zhiyi.shiro.config;

import org.apache.shiro.mgt.SecurityManager;
import org.apache.shiro.spring.LifecycleBeanPostProcessor;
import org.apache.shiro.spring.web.ShiroFilterFactoryBean;
import org.apache.shiro.web.mgt.DefaultWebSecurityManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;

import java.util.LinkedHashMap;
import java.util.Map;

@Configuration
public class ShiroConfig {
    private Logger logger = LoggerFactory.getLogger(this.getClass());

    /**
     * 负责shiroBean的生命周期
     */
    @Bean
    public LifecycleBeanPostProcessor lifecycleBeanPostProcessor(){
        return new LifecycleBeanPostProcessor();
    }
    /**
     *这是个自定义的认证类，继承子AuthorizingRealm，负责用户的认证和权限处理
     */
    @Bean
    @DependsOn("lifecycleBeanPostProcessor")
    public MyShiroRealm shiroRealm(){
        MyShiroRealm realm = new MyShiroRealm();
        //realm.setCredentialsMatcher(hashedCredentialsMatcher());
        return realm;
    }
    /** 安全管理器
     * 将realm加入securityManager
     * @return
     */
    @Bean
    public SecurityManager securityManager(){
        //注意是DefaultWebSecurityManager！！！
        DefaultWebSecurityManager securityManager = new DefaultWebSecurityManager();
        securityManager.setRealm(shiroRealm());
        return securityManager;
    }
    /** shiro filter 工厂类
     * 1.定义ShiroFilterFactoryBean
     * 2.设置SecurityManager
     * 3.配置拦截器
     * 4.返回定义ShiroFilterFactoryBean
     */
    @Bean
    public ShiroFilterFactoryBean shiroFilter(SecurityManager securityManager){
        //1
        ShiroFilterFactoryBean shiroFilterFactoryBean = new ShiroFilterFactoryBean();

        //2
        //注册securityManager
        shiroFilterFactoryBean.setSecurityManager(securityManager);
       logger.info("注册安全管理器成功");
        //3
        // 拦截器+配置登录和登录成功之后的url
        //LinkHashMap是有序的，shiro会根据添加的顺序进行拦截
        Map<String,String> filterChainDefinitionMap = new LinkedHashMap<String, String>();
        //配置不会被拦截的连接  这里顺序判断
        //anon，所有的url都可以匿名访问
        //authc：所有url都必须认证通过才可以访问
        //user，配置记住我或者认证通过才能访问
        //logout，退出登录
        //配置过滤器链，让静态资源可以自由随意访问
//        filterChainDefinitionMap.put("/JQuery/**","anon");
//        filterChainDefinitionMap.put("/js/**","anon");
//        //配置退出过滤器
//        filterChainDefinitionMap.put("/example1","anon");
//        filterChainDefinitionMap.put("/lxt","anon");
//        filterChainDefinitionMap.put("/login","authc");
//        filterChainDefinitionMap.put("/success","anon");
//        filterChainDefinitionMap.put("/index","anon");
//        filterChainDefinitionMap.put("/Register","anon");
//        filterChainDefinitionMap.put("/logout","logout");
//        //过滤连接自定义，从上往下顺序执行，所以用LinkHashMap /**放在最下边
//        filterChainDefinitionMap.put("/**","authc");
//        //设置登录界面，如果不设置为寻找web根目录下的文件
////        shiroFilterFactoryBean.setLoginUrl("/zhiyi");
//        //设置登录成功后要跳转的连接
//        shiroFilterFactoryBean.setSuccessUrl("/success");
//        //设置登录未成功，也可以说无权限界面
//        shiroFilterFactoryBean.setUnauthorizedUrl("/403");

        shiroFilterFactoryBean.setFilterChainDefinitionMap(filterChainDefinitionMap);
       logger.info("shiro拦截工厂注入类成功");

        //4
        //返回
        return shiroFilterFactoryBean;
    }





}

```

其中我注释掉了很多内容，但是需要什么服务自己开启即可
下面自己写一个 controller,service 测试一下，具体代码参考文章底部的 git 项目
Controller 层：

```java
package com.zhiyi.shiro.controller;

import com.zhiyi.shiro.service.ShiroService;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.apache.shiro.subject.Subject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletOutputStream;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

@Controller
@RequestMapping("shiro")
public class ShiroController {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    ShiroService shiroService;
    @ResponseBody
    @RequestMapping("login")
    public Map<String,Object> login(@RequestParam("userName")String userName,@RequestParam("passWord")String passWord, HttpServletResponse response, HttpServletRequest request){
        response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
        response.setHeader("Access-Control-Allow-Credentials", "true");// 允许服务器向浏览器跨域响应时更改浏览器（客户端）的cookie
        Map<String,Object> map=new HashMap<String,Object>();


        Subject subject=SecurityUtils.getSubject();//获取当前与系统交互的对象

        return  shiroService.confirmUserService(subject,userName,passWord,request);
    }
}
```

Service 层：

```java
package com.zhiyi.shiro.service;

import com.zhiyi.shiro.mapper.GetMapper;
import com.zhiyi.shiro.mapper.UpdateMapper;
import com.zhiyi.shiro.model.Shiro_User;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.apache.shiro.subject.Subject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

@Service
public class ShiroService {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    GetMapper getMapper;
    @Autowired
    UpdateMapper updateMapper;

    public  Map<String,Object> confirmUserService(Subject subject, String userName, String password, HttpServletRequest request){
        Map<String,Object> map=new HashMap<String,Object>();
        UsernamePasswordToken token=new UsernamePasswordToken(userName,password);//由用户名和密码组成
        try{
            subject.login(token);
            logger.info("登录成功");
            map.put("status",0);
            String tokenPass=session.getId();
            Shiro_User user=new Shiro_User();
            user.setUserName(userName);
            List<String>roles=getMapper.getAllROles();
            List<String>listRoles=new LinkedList<String>();
            for(String role:roles){
                if(subject.hasRole(role)){
                    listRoles.add(role);
                }
            }
            List<String> lpermissions=getMapper.getAllPermissions();
            List<String>listPermissions=new LinkedList<String>();
            for (String permission:lpermissions){
                if(subject.isPermitted(permission)){
                    logger.info("该用户的拥有权限---"+permission);
                    if(!listPermissions.contains(permission)){
                        listPermissions.add(permission);
                    }

                }
            }
            map.put("permissions",listPermissions);
            map.put("roles",listRoles);
        }catch (UnknownAccountException uae){
            System.out.println("没有用户名为"+token.getPrincipal()+"的用户");
            map.put("status",1);
        } catch (IncorrectCredentialsException ice){
            System.out.println("用户名为："+token.getPrincipal()+"的用户密码不正确");
            map.put("status",2);
        } catch (LockedAccountException lae){
            System.out.println("用户名为："+token.getPrincipal()+"的用户已被冻结");
            map.put("status",3);
        } catch (AuthenticationException e){
            System.out.println("未知错误！");
            map.put("status",4);
        }
        return  map;
    }
}

```

至此一个最最基本的 shiro 配置就结束了，想要获取更多 shiro 的功能，请自行上网搜索学习
git 地址：[点击此处](https://github.com/zhiyiTec/shiro_springBoot_vue.git)
