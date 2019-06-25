# 第一章——shiro 入门

## 1.默认已经创建好 web 项目,只需要添加一些必要的依赖即可，本课程默认使用的架构是 springBoot

```xml
 <!--集成shiro-->
        <!-- https://mvnrepository.com/artifact/org.apache.shiro/shiro-spring -->
        <dependency>
            <groupId>org.apache.shiro</groupId>
            <artifactId>shiro-spring</artifactId>
            <version>1.4.0</version>
        </dependency>
```

其实还应该添加日志搭配，本课程采用 log4j 日志，不会或者不熟悉的伙伴，可以[参考此处](https://blog.csdn.net/zhiyikeji/article/details/85955010)

## 2.在 resource 目录下添加 shiro 对应的配置文件 shiro.ini 文件:

```ini
[users]
root=123456,admin
test=123456,test

[roles]
admin=*
test=search,add,update
```

我先大概说一下具体怎么写这种配置文件的内容，shiro 的工作流程是用户对应角色，角色对应权限，所以先写用户，类似于 key value 的写法

> root=123456,admin 表示用户名为 root 的这位用户，登录密码为 123456,对应的角色是 admin
> admin=\* 表示 admin 这个角色拥有所有的权限
> 先写到此处编写一个对应的单元测试了解如何使用，至于如何使用单元测试[点击此处](https://blog.csdn.net/zhiyikeji/article/details/85867305)
> 对应测试的代码如下(认真牢记我注释的地方):

```java
package com.zhiyi.shiro.test;

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.UsernamePasswordToken;
import org.apache.shiro.config.IniSecurityManagerFactory;
import org.apache.shiro.mgt.SecurityManager;
import org.apache.shiro.subject.Subject;
import org.apache.shiro.util.Factory;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class ShiroTest {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Test
    public void test(){
        Factory<SecurityManager>factory=new IniSecurityManagerFactory("classpath:shiro.ini");//此处创建工厂来调用配置文件
        SecurityManager securityManager=factory.getInstance();
        SecurityUtils.setSecurityManager(securityManager);//此处是全局的设置，只需要设置一次即可
        Subject subject=SecurityUtils.getSubject();//获取当前与系统交互的对象
        UsernamePasswordToken token=new UsernamePasswordToken("root","123456");//由用户名和密码组成

        try {

            subject.login(token);//调用subject的login方法进行登录
            if(subject.isAuthenticated()){
                //subject.isAuthenticated()：用于判断是否验证成功，成功返回true,否则返回false
                logger.info("用户验证成功");
                if(subject.hasRole("admin")){
                    //subject.hasRole("admin"):用于判断当前这个用户是否拥有admin角色，拥有返回true，否则返回fasle
                    logger.info("该用户当前身份为管理员");
                }
                    if(subject.isPermitted("search")){
                        //subject.isPermitted("search"),判断这个用户是否拥有search权限，有的话返回true,否则返回false
                    logger.info("该用户拥有search权限");
                }
                 if(subject.isPermittedAll("search","add")){
                    //subject.isPermittedAll:用于判断该用户是否拥有多个权限
                    logger.info("该用户拥有search,add权限");
                }
            }
        }catch (Exception e){
            e.printStackTrace();
            logger.info("用户名或密码错误，验证失败");
        }
    }
}
```

# 第二章——ini 文件以及自定义 realm

## 1.先引入一个新的概念 Realm,我们在第一章使用的工厂就是对 Realm 的封装，具体看一下如何运行

- 1.首先编写一个对应的 Realm 的配置类，并且实现 Realm 的接口，代码如下，仔细看注释:

```java
package com.zhiyi.shiro.config;

import org.apache.shiro.authc.*;
import org.apache.shiro.realm.Realm;
import org.apache.shiro.realm.RealmFactory;

public class MyRealm  implements Realm {
    /**
     * 设置数据源的名字
     * @return
     */
    @Override
    public String getName() {
        return "myRealm";
    }

    /**
     * 设置数据源的支持策略，本数据源设置只支持userName,Password策略
     * @param token
     * @return
     */
    @Override
    public boolean supports(AuthenticationToken token) {
        return token instanceof UsernamePasswordToken;
    }

    /**
     * 获取认证信息,即设置匹配规则
     * @param token
     * @return
     * @throws AuthenticationException
     */
    @Override
    public AuthenticationInfo getAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        String userName=String.valueOf(token.getPrincipal());
        String password=String.valueOf((char [])token.getCredentials());
        if(!"root".equals(userName)){
            throw new UnknownAccountException();
        }else if(!"123456".equals(password)){
            throw new IncorrectCredentialsException();
        }
        return new SimpleAuthenticationInfo(userName,password,getName());
    }
}

```

- 编写一个单元测试:

```java
package com.zhiyi.shiro.test;

import com.zhiyi.shiro.config.MyRealm;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.UsernamePasswordToken;
import org.apache.shiro.authc.pam.AtLeastOneSuccessfulStrategy;
import org.apache.shiro.authc.pam.ModularRealmAuthenticator;
import org.apache.shiro.authz.ModularRealmAuthorizer;
import org.apache.shiro.authz.permission.WildcardPermissionResolver;
import org.apache.shiro.mgt.DefaultSecurityManager;
import org.apache.shiro.subject.Subject;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class ShiroIniTest {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Test
    public void test(){
        DefaultSecurityManager securityManager=new DefaultSecurityManager();
        ModularRealmAuthenticator authenticator=new ModularRealmAuthenticator();//此处设置验证的策略
        authenticator.setAuthenticationStrategy(new AtLeastOneSuccessfulStrategy());//设置至少有一匹配的策略
        securityManager.setAuthenticator(authenticator) ;

        //下面用于进行授权
        ModularRealmAuthorizer authorizer=new ModularRealmAuthorizer();
        authorizer.setPermissionResolver(new WildcardPermissionResolver());
        securityManager.setAuthorizer(authorizer);//设置授权到securityManager上
        securityManager.setRealm(new MyRealm());//设置数据源
        SecurityUtils.setSecurityManager(securityManager);


        //下面用于登录
        Subject subject=SecurityUtils.getSubject();//获取当前与系统交互的对象
        UsernamePasswordToken token=new UsernamePasswordToken("root","123456");//由用户名和密码组成
        try{
            subject.login(token);
            logger.info("登录成功");
        }catch (AuthenticationException e){
            logger.info("验证失败");
        }
    }
}

```

下面解释一下:

```java
 DefaultSecurityManager securityManager=new DefaultSecurityManager();
        ModularRealmAuthenticator authenticator=new ModularRealmAuthenticator();//此处设置验证的策略
        authenticator.setAuthenticationStrategy(new AtLeastOneSuccessfulStrategy());//设置至少有一匹配的策略
        securityManager.setAuthenticator(authenticator) ;

        //下面用于进行授权
        ModularRealmAuthorizer authorizer=new ModularRealmAuthorizer();
        authorizer.setPermissionResolver(new WildcardPermissionResolver());
        securityManager.setAuthorizer(authorizer);//设置授权到securityManager上
        securityManager.setRealm(new MyRealm());//设置数据源
```

等价于:

```java
 Factory<SecurityManager>factory=new IniSecurityManagerFactory("classpath:shiro.ini");
        SecurityManager securityManager=factory.getInstance();
        SecurityUtils.setSecurityManager(securityManager);//此处是全局的设置，只需要设置一次即可
```

# 第三章——使用 mysql 数据源

## 先创建数据库,sql 语句如下（mySql）

```sql
/*
SQLyog Ultimate v11.33 (64 bit)
MySQL - 8.0.13 : Database - shiro
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`shiro` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `shiro`;

/*Table structure for table `shiro_role_permission` */

DROP TABLE IF EXISTS `shiro_role_permission`;

CREATE TABLE `shiro_role_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(32) NOT NULL COMMENT '角色名',
  `permissionName` varchar(32) NOT NULL COMMENT '权限名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `shiro_role_permission` */

insert  into `shiro_role_permission`(`id`,`roleName`,`permissionName`) values (1,'admin','/add.html'),(2,'admin','/del.html'),(3,'test','/get.html'),(4,'test','/add.html'),(5,'guest','/get.html');

/*Table structure for table `shiro_user` */

DROP TABLE IF EXISTS `shiro_user`;

CREATE TABLE `shiro_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户ID',
  `password` varchar(32) NOT NULL COMMENT '密码',
  `userName` varchar(32) NOT NULL COMMENT '用户名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `shiro_user` */

insert  into `shiro_user`(`id`,`userId`,`password`,`userName`) values (1,'000001','123456','admin'),(2,'000002','123456','test');

/*Table structure for table `shiro_user_role` */

DROP TABLE IF EXISTS `shiro_user_role`;

CREATE TABLE `shiro_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(32) NOT NULL COMMENT '角色名称',
  `userId` varchar(32) NOT NULL COMMENT '用户ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `shiro_user_role` */

insert  into `shiro_user_role`(`id`,`roleName`,`userId`) values (1,'admin','000001'),(2,'guest','000002'),(3,'test','000002');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

```

## 2.接着在 resource 目录下新建一个 ini 文件用于编写对应的配置，但是我们的用户名，密码以及角色，权限均是从数据库查询出来的，所以不用编写[user],[role],[permission]等配置，直接写[main]

代码如下

```ini
[main]
#↓ 使用druid数据源
dataSource=com.alibaba.druid.pool.DruidDataSource
#↓ MySQL驱动
dataSource.driverClassName=com.mysql.jdbc.Driver
#↓ MySQL相关参数配置
dataSource.url=jdbc:mysql://localhost:3306/shiro?autoReconnect=true&useUnicode=true&characterEncoding=utf-8&&zeroDateTimeBehavior=CONVERT_TO_NULL&&serverTimezone=GMT%2B8
dataSource.username=root
# 注意如果数据库没有密码就要把下面这一行注释掉，不允许出现dataSource.password=  这种写法
dataSource.password=123456

#↓ 使用 JdbcRealm 作为当前验证的Realm
jdbcRealm=org.apache.shiro.realm.jdbc.JdbcRealm
# 是检查权限
jdbcRealm.permissionsLookupEnabled = true
# 设置Realm的数据源
jdbcRealm.dataSource=$dataSource



# 重写sql语句
# 根据用户id查询出密码
jdbcRealm.authenticationQuery = select password from shiro_user where userId = ?
# 根据用户id查询出角色
jdbcRealm.userRolesQuery = select roleName from shiro_user_role where userId =?
# 根据查询的角色查找对应的权限
jdbcRealm.permissionsQuery = select permissionName from shiro_role_permission where roleName = ?

#把查询出的数据源指定给securityManager,如果有多个数据源没用逗号隔开
securityManager.realms=$jdbcRealm
```

注意，本数据源使用的阿里的 durid 数据源，所以别忘了导依赖:

```xml
 <!-- druid -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.9</version>
        </dependency>
```

## 3.接着编写我们对应的单元测试了

```java
package com.zhiyi.shiro.test;

import com.zhiyi.shiro.config.MyRealm;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.UsernamePasswordToken;
import org.apache.shiro.authc.pam.AtLeastOneSuccessfulStrategy;
import org.apache.shiro.authc.pam.ModularRealmAuthenticator;
import org.apache.shiro.authz.ModularRealmAuthorizer;
import org.apache.shiro.authz.permission.WildcardPermissionResolver;
import org.apache.shiro.config.IniSecurityManagerFactory;
import org.apache.shiro.mgt.DefaultSecurityManager;
import org.apache.shiro.mgt.SecurityManager;
import org.apache.shiro.subject.Subject;
import org.apache.shiro.util.Factory;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class ShiroJdbcTest {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Test
    public void test(){
        Factory<SecurityManager> factory=new IniSecurityManagerFactory("classpath:shiro_mysql.ini");
        SecurityManager securityManager=factory.getInstance();
        SecurityUtils.setSecurityManager(securityManager);//此处是全局的设置，只需要设置一次即可
        Subject subject=SecurityUtils.getSubject();//获取当前与系统交互的对象
        UsernamePasswordToken token=new UsernamePasswordToken("000001","123456");//由用户名和密码组成
        try {

            subject.login(token);//调用subject的login方法进行登录
            if(subject.isAuthenticated()){
                logger.info("用户验证成功");
                if(subject.hasRole("admin")){
                    logger.info("该用户当前身份为管理员");
                }
                if(subject.isPermitted("search")){
                    logger.info("该用户拥有search权限");
                }
                if(subject.isPermittedAll("search","add","del")){
                    logger.info("该用户拥有search,add权限");
                }
            }
        }catch (Exception e){
            e.printStackTrace();
            logger.info("用户名或密码错误，验证失败");
        }
    }
}

```
