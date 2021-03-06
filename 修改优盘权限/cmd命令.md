# 一些 cmd 命令

---

## attrib 命令语法介绍

### 语法介绍

`attrib [{+r | -r}] [{+a | -a}] [{+s | -s}] [{+h | -h}] [[Drive:][Path] FileName] [/s[/d]]`

### 参数介绍

| 参数 |                                作用                                |
| :--: | :----------------------------------------------------------------: |
|  +r  |                          设置只读文件属性                          |
|  -r  |                          清除只读文件属性                          |
|  +a  |                            设置存档属性                            |
|  -a  |                           清除存档属性。                           |
|  +s  |                          设置系统文件属性                          |
|  -s  |                          清除系统文件属性                          |
|  +h  |                          设置隐藏文件属性                          |
|  -h  |                          清除隐藏文件属性                          |
|  /s  | 将 attrib 和任意命令行选项应用到当前目录及其所有子目录中的匹配文件 |
|  /d  |                将 attrib 和任意命令行选项应用到目录                |
|  /?  |                       在命令提示符下显示帮助                       |

> 上述参数中[] 或{}内的参数为可选参数，即可以设置，也可以不设置；
> +号表示添加该属性；－号表示清除该属性；

### 应用举例

**1. 给文件添加单个属性和清除属性**
给 c:\盘中的 MyTxt.txt 文本文件添加隐藏属性
`attrib +h c:\MyTxt.txt`
清除 c:\盘中的 MyTxt.txt 文本文件的隐藏属性
`attrib -h c:\MyTxt.txt`
  
**2. 给文件添加多个属性和清除多个属性**
给 c:\盘中的 MyTxt.txt 文本文件添加只读属性和隐藏属性
`attrib +r +h c:\MyTxt.txt`
清除 c:\盘中的 MyTxt.txt 文本文件的只读属性和隐藏属性
`attrib -r -h c:\MyTxt.txt`
给 c:\盘中的 MyTxt.txt 文本文件添加只读属性、存档、系统和隐藏属性
`attrib +r +a +s +h c:\MyTxt.txt`
清除 c:\盘中的 MyTxt.txt 文本文件的只读属性、存档、系统和隐藏属性
`attrib -r -a -s -h c:\MyTxt.txt`

**3. 给当前目录及所有子目录（文件夹本身）和所有文件添加属性**
给 c:\中的 test 目录及子目标和所有文件添加只读、隐藏属性
`attrib +r +h /s c:\test`
给 c:\中的 test 目录和所包含的文件添加只读、隐藏属性
`attrib +r +h /d c:\test`
