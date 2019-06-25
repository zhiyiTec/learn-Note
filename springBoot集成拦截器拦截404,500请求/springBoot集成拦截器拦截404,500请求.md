# 1.直接在controller写一个控制器，但是这个控制器要实现HandlerInterceptor接口，并且要实习里面的三个方法:
* preHandle;
> 	  preHandle方法是进行处理器拦截用的，顾名思义，该方法将在Controller处理之前进行调用，SpringMVC中的Interceptor拦截器是链式的，可以同时存在
>	  多个Interceptor，然后SpringMVC会根据声明的前后顺序一个接一个的执行，而且所有的Interceptor中的preHandle方法都会在
>	  Controller方法调用之前调用。SpringMVC的这种Interceptor链式结构也是可以进行中断的，这种中断方式是令preHandle的返
>	  回值为false，当preHandle的返回值为false的时候整个请求就结束了。
* postHandle;
>这个方法只会在当前这个Interceptor的preHandle方法返回值为true的时候才会执行。postHandle是进行处理器拦截用的，它的执行时间是在处理器进行处理之
> 后，也就是在Controller的方法调用之后执行，但是它会在DispatcherServlet进行视图的渲染之前执行，也就是说在这个方法中你可以对ModelAndView进行操
> 作。这个方法的链式结构跟正常访问的方向是相反的，也就是说先声明的Interceptor拦截器该方法反而会后调用，这跟Struts2里面的拦截器的执行过程有点像，
> 只是Struts2里面的intercept方法中要手动的调用ActionInvocation的invoke方法，Struts2中调用ActionInvocation的invoke方法就是调用下一个Interceptor
> 或者是调用action，然后要在Interceptor之前调用的内容都写在调用invoke之前，要在Interceptor之后调用的内容都写在调用invoke方法之后。
* afterCompletion
>  该方法也是需要当前对应的Interceptor的preHandle方法的返回值为true时才会执行。该方法将在整个请求完成之后，也就是DispatcherServlet渲染了视图执行，
>  这个方法的主要作用是用于清理资源的，当然这个方法也只能在当前这个Interceptor的preHandle方法的返回值为true时才会执行。    
> 
具体详细代码：
```java
package com.boot.zhiyi.controller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.stereotype.Controller;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class ErrorInterceptor implements HandlerInterceptor {
	
	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
			throws Exception {
		// TODO Auto-generated method stub
		System.out.println("------------开始处理请求------------");
		return true;
	}

	
	@Override
	public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
			ModelAndView modelAndView) throws Exception {
		if (response.getStatus() == 500) {
			modelAndView.setViewName("/errorpage/500");
            request.getRequestDispatcher("500.html").forward(request, response);
		} else if (response.getStatus() == 404) {
			modelAndView.setViewName("/errorpage/404");
            request.getRequestDispatcher("404.html").forward(request, response);
		}
	}


	@Override
	public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
			throws Exception {
		// TODO Auto-generated method stub
		System.out.println("-----------------------------------资源调用结束，开始清理占用资源-----------------------------------");
	}

}

```
# 2.创建一个配置类，并继承WebMvcConfigurerAdapter，用于定义拦截规则：
```java
package com.boot.zhiyi.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

import com.boot.zhiyi.controller.ErrorInterceptor;

@SuppressWarnings("deprecation")
@Configuration
public class MyWebAppConfigurer extends WebMvcConfigurerAdapter {
	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		// 多个拦截器组成一个拦截器链
		// addPathPatterns 用于添加拦截规则
		// excludePathPatterns 用户排除拦截
		registry.addInterceptor(new ErrorInterceptor()).addPathPatterns("/**");
		super.addInterceptors(registry);
	}
}

```
到这里拦截器就基本实现了，我上面给出的例子中是可以实现对404或者500的拦截。

不过需要注意的是，这种拦截有时候也会出现特别大问题。例如一个网页中如果需要加载很多的图片或者js文件资源，
可是正好没有这个资源，也就是找不到这么多个资源报一堆的404错误。这个时候如果还是单纯的使用这种拦截就会出现null指针异常的情况。
### 解决办法：
创建一个控制器并实现ErrorController接口，这样就可以利用这个类来处理上面发生的问题了。
具体代码:
```java
package com.boot.zhiyi.controller;

import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.web.bind.annotation.RequestMapping;

public class MainsiteErrorController implements ErrorController {
	private static final String ERROR_PATH = "/error";
	@RequestMapping(value=ERROR_PATH)
    public String handleError(){
        return "errorpage/error";
    }
    @Override
    public String getErrorPath() {
        return ERROR_PATH;
    }

}

```
至此一个对错误请求的拦截请求就此结束了

