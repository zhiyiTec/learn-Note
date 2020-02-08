# 1.设置外键失败问题
### 1.问题描述
> alter table stu add foreign key(cno) references user(id);
Failed to add the foreign key constraint. Missing index for constraint 'stu_ibfk_1' in the referenced table 'user'
### 2.解决方案：
> 作为外键，user表中的id必须是唯一值,因此得添加约束unique,或者primary key;   
设置外键的办法：
``` java
ALTER TABLE user ADD UNIQUE (id)
```
# 2.批量删除出现 sql injection violation, multi-statement not allow : ...的问题
### 1.问题描述：
> 【异常】——Cause: java.sql.SQLException: sql injection violation, multi-statement not allow :XXXXX
### 2.解决方案
不允许批量执行，其本质错误是Druid的防火墙配置(WallConfig)中变量
multiStatementAllow默认为false，在源码中当多条语句时，判断了是否开启了批量执行,
否则报错不允许执行多条语句。
#### 1.引入阿里的Durid连接池
``` xml
<!-- https://mvnrepository.com/artifact/com.alibaba/druid-spring-boot-starter -->
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid-spring-boot-starter</artifactId>
			<version>${durid}</version>
		</dependency>
```
##### 2.创建一个配置类来开启Druid的防火墙配置
``` java
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
###### 3.在application.properties的配置文件中修改jdb连接路径，添加allowMultiQueries=true，改为如下：
```java
spring.datasource.url=jdbc:mysql://localhost:3306/vqqdeoplay?autoReconnect=true&useUnicode=true&characterEncoding=utf-8&&zeroDateTimeBehavior=CONVERT_TO_NULL&&serverTimezone=GMT%2B8&useSSL=false&&allowMultiQueries=true
```