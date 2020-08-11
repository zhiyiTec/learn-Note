<!-- TOC -->

- [1.设置外键失败问题](#1设置外键失败问题)
  - [1.1.问题描述](#11问题描述)
  - [1.2.解决方案：](#12解决方案)
- [2.批量删除出现 sql injection violation, multi-statement not allow : ...的问题](#2批量删除出现-sql-injection-violation-multi-statement-not-allow--的问题)
  - [2.1.问题描述：](#21问题描述)
  - [2.2.解决方案](#22解决方案)
    - [2.2.1.引入阿里的Durid连接池](#221引入阿里的durid连接池)
    - [2.2.2.创建一个配置类来开启Druid的防火墙配置](#222创建一个配置类来开启druid的防火墙配置)
    - [2.2.3.在application.properties的配置文件中修改jdb连接路径，添加allowMultiQueries=true，改为如下：](#223在applicationproperties的配置文件中修改jdb连接路径添加allowmultiqueriestrue改为如下)
- [3.设置外键提示3780错误](#3设置外键提示3780错误)
  - [3.1 问题描述](#31-问题描述)
  - [3.2解决方案:](#32解决方案)
    - [3.2.1 首先注意两者是否均选中或均未选中Unsigned，再次注意编码的方式上是否一致，最后在查看是否属于同一种类型](#321-首先注意两者是否均选中或均未选中unsigned再次注意编码的方式上是否一致最后在查看是否属于同一种类型)
- [4.mysql使用循环生成测试数据](#4mysql使用循环生成测试数据)
  - [4.1.创建存储过程](#41创建存储过程)
  - [4.2.使用这个存储过程](#42使用这个存储过程)
  - [4.3.使用完成之后可以删除这个存储过程](#43使用完成之后可以删除这个存储过程)

<!-- /TOC -->
# 1.设置外键失败问题
## 1.1.问题描述
> alter table stu add foreign key(cno) references user(id);
Failed to add the foreign key constraint. Missing index for constraint 'stu_ibfk_1' in the referenced table 'user'
## 1.2.解决方案：
> 作为外键，user表中的id必须是唯一值,因此得添加约束unique,或者primary key;   
设置外键的办法：
```java
ALTER TABLE user ADD UNIQUE (id)
```
# 2.批量删除出现 sql injection violation, multi-statement not allow : ...的问题
## 2.1.问题描述：
> 【异常】——Cause: java.sql.SQLException: sql injection violation, multi-statement not allow :XXXXX
## 2.2.解决方案
不允许批量执行，其本质错误是Druid的防火墙配置(WallConfig)中变量
multiStatementAllow默认为false，在源码中当多条语句时，判断了是否开启了批量执行,
否则报错不允许执行多条语句。
### 2.2.1.引入阿里的Durid连接池
```xml
<!-- https://mvnrepository.com/artifact/com.alibaba/druid-spring-boot-starter -->
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid-spring-boot-starter</artifactId>
			<version>${durid}</version>
		</dependency>
```
### 2.2.2.创建一个配置类来开启Druid的防火墙配置
```java
package com.boot.zhiyi.config;

import com.alibaba.druid.filter.Filter;
import com.alibaba.druid.pool.DruidDataSource;
import com.alibaba.druid.wall.WallConfig;
import com.alibaba.druid.wall.WallFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;
import org.springframework.context.annotation.Primary;

import javax.sql.DataSource;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
@Configuration
public class DuridConfig {

    @Autowired
    WallFilter wallFilter;
    @Bean(name = "dataSource")    //声明其为Bean实例
    @Primary  //在同样的DataSource中，首先使用被标注的DataSource
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource dataSource(){
        DruidDataSource datasource = new DruidDataSource();

        // filter
        List<Filter> filters = new ArrayList<>();
        filters.add(wallFilter);
        datasource.setProxyFilters(filters);

        return datasource;
    }
    @Bean(name = "wallFilter")
    @DependsOn("wallConfig")
    public WallFilter wallFilter(WallConfig wallConfig) {
        WallFilter wallFilter = new WallFilter();
        wallFilter.setConfig(wallConfig);
        return wallFilter;

    }

    @Bean(name = "wallConfig")
    public WallConfig wallConfig(){
        WallConfig wallConfig = new WallConfig();
        wallConfig.setMultiStatementAllow(true);//允许一次执行多条语句
        wallConfig.setNoneBaseStatementAllow(true);//允许一次执行多条语句
        return wallConfig;
    }


}

```
### 2.2.3.在application.properties的配置文件中修改jdb连接路径，添加allowMultiQueries=true，改为如下：
```java
spring.datasource.url=jdbc:mysql://localhost:3306/vqqdeoplay?autoReconnect=true&useUnicode=true&characterEncoding=utf-8&&zeroDateTimeBehavior=CONVERT_TO_NULL&&serverTimezone=GMT%2B8&useSSL=false&&allowMultiQueries=true
```
# 3.设置外键提示3780错误
## 3.1 问题描述
> 3780 - Referencing column 'bookdetailld' and referenced column 'id' in foreign key constraint 'borrow f kl' are
incompatible
## 3.2解决方案:
### 3.2.1 首先注意两者是否均选中或均未选中Unsigned，再次注意编码的方式上是否一致，最后在查看是否属于同一种类型
# 4.mysql使用循环生成测试数据
## 4.1.创建存储过程
``` java
delimiter //
create procedure getData()
BEGIN
DECLARE i INT;
SET i=1;
WHILE i<200000 DO
INSERT INTO trade VALUES ("172.20.0.41","2016-03-31_09-19-23.404","trade","sendMessage.trade.Test","main","2532",UUID(),"XGD","main","content");
SET i=i+1;
END WHILE;
END
//
```
## 4.2.使用这个存储过程
```java
CALL getData();
```
## 4.3.使用完成之后可以删除这个存储过程
``` java
DROP PROCEDURE getData;
```