1.创建好springBoot web项目，在pom.xml文件中添加maven依赖：
``` xml
 <!-- MySQL 连接驱动依赖 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
             <version>8.0.13</version>
        </dependency>
         <!-- Spring Boot Mybatis 依赖 -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.3.2</version>
        </dependency>
```
在application.properties文件中配置数据源：
```yml
## 数据源配置
spring.datasource.url=jdbc:mysql://localhost:3306/springbootdb?autoReconnect=true&useUnicode=true&characterEncoding=utf-8&&zeroDateTimeBehavior=CONVERT_TO_NULL&&serverTimezone=GMT%2B8
spring.datasource.username=root
spring.datasource.password=123456
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
## Mybatis 配置
mybatis.typeAliasesPackage=org.spring.springboot.domain
mybatis.mapperLocations=classpath:mapper/*.xml
```
在构件路径下也就是src/main/resources目录下新建一个目录mapper，编写对应的mapper.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.boot.zhiyi.mapper.CityMapper">//注意此处是mapper的目录
	<resultMap id="BaseResultMap" type="com.boot.zhiyi.Po.CityPo">
		<result column="id" property="id" />
		<result column="province_id" property="province_id" />
		<result column="city_name" property="city_name" />
		<result column="description" property="description" />
	</resultMap>
	<sql id="Base_Column_List">
		id, province_id, city_name, description
	</sql>
	<select id="getCityInfoByName" resultMap="BaseResultMap"
		parameterType="java.lang.String">
		select
		<include refid="Base_Column_List" />
		from city
		where city_name = #{cityName}
	</select>
</mapper>
```
接着在src/main/java下面创建mapper po,service,serviceImpl,controller，编写对应的内容即可     
在主运行程序上添加注解@MapperScan("com.boot.zhiyi.mapper")//mapper 接口类扫描包配置
```
@SpringBootApplication
//mapper 接口类扫描包配置
@MapperScan("com.boot.zhiyi.mapper")
public class SbWebApplication {
	public static void main(String[] args) {
		SpringApplication.run(SbWebApplication.class, args);
	}
}
```
运行程序即可
对应的详细代码请参考：