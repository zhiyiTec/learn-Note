##### 我们再添加另一项目的maven依赖后发现仍然不起作用，在对引入该jar包的项目进行编译时会出现“找不到程序包”的错误。这是由于一般作为jar包被引入其他项目，说明是公共模块代码，不需要单独部署。此时应该将该项目的pom.xml中如下内容去掉：
``` java
	<build>
		<plugins>
		<!--被引入的spring boot jar 包不能引入此plugin ，否则引入此jar包的项目编译时会报 找不到程序包 的错误-->
			<!--<plugin>-->
				<!--<groupId>org.springframework.boot</groupId>-->
				<!--<artifactId>spring-boot-maven-plugin</artifactId>-->
			<!--</plugin>-->
		</plugins>
	</build>
```
去掉这个插件之后重新打包即可