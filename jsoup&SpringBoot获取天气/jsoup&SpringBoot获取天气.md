# 本程序使用jsoup爬取中国天气网的天气信息，使用log4j作为日志进行记录，使用java cocket通信作为发送源发送天气信息，并且将数据保存在数据库中
# 1.引入 依赖：
* 1.引入jsoup：
``` xml
<dependency>
			<groupId>org.jsoup</groupId>
			<artifactId>jsoup</artifactId>
			<version>1.10.2</version>
		</dependency>

```
* 2.引入log4j:
```xml
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
2.先配置log4j日志：
> 在构件路径下：也就是resource目录（和application.properties同一级目录下创建log4j.properties文件），log4j.properties具体配置如下：
```yml
# LOG4J配置，设置输出的最低级别
log4j.rootCategory=debug, stdout,file,D,DATABASE,MAIL

# 控制台输出  只输出error级别以上的信息
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.Threshold =error
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss,SSS} %5p %c{1}:%L - %m%n
# 输出到文件
# root日志输出
log4j.appender.file=org.apache.log4j.FileAppender
log4j.appender.file.file=D:/LogFile/weather/allLog.log
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
log4j.appender.D.File = D:/LogFile/weather/error.log
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
# 将日志存储到数据库
log4j.appender.DATABASE=org.apache.log4j.jdbc.JDBCAppender
log4j.appender.DATABASE.URL=jdbc:mysql://localhost:3306/logtest?autoReconnect=true&useUnicode=true&characterEncoding=utf-8&&zeroDateTimeBehavior=CONVERT_TO_NULL&&serverTimezone=GMT%2B8
log4j.appender.DATABASE.driver=com.mysql.jdbc.Driver
log4j.appender.DATABASE.user=root
log4j.appender.DATABASE.password=123456
log4j.appender.DATABASE.sql=INSERT INTO log4j (UUID,CDATED,CLOGGER,CLEVEL,CMESSAGE) VALUES ('%x','[framework] %d - %c -%-4r [%t] %-5p %c %x - %m%n','%C','%p','%m')
log4j.appender.DATABASE.layout=org.apache.log4j.PatternLayout
log4j.appender.DATABASE.layout.ConversionPattern=[framework] %d - %c -%-4r [%t] %-5p %c %x - %m%n
log4j.appender.A1=org.apache.log4j.DailyRollingFileAppender
log4j.appender.A1.File=SampleMessages.log4j
log4j.appender.A1.DatePattern=yyyyMMdd-HH'.log4j'
log4j.appender.A1.layout=org.apache.log4j.xml.XMLLayout
```
# 3.开始详细的爬取天气过程
```java
package com.boot.zhiyi.getWeather;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class GetWeather {
	public static void main(String[] args) throws IOException {
		
		
			String city="101190101";
			String url = "http://www.weather.com.cn/weather/" +city  + ".shtml";
			List<String>lweather=new LinkedList<String>();//用于存储天气状况
			List<String>lweatherData=new LinkedList<String>();//用于存储日期
			List<String>lweatherTempture=new LinkedList<String>();//用于存储温度
			List<String>lweatherWin=new LinkedList<String>();//用于存储风向
			List<String>lweather_ALl=new LinkedList<String>();
			try {
				Document doc = Jsoup.connect(url).get();
				Elements content = doc.getElementsByClass("t clearfix");
				for (Element e : content) {
					Document conDoc = Jsoup.parse(e.toString());
					Elements cru = conDoc.getElementsByClass("crumbs fl");
					Elements sky = content.select("li[class^=sky skyid lv]");
					
					for (Element e1 : sky) {
						Elements weatherData=e1.select("h1");//此处用于获取日期天气
						lweatherData.add(weatherData.text());
						Elements weather=e1.select("p[class=wea]");//用于获取天气信息
						lweather.add(weather.text());
						Elements weatherTempture= e1.select("p[class=tem]");//用于获取天气温度
						lweatherTempture.add(weatherTempture.text());
						Elements weatherWin=e1.select("span");//用于获取风向
						lweatherWin.add(weatherWin.attr("title"));
						
					}
					
					//System.out.println(sky.toString());
				}
				
			} catch (Exception e) {
				e.printStackTrace();
			}
 
			
		System.out.println("天气查询完毕！！");
		System.out.println("当前城市【"+"南京"+"】");
		for(int i=0;i<lweather.size();i++) {
			String wea_All="日期:"+lweatherData.get(i)+",天气状况:"+lweather.get(i)+",温度："+lweatherTempture.get(i)+",风向："+lweatherWin.get(i);
			lweather_ALl.add(wea_All);
			//System.out.println("日期:"+lweatherData.get(i)+",天气状况:"+lweather.get(i)+",温度："+lweatherTempture.get(i)+",风向："+lweatherWin.get(i));
		}
		for(String weaAl:lweather_ALl) {
			System.out.println(weaAl);
		}
	}
}
```
更详细的整体框架(包括页面)可以下载我的gitHub里面的内容，下载[点击此处]()