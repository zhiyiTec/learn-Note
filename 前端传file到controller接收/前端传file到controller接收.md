# 本文就以选择excel导入作为例子来解析如何进行前后端的文件传值与接收，前端ajax,后端springBoot
# 1.准备：
* 1.导入excel的依赖:
``` xml
<!-- 导入poi -->
		<dependency>
			<groupId>org.apache.poi</groupId>
			<artifactId>poi</artifactId>
			<version>3.15</version>
		</dependency>
		<dependency>
			<groupId>org.apache.poi</groupId>
			<artifactId>poi-ooxml</artifactId>
			<version>3.15</version>
		</dependency>
```
* 2.设置接收的最大容量：    
 在application.properties文件中：
 ```yml
## 设置接收文件的大小
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=20MB
 ```
 # 2.前端代码：
 ```html
 <form action="http://localhost:8081/zhiyi/excleimport" method="POST" enctype="multipart/form-data">
        <input type="file" id="file1" name="fileContent">
    </form>
    <button id='btn'> 提交</button>
 ```
 这个是选择文件的file,注意这个input标签必须要在form表单中，而且form的enctype必须为multipart/form-data
 ```html

    <script>
        $("#btn").click(function() {
            var formData = new FormData();
            formData.append("excelFile", $("#file1")[0].files[0]);
            $.ajax({
                url: "http://localhost:8081/zhiyi/excleimport",
                data: formData,
                type: "post",
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log(data)
                },
                error: function() {
                    alert("失败")
                }
            });
        })
    </script>
 ```
 这个是js脚本内容,注意的是 processData，contentType这两个属性必须为false；
至此前端内容就结束了，可以直接copy了改就可以了
接下来再看看后端代码，我会贴出excel解析的部分，有需要的可以作为参考：
* controller层
```java
@ResponseBody
	@RequestMapping(value = "/excleimport", method = RequestMethod.POST)
	public Map<String, Object> excleimport(@RequestParam  MultipartFile excelFile,
			HttpServletResponse response) throws IOException {
		response.setHeader("Access-Control-Allow-Origin", "*");
		Map<String, Object> map = new HashMap<String, Object>();
		String name = excelFile.getOriginalFilename();
		if (!name.endsWith(".xls") && !name.endsWith(".xlsx")) {
			System.out.println("文件不是excel类型");
			map.put("filecondition", "文件类型错误");
		} else {
			ExcelImport.getDataFromExcel(excelFile.getInputStream());
		}
		map.put("result", "success");
		return map;
	}
```
到此所有的文件传值与接收就结束了，下面在附上ExcelImport.getDataFromExcel方法,也就是解析excel的方法：
```java
package com.boot.zhiyi.util;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class ExcelImport {
	  public static void getDataFromExcel(InputStream  InputStream )
	    {
	        
	        Workbook wookbook = null;
	        try 
	        {
	            //2003版本的excel，用.xls结尾
	            wookbook = new HSSFWorkbook(InputStream);//得到工作簿
	             
	        } 
	        catch (Exception ex) 
	        {
	            //ex.printStackTrace();
	            try
	            {
	                //2007版本的excel，用.xlsx结尾
	                
	                wookbook = new XSSFWorkbook(InputStream);//得到工作簿
	            } catch (IOException e)
	            {
	                // TODO Auto-generated catch block
	                e.printStackTrace();
	            }
	        }
	        
	        //得到一个工作表
	        Sheet sheet = wookbook.getSheetAt(0);
	        
	        //获得表头
	        Row rowHead = sheet.getRow(0);
	        
	        //判断表头是否正确
	        if(rowHead.getPhysicalNumberOfCells()<1 )
	        {
	            System.out.println("表头的数量不对!");
	        }
	        
	        //获得数据的总行数
	        int totalRowNum = sheet.getLastRowNum();
	        //要获得属性
	        Long phoneNumber=null ;
	        String deptName=null;
	        String userName = "";
	       //获得所有数据
	        for(int i = 1 ; i <= totalRowNum ; i++)
	        {
	            //获得第i行对象
	            Row row = sheet.getRow(i);
	            
	            //获得获得第i行第0列的 String类型对象
	            Cell cell = row.getCell((short)0);
	            phoneNumber =(long) cell.getNumericCellValue();
	            
	            //获得一个字符串类型的数据
	            cell = row.getCell((short)1);
	            deptName =   cell.getStringCellValue().toString();
	            
	            cell = row.getCell((short)2);
	            userName =  cell.getStringCellValue().toString();
	          /*  
	            cell = row.getCell((short)3);
	            email =  cell.getStringCellValue().toString();
	            
	            cell = row.getCell((short)4);
	            DeptName =  cell.getStringCellValue().toString();
	            
	            cell = row.getCell((short)5);
	            deptId=(int) cell.getNumericCellValue();*/
	            System.out.println("name="+userName+",phone="+phoneNumber+",deptName="+deptName);
	            
	        }
	    }
}

```