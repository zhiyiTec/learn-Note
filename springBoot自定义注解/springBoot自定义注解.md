# 1.自定义注解一般用拦截或者在处理业务逻辑之前进行的操作，比如我们需要在每次处理前端发出的请求时进行认证token的操作，这时就需要自定义注解
# 2.自定义注解的实现
## 2.1创建自定义注解类
下面以拦截token的注解为例
``` java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface UserLoginToken {
    boolean required() default true;
}

```
这时一个自定义注解就已经实现，下面创建一个自定义注解的拦截操作
## 2.2 创建拦截器
``` java
import com.personal.api.po.Constants;
import com.personal.indentity.annoation.PassToken;
import com.personal.indentity.annoation.UserEffective;
import com.personal.indentity.annoation.UserLoginToken;
import com.personal.indentity.service.UserService;
import com.personal.indentity.utils.TokenUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import redis.clients.jedis.Jedis;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.lang.reflect.Method;

@Controller
public class AuthenticationInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 如果不是映射到方法直接通过
        if (!(handler instanceof HandlerMethod)) {
            return true;
        }
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        Method method = handlerMethod.getMethod();
        /**检查有没有需要用户权限的注解**/
        if (method.isAnnotationPresent(UserLoginToken.class)) {
            UserLoginToken userLoginToken = method.getAnnotation(UserLoginToken.class);
            if (userLoginToken.required()) {
                // 执行认证
                if (token == null) {
                    throw new RuntimeException("无token，请重新登录");
                }
                //校验token有效性
                Boolean verify = false;
                try {
                    verify = TokenUtils.verifyToken(token);
                } catch (Exception e) {
                    verify = false;
                    throw new RuntimeException("无效token");
                }
                if(!verify){
                    throw new RuntimeException("token校验失败");
                }
                return true;
            }
        }
        return true;
    }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}
```
## 2.3如何使用这个注解
我们自定完成一个注解之后和spring内置注解一样，只需在controller中添加对应的注解即可
``` java
  /***
     * 判断token是否有效
     * @date 2019/06/14
     * @return String 返回类型
     */
    @ResponseBody
    @UserLoginToken
    @RequestMapping(value = "/judgeToken", method = RequestMethod.GET)
    public String getMessage(HttpServletResponse response, HttpServletRequest request) {
        return "校验token";
    }
```
至此一个完整的自定义注解就已经实现了