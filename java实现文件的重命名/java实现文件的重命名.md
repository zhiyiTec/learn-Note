# 使用java i/o流读取文件夹中的所有的文件，并实现按照指定的规则进行重命名
# 1.直接建一个util类，来进行创建两个重命名的方法:
```java
package reName;

import java.io.File;

public class util {
	/**
	 * 用于将文件名按照指定数字往后排
	 * @param startNum
	 * @param url
	 */
	public static void sort(int startNum,String url) {
		 File file = new File(url);
		 File[] list = file.listFiles();
		 String newName=null;
		// 如果目录下文件存在
	        if (file.exists() && file.isDirectory())
	        {
	            for (int i = 0; i < list.length; i++)
	            {
	                //取文件名子存入name中
	                String name = list[i].getName();
	                int lo=name.indexOf(".");
	               String lastName=name.substring(lo,name.length());
	               String forNeName=String.valueOf(startNum);
	               startNum++;
	                //重命名
	               newName=forNeName+lastName;
	                File dest = new File(url + "/" + newName);
	                list[i].renameTo(dest);
	                System.out.println(dest.getName());
	            }
	        }
	}
	/**
	 * 用于将文件名编制为七位，不够的用0来补充
	 * @param url
	 */
	public static void reName(String url) {
		 File file = new File(url);
		 File[] list = file.listFiles();
		 String newName=null;
		
		// 如果目录下文件存在
	        if (file.exists() && file.isDirectory())
	        {
	            for (int i = 0; i < list.length; i++)
	            {
	                //取文件名子存入name中
	                String name = list[i].getName();
	                int lo=name.indexOf(".");
	                
	               String strName=name.substring(0,lo);
	               String lastName=name.substring(lo,name.length());
	              // System.out.println(lastName);
	               int nameLength=strName.length();
	               System.out.println("nameLength="+nameLength);
	                if(nameLength<7) {
	                	String zeString="";
	                	for(int j=0;j<7-nameLength;j++) {
	                		zeString+="0";
	                		System.out.print(zeString);
	                	}
	                	newName=zeString+strName+lastName;
	                }else {
	                	 newName=name;
	                }
	                
	                //重命名
	                File dest = new File(url + "/" + newName);
	                list[i].renameTo(dest);
	                System.out.println(dest.getName());
	            }
	        }
	}
}
```
# 2.在建立一个main函数进行测试，当然也可以进行单元测试：
```java
package reName;

public class Main_ReName {
	public static void main(String[] args) {
		String url="C:\\Users\\17732\\Desktop\\2019.1.16\\切图\\01-16_11_01_1547610990";
		int startNum=4066;//将文件名从4066开始命名
		util.sort(startNum, url);//先将文件名换为4066,4067,4068.....
		util.reName(url);//在将文件名指定为7位，如果不够7位就在文件名前面补充0
	}
}
```
> 本人已经使用过，无任何异常，bug，可以放心使用，而且排序之后文件顺序不会改变