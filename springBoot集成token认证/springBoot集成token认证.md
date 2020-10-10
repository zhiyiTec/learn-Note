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

        <!--fastjson-->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.47</version>
        </dependency>
        <!-- 很好用的一个工具类包 这里用来处理json和AES加密-->
        <!-- https://mvnrepository.com/artifact/cn.hutool/hutool-all -->
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.4.4</version>
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
package com.personal.indentity.utils;

import cn.hutool.core.date.DateUtil;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTDecodeException;
import com.auth0.jwt.interfaces.Claim;
import com.auth0.jwt.interfaces.DecodedJWT;
import javax.servlet.http.HttpServletRequest;
import java.util.Arrays;
import java.util.Date;
import java.util.Map;

public class TokenUtils {
    /**
     * 签名秘钥
     */
    private static final String SECRET = "zx12345678";
    /**
     * 签发人
     */
    private static final String issuer="zhiyi";
    /**
     * token过期时间，单位:min
     */
    private static final Integer expireTime=2;

    /**
     * 从header中取token
     * @return
     */
    public static String getToken(){
        HttpServletRequest request =WebUtils.getRequest();
        String re=request.getHeader("token");
        return re;
    }

    /**
     * 创建token
     * @param json 需要放入token的参数，多个参数可以封装成json或者map
     * @return token
     */
    public static String createToken(JSONObject json) {
        try {
            // 加密方式
            Algorithm algorithm = Algorithm.HMAC256(SECRET);
            return JWT.create()
                    .withSubject(json.toString())
                    .withIssuer(issuer)
                    // 设置过期时间为60分钟后
                    .withExpiresAt(DateUtil.offsetMinute(new Date(), expireTime))
                    .withClaim("customString", "zhiyi")
                    .withArrayClaim("customArray", new Integer[]{1, 2, 3})
                    .sign(algorithm);
        } catch (Exception exception) {
            //Invalid Signing configuration / Couldn't convert Claims.
            System.out.println(exception.getMessage());
            return null;
        }
    }

    /**
     * 校验token合法性
     *
     * @param token to verify.
     */
    public static boolean verifyToken(String token) {
        try {
            Algorithm algorithm = Algorithm.HMAC256(SECRET);
            JWTVerifier verifier = JWT.require(algorithm)
                    // 验证签发人是否相同
                    .withIssuer(issuer)
                    .build();
            /*
             * 校验：
             * 格式校验：header.payload.signature
             * 加密方式校验 Header中的alg
             * 签名信息校验，防篡改
             * 载体Payload 中公有声明字段校验
             */
            verifier.verify(token);
            return true;
        } catch (Exception exception) {
            //Invalid signature/claims
            exception.printStackTrace();
            return false;
        }
    }

    /**
     * 解析token
     *
     * @param token to decode.
     */
    public static void decodeToken(String token) {
        try {
            DecodedJWT jwt = JWT.decode(token);
            Map<String, Claim> claims = jwt.getClaims();
            Claim customStringClaim = claims.get("customString");
            Claim customArrayClaim = claims.get("customArray");

            String issuer = jwt.getIssuer();
            String subject = jwt.getSubject();

            System.out.println(customStringClaim.asString());
            System.out.println(Arrays.toString(customArrayClaim.asArray(Integer.class)));
            System.out.println(issuer);
            System.out.println(JSONUtil.parseObj(subject).get("userId"));

        } catch (JWTDecodeException exception) {
            //Invalid token
            exception.printStackTrace();
        }
    }

    public static String getUserIdByToken(String token){
        DecodedJWT jwt = JWT.decode(token);
        Map<String, Claim> claims = jwt.getClaims();
        String subject = jwt.getSubject();
        String re=JSONUtil.parseObj(subject).get("userId").toString();
        return re;
    }


