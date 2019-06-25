# 1.首先保证springBoot的版本是1.3之后
# 2.在maven中引入依赖
``` xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <optional>true</optional>
</dependency>
```
# 3.开启热部署
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <fork>true</fork>
            </configuration>
        </plugin>
    </plugins>
</build>
```
# ---------------------------------------------------------
# 顺便讲一下多环境配置
## 1.首先讲一下命名规则：
### 在Spring Boot中多环境配置文件名需要满足application-{profile}.properties的格式，其中{profile}对应你的环境标识，比如：
* application-dev.properties：开发环境 
* application-test.properties：测试环境 
* application-prod.properties：生产环境 
### 这些文件的存放在与application.properties同级目录中即可
## 2.如何启用环境配置：
> 只需要在application.properties文件中加入**spring.profiles.active=dev**就会加载application-dev.properties配置文件内容
 