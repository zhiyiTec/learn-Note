<!-- TOC -->

- [1.我们先大概了解一下 jwt认证token的基本原理](#1我们先大概了解一下-jwt认证token的基本原理)
  - [1.什么是JWT](#1什么是jwt)
  - [2.JWT请求流程](#2jwt请求流程)
  - [3.JWT的主要应用场景](#3jwt的主要应用场景)
    - [Header](#header)
    - [Payload](#payload)
      - [标准中注册的声明 (建议但不强制使用) ：](#标准中注册的声明-建议但不强制使用-)
      - [公共的声明 ：](#公共的声明-)
      - [私有的声明 ：](#私有的声明-)
    - [Signature](#signature)
- [2.与springBoot项目的集成](#2与springboot项目的集成)
  - [1.添加maven依赖](#1添加maven依赖)
  - [2.自定义两个注解](#2自定义两个注解)
  - [3.简单自定义一个实体类User](#3简单自定义一个实体类user)
  - [4.Mapper接口](#4mapper接口)
  - [5.service](#5service)
  - [6.service的实现类](#6service的实现类)
  - [7.UserMapper.xml](#7usermapperxml)
  - [8.token的生成方法](#8token的生成方法)
  - [9.拦截器](#9拦截器)
    - [HandlerInterceptor接口主要定义了三个方法](#handlerinterceptor接口主要定义了三个方法)
    - [主要流程:](#主要流程)
  - [10.配置拦截器](#10配置拦截器)
  - [11.controller层](#11controller层)
  - [12.测试](#12测试)
    - [1.先访问login接口](#1先访问login接口)
    - [2.进行接口的token验证](#2进行接口的token验证)

<!-- /TOC -->
# 1.我们先大概了解一下 jwt认证token的基本原理
## 1.什么是JWT
> Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).定义了一种简洁的，自包含的方法用于通信双方之间以JSON对象的形式安全的传递信息。因为数字签名的存在，这些信息是可信的，JWT可以使用HMAC算法或者是RSA的公私秘钥对进行签名。
## 2.JWT请求流程
![](1.webp)
* 1. 用户使用账号和面发出post请求；
* 2. 服务器使用私钥创建一个jwt；
* 3. 服务器返回这个jwt给浏览器；
* 4. 浏览器将该jwt串在请求头中像服务器发送请求；
* 5. 服务器验证该jwt；
* 6. 返回响应的资源给浏览器。
## 3.JWT的主要应用场景
> 身份认证在这种场景下，一旦用户完成了登陆，在接下来的每个请求中包含JWT，可以用来验证用户身份以及对路由，服务和资源的访问权限进行验证。由于它的开销非常小，可以轻松的在不同域名的系统中传递，所有目前在单点登录（SSO）中比较广泛的使用了该技术。 信息交换在通信的双方之间使用JWT对数据进行编码是一种非常安全的方式，由于它的信息是经过签名的，可以确保发送者发送的信息是没有经过伪造的。

优点:
> * 1.简洁(Compact): 可以通过URL，POST参数或者在HTTP header发送，因为数据量小，传输速度也很快
>* 2.自包含(Self-contained)：负载中包含了所有用户所需要的信息，避免了多次查询数据库
>* 3.因为Token是以JSON加密的形式保存在客户端的，所以JWT是跨语言的，原则上任何web形式都支持。
>* 4.不需要在服务端保存会话信息，特别适用于分布式微服务。

JWT的结构:
JWT是由三段信息构成的，将这三段信息文本用.连接一起就构成了JWT字符串。
``` js
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```
JWT包含了三部分：
* Header 头部(标题包含了令牌的元数据，并且包含签名和/或加密算法的类型)
* Payload 负载 (类似于飞机上承载的物品)
* Signature 签名/签证
### Header
JWT的头部承载两部分信息：token类型和采用的加密算法。
``` java
{ 
  "alg": "HS256",
   "typ": "JWT"
} 
```
声明类型:这里是jwt
声明加密的算法:通常直接使用 HMAC SHA256
加密算法是单向函数散列算法，常见的有MD5、SHA、HAMC。
MD5(message-digest algorithm 5) （信息-摘要算法）缩写，广泛用于加密和解密技术，常用于文件校验。校验？不管文件多大，经过MD5后都能生成唯一的MD5值
SHA (Secure Hash Algorithm，安全散列算法），数字签名等密码学应用中重要的工具，安全性高于MD5
HMAC (Hash Message Authentication Code)，散列消息鉴别码，基于密钥的Hash算法的认证协议。用公开函数和密钥产生一个固定长度的值作为认证标识，用这个标识鉴别消息的完整性。常用于接口签名验证
### Payload
载荷就是存放有效信息的地方。
有效信息包含三个部分
* 1.标准中注册的声明
* 2.公共的声明
* 3.私有的声明
#### 标准中注册的声明 (建议但不强制使用) ：
* iss: jwt签发者
* sub: 面向的用户(jwt所面向的用户)
* aud: 接收jwt的一方
* exp: 过期时间戳(jwt的过期时间，这个过期时间必须要大于签发时间)
* nbf: 定义在什么时间之前，该jwt都是不可用的.
* iat: jwt的签发时间
* jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。
#### 公共的声明 ：
公共的声明可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.
#### 私有的声明 ：
私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。
### Signature
jwt的第三部分是一个签证信息
这个部分需要base64加密后的header和base64加密后的payload使用.连接组成的字符串，然后通过header中声明的加密方式进行加盐secret组合加密，然后就构成了jwt的第三部分。
密钥secret是保存在服务端的，服务端会根据这个密钥进行生成token和进行验证，所以需要保护好。

<font color=#FF0000 >了解以上知识后我们开始进行与springBoot项目的集成</font>
# 2.与springBoot项目的集成
## 1.添加maven依赖
``` xml
 <!--token-->
        <dependency>
            <groupId>com.auth0</groupId>
            <artifactId>java-jwt</artifactId>
            <version>3.3.0</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.47</version>
        </dependency>
```
注意：我们默认是已经配置好mybatis的web项目，还未配置myBatis?[点击此处](https://blog.csdn.net/zhiyikeji/article/details/85019689?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522160048535419195188331273%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=160048535419195188331273&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_v2~rank_blog_default-19-85019689.pc_v2_rank_blog_default&utm_term=springBoot&spm=1018.2118.3001.4187)
## 2.自定义两个注解
用来跳过验证的PassToken
``` java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface PassToken {
    boolean required() default true;
}
```
需要登录才能进行操作的注解UserLoginToken
``` java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface UserLoginToken {
    boolean required() default true;
}
```
@Target:注解的作用目标
* @Target(ElementType.TYPE)——接口、类、枚举、注解
* @Target(ElementType.FIELD)——字段、枚举的常量
* @Target(ElementType.METHOD)——方法
* @Target(ElementType.PARAMETER)——方法参数
* @Target(ElementType.CONSTRUCTOR) ——构造函数
* @Target(ElementType.LOCAL_VARIABLE)——局部变量
* @Target(ElementType.ANNOTATION_TYPE)——注解
* @Target(ElementType.PACKAGE)——包
 
@Retention：注解的保留位置
* RetentionPolicy.SOURCE:这种类型的Annotations只在源代码级别保留,编译时就会被忽略,在class字节码文件中不包含。
* RetentionPolicy.CLASS:这种类型的Annotations编译时被保留,默认的保留策略,在class文件中存在,但JVM将会忽略,运行时无法获得。
* RetentionPolicy.RUNTIME:这种类型的Annotations将被JVM保留,所以他们能在运行时被JVM或其他使用反射机制的代码所读取和使用。
* @Document：说明该注解将被包含在javadoc中
* @Inherited：说明子类可以继承父类中的该注解
![](2.png)
## 3.简单自定义一个实体类User
``` java
public class User  implements java.io.Serializable {
    /** 版本号 */
    private static final long serialVersionUID = 6111899065812654266L;
    /** 主键自增Id */
    private Integer userId;

    /** 用户民 */
    private String userName;

    /** 用户密码 */
    private String password;
    /**
     * 获取主键自增Id
     *
     * @return 主键自增Id
     */
    public Integer getUserId() {
        return this.userId;
    }

    /**
     * 设置主键自增Id
     *
     * @param userId
     *          主键自增Id
     */
    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    /**
     * 获取用户民
     *
     * @return 用户民
     */
    public String getUserName() {
        return this.userName;
    }

    /**
     * 设置用户民
     *
     * @param userName
     *          用户民
     */
    public void setUserName(String userName) {
        this.userName = userName;
    }

    /**
     * 获取用户密码
     *
     * @return 用户密码
     */
    public String getPassword() {
        return this.password;
    }

    /**
     * 设置用户密码
     *
     * @param password
     *          用户密码
     */
    public void setPassword(String password) {
        this.password = password;
    }
}
```
## 4.Mapper接口
``` java

public interface UserMapper {
    public List<User> getUserSelective(User user);

    public User getUserByPrimary(Integer userId);

    public User getUserByName(String userName);
}
```
## 5.service
UserService
```java

public interface UserService {
    /**
     * 通过用户名获取唯一用户
     * @param userName
     * @return
     */
    public User getUserByUserName(String userName);

    /**
     * 根据条件获取用户
     * @param user
     * @return
     */
    public List<User> getUserSelective(User user);

    /**
     * 通过主键获取用户
     * @param userId
     * @return
     */
    public User getUserByUserId(Integer userId);

}

```
TokenService
``` java
public interface TokenService {
    /**
     * 获取用户token
     * @param user
     * @return
     */
    public String getToken(User user);
}

```
## 6.service的实现类
UserServiceImpl
``` java
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserMapper userMapper;
    @Override
    public User getUserByUserName(String userName) {
        User user=userMapper.getUserByName(userName);
        return user;
    }

    @Override
    public List<User> getUserSelective(User user) {
        return userMapper.getUserSelective(user);
    }

    @Override
    public User getUserByUserId(Integer userId) {
        return userMapper.getUserByPrimary(userId);
    }
}
```
TokenServiceImpl
``` java
@Service
public class TokenServiceImpl implements TokenService {

    @Override
    public String getToken(User user) {
        Date start = new Date();
        long currentTime = System.currentTimeMillis() + 60* 60 * 1000;//一小时有效时间
        Date end = new Date(currentTime);
        String token = "";
        try {
            token = JWT.create().withAudience(user.getUserId().toString()).withIssuedAt(start).withExpiresAt(end)
                    .sign(Algorithm.HMAC256(user.getPassword()));
        }catch (Exception e){
            e.printStackTrace();
        }

        return token;
    }
}
```
注意：如果Algorithm.HMAC256无法使用，则手动引入外部的sunjce_provider.jar,[点击此处下载sunjce_provider.jar包](http://zhiyitec.top:2000/downLoad/sunjce_provider.jar)，不知道怎么引用外部Jar到项目中？[点击此处](https://blog.csdn.net/zhiyikeji/article/details/108655717)
## 7.UserMapper.xml
``` xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.dubbo.indetity.mapper.UserMapper">
    <sql id="allColumns">
        u.user_id, u.user_name, u.password
    </sql>
    <select id="getUserSelective" parameterType="com.dubbo.indetity.po.User" resultType="com.dubbo.indetity.po.User">
        SELECT
        <include refid="allColumns" />
        FROM user u WHERE 1 = 1
        <if test="userName != null and userName != ''">
            AND u.user_name LIKE CONCAT('%', #{userName}, '%')
        </if>
        <if test="password != null and password != ''">
            AND u.password =#{password}
        </if>
    </select>
    <select id="getUserByPrimary" parameterType="java.lang.Integer" resultType="com.dubbo.indetity.po.User">
        SELECT <include refid="allColumns" /> FROM User as u WHERE u.user_id =#{userId}
    </select>
    <select id="getUserByName" parameterType="java.lang.String" resultType="com.dubbo.indetity.po.User">
        SELECT <include refid="allColumns" /> FROM User as u WHERE u.user_name =#{userName}
        limit 1
    </select>
</mapper>
```
## 8.token的生成方法
TokenUtils
``` java
package com.dubbo.consumer.indentity.util;

import com.auth0.jwt.JWT;
import org.springframework.util.StringUtils;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

public class TokenUtils {
    /**
     * 通过token获取用户id
     * @return
     */
    public static String getTokenUserId() {
        String token = getToken();
        String userId = JWT.decode(token).getAudience().get(0);
        return userId;
    }




    /**
     * 从session或者header中获取token
     * @return
     */
    public static String getToken(){
        String token=null;
        //先从session中获取token
        HttpSession session   = WebUtils.getSession();
        Object tokenObject=session.getAttribute("token");
        if(tokenObject!=null){
            token=tokenObject.toString();
        }
        if(StringUtils.isEmpty(token)){
            //从 http 请求头中取出 token
            token = WebUtils.getRequest().getHeader("token");
        }
        return token;
    }
}

```
WebUtils
``` java
package com.dubbo.consumer.indentity.util;

import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

public class WebUtils {
    /**
     * 获取request
     *
     * @return
     */
    public static HttpServletRequest getRequest() {
        ServletRequestAttributes requestAttributes = (ServletRequestAttributes) RequestContextHolder
                .getRequestAttributes();
        return requestAttributes == null ? null : requestAttributes.getRequest();
    }

    /**
     * 获取session
     *
     * @return
     */
    public static HttpSession getSession() {
        HttpSession session   = getRequest().getSession();
        return session;
    }
}

```
Algorithm.HMAC256():使用HS256生成token,密钥则是用户的密码，唯一密钥的话可以保存在服务端。
withAudience()存入需要保存在token的信息，这里我把用户ID存入token中
## 9.拦截器
用于获取token并验证token
``` java
package com.dubbo.consumer.indentity.interceptor;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTDecodeException;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.dubbo.consumer.indentity.annoation.PassToken;
import com.dubbo.consumer.indentity.annoation.UserLoginToken;
import com.dubbo.consumer.indentity.util.TokenUtils;
import com.dubbo.indetity.po.User;
import com.dubbo.indetity.service.UserService;
import org.apache.dubbo.config.annotation.Reference;
import org.springframework.stereotype.Controller;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.lang.reflect.Method;

@Controller
public class AuthenticationInterceptor implements HandlerInterceptor {
    @Autowired
    UserService userService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("=========================启动token拦截器======================");
        String token = TokenUtils.getToken();
        // 如果不是映射到方法直接通过
        if(!(handler instanceof HandlerMethod)){
            return true;
        }
        HandlerMethod handlerMethod=(HandlerMethod)handler;
        Method method=handlerMethod.getMethod();
        //检查是否有passtoken注释，有则跳过认证
        if (method.isAnnotationPresent(PassToken.class)) {
            PassToken passToken = method.getAnnotation(PassToken.class);
            if (passToken.required()) {
                return true;
            }
        }
        //检查有没有需要用户权限的注解
        if (method.isAnnotationPresent(UserLoginToken.class)) {
            UserLoginToken userLoginToken = method.getAnnotation(UserLoginToken.class);
            if (userLoginToken.required()) {
                // 执行认证
                if (token == null) {
                    throw new RuntimeException("无token，请重新登录");
                }
                // 获取 token 中的 userid
                String userId;
                try {
                    userId = JWT.decode(token).getAudience().get(0);
                } catch (JWTDecodeException j) {
                    throw new RuntimeException("401");
                }
                User user = userService.getUserByUserId(Integer.valueOf(userId));
                if (user == null) {
                    throw new RuntimeException("用户不存在，请重新登录");
                }
                // 验证 token
                JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256(user.getPassword())).build();
                try {
                    jwtVerifier.verify(token);
                } catch (JWTVerificationException e) {
                    throw new RuntimeException("401");
                }
                return true;
            }
        }
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}

```
### HandlerInterceptor接口主要定义了三个方法
1.boolean preHandle ()：
预处理回调方法,实现处理器的预处理，第三个参数为响应的处理器,自定义Controller,返回值为true表示继续流程（如调用下一个拦截器或处理器）或者接着执行
postHandle()和afterCompletion()；false表示流程中断，不会继续调用其他的拦截器或处理器，中断执行。

2.void postHandle()：
后处理回调方法，实现处理器的后处理（DispatcherServlet进行视图返回渲染之前进行调用），此时我们可以通过modelAndView（模型和视图对象）对模型数据进行处理或对视图进行处理，modelAndView也可能为null。

3.void afterCompletion():
整个请求处理完毕回调方法,该方法也是需要当前对应的Interceptor的preHandle()的返回值为true时才会执行，也就是在DispatcherServlet渲染了对应的视图之后执行。用于进行资源清理。整个请求处理完毕回调方法。如性能监控中我们可以在此记录结束时间并输出消耗时间，还可以进行一些资源清理，类似于try-catch-finally中的finally，但仅调用处理器执行链中
### 主要流程:
1.从 http 请求头中取出 token，
2.判断是否映射到方法
3.检查是否有passtoken注释，有则跳过认证
4.检查有没有需要用户登录的注解，有则需要取出并验证
5.认证通过则可以访问，不通过会报相关错误信息
## 10.配置拦截器
在配置类上添加了注解@Configuration，标明了该类是一个配置类并且会将该类作为一个SpringBean添加到IOC容器内
``` java
package com.dubbo.consumer.indentity.cofig;


import com.dubbo.consumer.indentity.interceptor.AuthenticationInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.format.FormatterRegistry;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.validation.MessageCodesResolver;
import org.springframework.validation.Validator;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.method.support.HandlerMethodReturnValueHandler;
import org.springframework.web.servlet.HandlerExceptionResolver;
import org.springframework.web.servlet.config.annotation.*;

import java.util.List;

@Configuration
public class InterceptorConfig implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {

    }

    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {

    }

    @Override
    public void configureAsyncSupport(AsyncSupportConfigurer configurer) {

    }

    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {

    }

    @Override
    public void addFormatters(FormatterRegistry registry) {

    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authenticationInterceptor()).addPathPatterns("/**");
    }
    @Bean
    public AuthenticationInterceptor authenticationInterceptor() {
        return new AuthenticationInterceptor();
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {

    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {

    }

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {

    }

    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {

    }

    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {


    }

    @Override
    public void addReturnValueHandlers(List<HandlerMethodReturnValueHandler> handlers) {

    }

    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {

    }

    @Override
    public void extendMessageConverters(List<HttpMessageConverter<?>> converters) {

    }

    @Override
    public void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {

    }

    @Override
    public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {

    }

    @Override
    public Validator getValidator() {
        return null;
    }

    @Override
    public MessageCodesResolver getMessageCodesResolver() {
        return null;
    }
}
```
> WebMvcConfigurerAdapter该抽象类其实里面没有任何的方法实现，只是空实现了接口
WebMvcConfigurer内的全部方法，并没有给出任何的业务逻辑处理，这一点设计恰到好处的让我们不必去实现那些我们不用的方法，都交由WebMvcConfigurerAdapter抽象类空实现,如果我们需要针对具体的某一个方法做出逻辑处理,仅仅需要在
WebMvcConfigurerAdapter子类中@Override对应方法就可以了。
InterceptorRegistry内的addInterceptor需要一个实现HandlerInterceptor接口的拦截器实例，addPathPatterns方法用于设置拦截器的过滤路径规则。
这里我拦截所有请求，通过判断是否有@LoginRequired注解 决定是否需要登录

## 11.controller层
在数据访问接口中加入登录操作注解
``` java
package com.dubbo.consumer.indentity;

import com.dubbo.api.po.BaseResult;

import com.dubbo.consumer.indentity.annoation.UserLoginToken;
import com.dubbo.consumer.indentity.util.TokenUtils;
import com.dubbo.indetity.po.User;
import com.dubbo.indetity.service.TokenService;


import com.dubbo.indetity.service.UserService;


import org.apache.dubbo.common.json.JSONObject;
import org.apache.dubbo.config.annotation.Reference;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;


@Controller
public class UserController {
    @Autowired
    UserService userService;
    @Autowired
    TokenService tokenService;

    // 登录
    @ResponseBody
    @RequestMapping(value = "/login" ,method = RequestMethod.POST)
    public String login(@RequestBody User user,HttpServletResponse response, HttpServletRequest request) {
        HttpSession session   =   request.getSession();
        User basic=userService.getUserByUserName(user.getUserName());
        User userForBase = new User();
        userForBase.setUserId(basic.getUserId());
        userForBase.setUserName(basic.getUserName());
        userForBase.setPassword(basic.getPassword());
        if (!userForBase.getPassword().equals(user.getPassword())) {
            return "密码错误";

        } else {
            String token = tokenService.getToken(userForBase);
            Cookie cookie = new Cookie("token", token);
            cookie.setPath("/");
            response.addCookie(cookie);
            session.setAttribute("token",token);
            return token;


        }
        return "获取失败";
    }
    /***
     * 这个请求需要验证token才能访问
     * @date 2019/06/14
     * @return String 返回类型
     */
    @ResponseBody
    @UserLoginToken
    @RequestMapping(value = "/getMessage" ,method = RequestMethod.GET)
    public String getMessage(HttpServletResponse response, HttpServletRequest request) {

        // 取出token中带的用户id 进行操作
        System.out.println(TokenUtils.getTokenUserId());

        return "您已通过验证";
    }
}
```
不加注解的话默认不验证，登录接口一般是不验证的。在getMessage()中我加上了登录注解，说明该接口必须登录获取token后，在请求头中加上token并通过验证才可以访问
## 12.测试
### 1.先访问login接口
![](3.png)
出现以上结果说明token获取成功
### 2.进行接口的token验证
![](4.png)
注意：网上大部分教程都没有将token添加至session中，所以你在测试时如果没有将token添加到session，你需要在postMan测试手动在请求头添加token,否则就会读取不到token导致失败
![](5.png)
至此一个简单的token集成到此结束