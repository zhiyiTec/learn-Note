# 1.一般在创建springBoot的web项目时会自动引入依赖，如果没有就在pom.xml文件中加入这个依赖：
```
<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>
```
这儿有个坑就是上面的依赖作用scope（范围）是只有在test包中，所以想自己创建包来进行测试，就需要把<scope>给删除掉，如下所示：
```
<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			
		</dependency>
```
# 2.接着就是新建有个类，如下：
```
package com.boot.zhiyi.test;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import redis.clients.jedis.Jedis;
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class Redis_String {
	@Test
	public void Redis_String() {
		Jedis jedis=new Jedis();
		System.out.println("连接成功");
		jedis.auth("zx12345678");
		jedis.set("zx", "zhuxu");
		System.out.println("redis存储的字符串为="+jedis.get("zx"));
	}
	
}
```
这就可以进行单元测试了