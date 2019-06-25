# 1.引入相关的maven依赖：
```xml
 <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
            <version>2.1.3.RELEASE</version>
        </dependency>
 <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <version>1.4.197</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.6</version>
        </dependency>
```
# 2.在application.properties文件中进行配置：
```yml
# 数据源配置
# 使用H2数据库
spring.datasource.platform=h2
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.username=root
spring.datasource.password=123456
# 数据项配置
spring.datasource.schema=classpath:db/user.sql
# 配置h2的远程访问
spring.h2.console.settings.web-allow-others=true
# 配置程序开启时就会启动h2 web consloe
spring.h2.console.enabled=true
#，进行该配置，你就可以通过YOUR_URL/h2-console访问h2 web consloe。YOUR_URL是你程序的访问URl
spring.h2.console.path=/h2-console
# 显示sql语句
spring.jpa.show-sql = true
# 这个必须加，每次启动对应实体
spring.jpa.hibernate.ddl-auto = update
# 是否生成ddl语句
spring.jpa.generate-ddl=false
```
# 3.编写对应的model：
```java
package com.zhiyi.h2.model;

import lombok.Data;

import javax.persistence.*;

@Entity
@Table(name="user")
@Data
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column
    private String name;
    @Column
    private String phone;

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getPhone() {
        return phone;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }
}

```
注意：上面的注解(@Entity,@Table(name="user"),@Data，@Id，@GeneratedValue(strategy = GenerationType.IDENTITY),@Column)是lombok中的，建议花费五分钟自行学习一下，很有用
# 4编写启动程序时需要运行的sql语句，在classpath路径，也就是和application.properites同级的目录下创建一个db目录，里面存放需要执行的sql脚本
```sql
DROP TABLE IF EXISTS user;
CREATE TABLE user (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name varchar(35),
 PHONE varchar(35)
);
select * from user;
insert into user(id,name,PHONE) values(784,'在写作协作','123456');
insert into user(id,name,phone) values(90,'是的','123456');

select * from user;
```
# 5.编写对应的Dao:
```java
package com.zhiyi.h2.dao;
import com.zhiyi.h2.model.User;
import org.springframework.data.repository.CrudRepository;
public interface H2Dao extends CrudRepository<User,Long> {
    User findByName(String name);
    @Override
    Iterable<User> findAll();
    @Override
    void delete(User user);
}
```
注意：delete中的对象不是自己创建的，而是先自己通过查询，然后在进行删除，下面我会在测试用例中体现
# 6.编写对应的测试用例:
```java
package com.zhiyi.h2.test;

import com.zhiyi.h2.model.User;
import com.zhiyi.h2.dao.H2Dao;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.List;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class H2Test {
    @Autowired
    private H2Dao H2Service;
    @Test
    public void testGetUserByName(){
        User user=H2Service.findByName("zx");
        System.out.println("查询到用户名为："+user.getName()+"的电话为："+user.getPhone());
    }
    @Test
    public void testGetUserAll(){
        Iterable<User>userIterable=H2Service.findAll();
       for(User user:userIterable){
           System.out.println("查询到用户名为："+user.getName()+"的电话为："+user.getPhone());
       }
    }
    @Test
    public void getUserByPhone(){
    String phone="123456";
       List<User>userList= H2Service.findUserByPhone(phone);
       Integer userNu=userList.size();
        System.out.println("通过电话"+phone+"查询到"+userNu+"为用户");

    }
    @Test
    public void delUserByPhone(){
        String phone="123456";
        List<User>userList= H2Service.findUserByPhone(phone);
        H2Service.delete(userList.get(0));
    }

}
```
到此集成h2就此结束了