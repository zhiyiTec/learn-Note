## 1.引入对应的jar包，下面只讲述如何使用maven工程导入项目jar包:
> 在pom.xml文件中添加
```xml
<dependency>
  <!-- jsoup HTML parser library @ http://jsoup.org/ -->
  <groupId>org.jsoup</groupId>
  <artifactId>jsoup</artifactId>
  <version>1.10.2</version>
</dependency>
```
## 2.先讲述几个比较常用的爬虫函数：
* 1. 载入文件
> 从URL加载文档，使用Jsoup.connect()方法从URL加载HTML。
```java
Document document = Jsoup.connect("http://www.yiibai.com").get();
    System.out.println(document.title());//此处用于输出网页标题
     System.out.println(document);//此处用于输出网页里的所有代码
```
* 2. 从文件加载文档
使用Jsoup.parse()方法从文件加载HTML。
```java
Document document = Jsoup.parse( new File( "D:/temp/index.html" ) , "utf-8" );
    System.out.println(document.title());
```
* 3.从String加载文档
```java
String html = "<html><head><title>First parse</title></head>"
                    + "<body><p>Parsed HTML into a doc.</p></body></html>";
    Document document = Jsoup.parse(html);
    System.out.println(document.title());
```
* 4.获取HTML页面中的所有链接
```java
 Document document = Jsoup.parse(new File("C:/Users/zkpkhua/Desktop/yiibai-index.html"), "utf-8");
    Elements links = document.select("a[href]");  
    for (Element link : links) 
    {
         System.out.println("link : " + link.attr("href"));  
         System.out.println("text : " + link.text());  
    }
```
* 5.获取HTML页面中的所有图像
```java
 Document document = Jsoup.parse(new File("C:/Users/zkpkhua/Desktop/yiibai-index.html"), "utf-8");
    Elements images = document.select("img[src~=(?i)\\.(png|jpe?g|gif)]");
    for (Element image : images) 
    {
        System.out.println("src : " + image.attr("src"));
        System.out.println("height : " + image.attr("height"));
        System.out.println("width : " + image.attr("width"));
        System.out.println("alt : " + image.attr("alt"));
    }
```
* 6.获取url的链接
```java

```
