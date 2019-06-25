# 1.首先引入maven依赖：
```xml
		<!-- jstl JSP标准标签库  -->
		<dependency>
		    <groupId>javax.servlet</groupId>
		    <artifactId>jstl</artifactId>
		    <version>1.2</version>
		</dependency>
		<!-- 返回jsp页面还需要这个依赖 -->
		<dependency>
		    <groupId>org.apache.tomcat.embed</groupId>
		    <artifactId>tomcat-embed-jasper</artifactId>
		    <scope>provided</scope>
		</dependency>
```
# 2.配置返回的视图层，也就是modelAndView最后要返回并且要跳转的页面
### 在application.properties中配置
```yml
#jsp path
spring.mvc.view.prefix=/static/jsp/
spring.mvc.view.suffix=.jsp
```
注意上面你要返回的jsp页面的路径
# 3.modelAndView的使用：
``` java
//无论是@RestController还是@Controller都不影响返回页面
	@RequestMapping(value = "/loginPage", method = RequestMethod.GET)
	public ModelAndView loginPage(HttpServletRequest request,HttpServletResponse response){
		ModelAndView mav = new ModelAndView();
		mav.setViewName("login");
		
		return mav;
	}

```
