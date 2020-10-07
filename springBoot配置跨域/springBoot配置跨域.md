<!-- TOC -->

- [1.配置跨域有两种方式](#1配置跨域有两种方式)
  - [1.在每个controller中设置](#1在每个controller中设置)
  - [2.新建一个配置类WebMvcConfig配置全局的跨域](#2新建一个配置类webmvcconfig配置全局的跨域)
- [2.前端访问](#2前端访问)

<!-- /TOC -->
# 1.配置跨域有两种方式
##  1.在每个controller中设置
``` java
 @ResponseBody
    @RequestMapping(value = "/cs", method = RequestMethod.POST)
    public String cs(HttpServletResponse response, HttpServletRequest request) {
        response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
        response.setHeader("Access-Control-Allow-Credentials", "true");// 允许服务器向浏览器跨域响应时更改浏览器（客户端）的cookie
        
        return "跨域测试";
    }
```
这种方式只能确保这一个controller中可以跨域
## 2.新建一个配置类WebMvcConfig配置全局的跨域
``` java
import org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
@Configuration
public class WebMvcConfig  extends WebMvcConfigurerAdapter {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("*")
                .allowedMethods("GET","HEAD","POST","PUT","PATCH","DELETE","OPTIONS","TRACE")
                .allowCredentials(true);
    }
}
```
* registry.allowedOrigins(““)设置跨域访问的域名，如果是，默认都可以访问。
* registry.allowCredentials(true)设置是否允许客户端发送cookie信息。默认是false，但是如果不接受cookie，则会导致客户端获取的session不同这种问题
# 2.前端访问
如果前端发送ajax请求保证同一个会话中session相同，则需设置 withCredentials: true
``` js
  $.ajax({
                url: "http://localhost:9001/loginOut",
                // data: data,
                dataType: "json",
                type: "get",
                // async: false, //此处必须要有这句话，否则任然会传值失败
                //加上这句话,允许浏览器向服务器跨域请求时携带cookie
                //加上这句话,允许浏览器向服务器跨域请求时携带cookie
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true,
                success: function(data) {
                    console.log(data)
                },
                error: function() {
                    alert("token认证失败")
                }
            });
        })
```