# 1.在pom.xml文件中引入对应的配置文件：
```
<!-- https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-redis -->
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-redis</artifactId>
			<version>1.4.7.RELEASE</version>
		</dependency>
```
# 2.在application.properties文件中加入以下配置：
```
# REDIS (RedisProperties)
# Redis数据库索引（默认为0）
spring.redis.database=0
# Redis服务器地址
spring.redis.host=localhost
# Redis服务器连接端口
spring.redis.port=6379
# Redis服务器连接密码（默认为空）
spring.redis.password=
# 连接池最大连接数（使用负值表示没有限制）
spring.redis.jedis.pool.max-active=8
# 连接池最大阻塞等待时间（使用负值表示没有限制）
spring.redis.jedis.pool.max-wait=-1
# 连接池中的最大空闲连接
spring.redis.jedis.pool.max-idle=8
# 连接池中的最小空闲连接
spring.redis.jedis.pool.min-idle=0
# 连接超时时间（毫秒）
spring.redis.timeout=0
```
# 3.执行测试：
随便新建一个类：
```
package com.boot.zhiyi.test;

import redis.clients.jedis.Jedis;

public class Redis_String {
	public static void main(String[] args) {
		Jedis jedis=new Jedis();
		System.out.println("连接成功");
		jedis.auth("zx12345678");//如果redis没有密码就删除这句话即可
		jedis.set("zx", "zhuxu");
		
		System.out.println("redis存储的字符串为="+jedis.get("zx"));
	}
}

```