    public static void main(String[] args) {
        JSONObject subjectJson = new JSONObject();
        subjectJson.put("userId", 1);
        subjectJson.put("name", "ylc");
        String token = createToken(subjectJson);
        System.out.println("token:" + token);
        System.out.println("==============================================");
//
//        System.out.println("1 min exp,now verify result:" + verifyToke(token));
//        System.out.println("==============================================");
//
//        System.out.println("decode info:");
//        decodeToken(token);
//        System.out.println("================================================");
//        System.out.println("1 min later,verify result:"+verifyToke("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjoxLFwibmFtZVwiOlwieWxjXCJ9IiwiaXNzIjoiemhpeWkiLCJleHAiOjE2MDIzMzI2OTMsImN1c3RvbUFycmF5IjpbMSwyLDNdLCJjdXN0b21TdHJpbmciOiJ6aGl5aSJ9.v6AQ2mba8gGsHFpJ52EY4fwoN03gEDsCUUSafpPscyQ"));
//        System.out.println("================================================");
        System.out.println("userId:"+getUserIdByToken("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjoxLFwibmFtZVwiOlwieWxjXCJ9IiwiaXNzIjoiemhpeWkiLCJleHAiOjE2MDIzMzM1MjEsImN1c3RvbUFycmF5IjpbMSwyLDNdLCJjdXN0b21TdHJpbmciOiJ6aGl5aSJ9.BKU-X6Bre9kCbsCtQgwDO6UE7znqbM84xy8dH6R7AiY"));
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
package com.personal.indentity.interceptor;
import com.personal.indentity.annoation.PassToken;
import com.personal.indentity.annoation.UserLoginToken;
import com.personal.indentity.service.UserService;
import com.personal.indentity.utils.TokenUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.lang.reflect.Method;

@Controller
public class AuthenticationInterceptor implements HandlerInterceptor {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    UserService userService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        logger.info("=========================启动token拦截器======================");
        String token = TokenUtils.getToken();
        // 如果不是映射到方法直接通过
        if (!(handler instanceof HandlerMethod)) {
            return true;
        }
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        Method method = handlerMethod.getMethod();
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
                //校验token有效性
                Boolean verify = false;
                try {
                    verify = TokenUtils.verifyToken(token);
                } catch (Exception e) {
                    verify = false;
                    throw new RuntimeException("无效token");
                }
                if(!verify){
                    throw new RuntimeException("token校验失败");
                }
//                // 获取 token 中的 userid
//                if (verify) {
//                    String userId;
//                    try {
//                        userId = TokenUtils.getUserIdByToken(token);
//                    } catch (JWTDecodeException j) {
//                        throw new RuntimeException("401");
//                    }
//                    User user = userService.getUserByUserId(Integer.valueOf(userId));
//                    if (user == null) {
//                        throw new RuntimeException("用户不存在，请重新登录");
//                    }
//                } else {
//                    throw new RuntimeException("token校验失败");
//                }
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
package com.personal.indentity.controller;

import cn.hutool.json.JSONObject;
import com.personal.api.po.ResultResponse;
import com.personal.indentity.entity.Token;
import com.personal.indentity.entity.User;
import com.personal.indentity.service.UserService;
import com.personal.indentity.utils.TokenUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Controller
public class LoginController {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    UserService userService;
    @ResponseBody
    @RequestMapping(value = "/login",method = RequestMethod.POST)
    public ResultResponse login(@RequestBody User user, HttpServletResponse response, HttpServletRequest request){
        ResultResponse resultResponse=new ResultResponse();
        user.setUserName(user.getUsername());
        User basic=userService.getUserByUserName(user.getUserName());
        if(basic==null){
            resultResponse.markError("用户名或密码错误");
        }else {
            //比对密码
            if (user.getPassword().equals(basic.getPassword())){
                JSONObject subjectJson = new JSONObject();
                subjectJson.put("userId", 1);
                String token = TokenUtils.createToken(subjectJson);
                Cookie cookie = new Cookie("token", token);
                cookie.setPath("/");
                response.addCookie(cookie);
                resultResponse.markSuccess("token获取成功",new Token(token));
            }else{
                resultResponse.markError("用户名或密码错误");
            }
        }
        return resultResponse;
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