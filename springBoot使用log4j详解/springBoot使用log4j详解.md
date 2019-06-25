# 1.引入log4j依赖：
```xml
<!-- https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-log4j -->
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-log4j</artifactId>
			<version>1.3.8.RELEASE</version>
		</dependency>

```
此处有个注意点，就是关闭springboot自带的依赖：
将springstarter依赖：
```xml
<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
```
改为：
```xml
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
```
# 2.在构件路径下：也就是resource目录（和application.properties同一级目录下创建log4j.properties文件），log4j.properties具体配置如下：
``` yml
# LOG4J配置，设置输出的最低级别，此处设置的是根节点
log4j.rootCategory=debug, stdout,file,D

# 控制台输出  只输出error级别以上的信息
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss,SSS} %5p %c{1}:%L - %m%n
# 输出到文件
# root日志输出
log4j.appender.file=org.apache.log4j.FileAppender
log4j.appender.file.file=D:/LogFile/allLog.log
log4j.appender.file.DatePattern='.'yyyy-MM-dd
# 此处设置文件内容不覆盖，而是自动往后追加  
log4j.appender.file.Append=true  
log4j.appender.file.Threshold =info
log4j.appender.file.layout=org.apache.log4j.PatternLayout
log4j.appender.file.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss,SSS} %5p %c{1}:%L - %m%n
# 错误日志输出
# error日志输出
log4j.appender.D = org.apache.log4j.DailyRollingFileAppender
## 异常日志文件名
log4j.appender.D.File = D:/LogFile/error.log
log4j.appender.D.Append = true
## 只输出ERROR级别以上的日志!!!
log4j.appender.D.Threshold = ERROR 
log4j.appender.D.layout = org.apache.log4j.PatternLayout
log4j.appender.D.layout.ConversionPattern =%d{yyyy-MM-dd HH:mm:ss,SSS} %5p %c{1}:%L - %m%n
# 发送日志给邮件
og4j.appender.MAIL=org.apache.log4j.net.SMTPAppender
log4j.appender.MAIL.Threshold=ERROR
log4j.appender.MAIL.BufferSize=10
www.wuset.com ">log4j.appender.MAIL.From=1773203101@qq.com
log4j.appender.MAIL.SMTPHost=www.wusetu.com
log4j.appender.MAIL.Subject=Log4J Message
www.wusetu.com ">log4j.appender.MAIL.To=1773203101@qq.com
log4j.appender.MAIL.layout=org.apache.log4j.PatternLayout
log4j.appender.MAIL.layout.ConversionPattern=[framework] %d - %c -%-4r [%t] %-5p %c %x - %m%n

```
# 3.进行简单的测试：
新建一个测试类：
``` java
package com.boot.zhiyi.logTest;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class logTest {
	 private Logger logger = LoggerFactory.getLogger(this.getClass());
	 @Test
	 public void testLog() {
		 
		logger.error("用户为绑定就开始缴费");
	 }
}
```
更多具体的log4j配置，请参考此处 [点击查看](https://www.jianshu.com/p/f3c489996ac1)