# 项目引入lombok后报错：java: java.lang.ExceptionInInitializerError
这个错误信息是：初始化异常,这里出现的原因是我们引入的lombok的依赖版本太低了，只要去Maven仓库下载最新的依赖就好了
``` xml
<!--lombok-->
        <!-- https://mvnrepository.com/artifact/org.projectlombok/lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.12</version>
            <scope>provided</scope>
        </dependency>
```