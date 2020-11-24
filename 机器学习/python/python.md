<!-- TOC -->

- [1.python的基本语法元素](#1python的基本语法元素)
  - [1.1.python程序语法元素分析](#11python程序语法元素分析)
    - [1.1.1 命名规则](#111-命名规则)
    - [1.1.2 print函数的格式化](#112-print函数的格式化)
    - [1.1.3 eval函数](#113-eval函数)
- [2.python的基本图形绘制](#2python的基本图形绘制)
  - [2.1 python蟒蛇的绘制](#21-python蟒蛇的绘制)
    - [2.1.1 引入绘图库 turtle](#211-引入绘图库-turtle)
      - [1.turtle空间坐标体系](#1turtle空间坐标体系)
        - [绝对坐标](#绝对坐标)
        - [海龟坐标](#海龟坐标)
      - [2.turtle的角度坐标体系](#2turtle的角度坐标体系)
        - [1.绝对角度](#1绝对角度)
        - [2.海龟角度](#2海龟角度)
  - [2.2 RGB色彩模式](#22-rgb色彩模式)
    - [1.turtle的RGB色彩模式](#1turtle的rgb色彩模式)
- [3.基本数据类型](#3基本数据类型)
  - [1.整数类型](#1整数类型)
    - [四种进制表现形式](#四种进制表现形式)
  - [2.浮点数类型](#2浮点数类型)
    - [浮点数的科学计数法](#浮点数的科学计数法)
  - [3.复数类型](#3复数类型)
  - [4.数值运算操作符](#4数值运算操作符)
    - [基本的运算操作符](#基本的运算操作符)
    - [二元操作符对应的增强赋值操作符](#二元操作符对应的增强赋值操作符)
    - [不同类型的混合运算](#不同类型的混合运算)
  - [5.数值运算函数](#5数值运算函数)
  - [6.字符串类型](#6字符串类型)
    - [1.字符串的表示方法](#1字符串的表示方法)
    - [2.字符串的序号](#2字符串的序号)
      - [1.正向递增序号和反向递减序号](#1正向递增序号和反向递减序号)
      - [2.使用[]获取字符串中的一个或多个字符](#2使用获取字符串中的一个或多个字符)
        - [1.索引](#1索引)
        - [2.切片](#2切片)
    - [3.字符串的特殊字符](#3字符串的特殊字符)
      - [1.转义符](#1转义符)
    - [4.字符串类型及操作](#4字符串类型及操作)
    - [5.字符串的处理函数](#5字符串的处理函数)
    - [6.python字符串的编码方式](#6python字符串的编码方式)
    - [7.字符串的处理方法](#7字符串的处理方法)
      - [1.字符类型及操作](#1字符类型及操作)
      - [2.字符串类型的格式化](#2字符串类型的格式化)
  - [7.time库的使用](#7time库的使用)
    - [1.time库是干嘛的](#1time库是干嘛的)
    - [2.time库的使用：](#2time库的使用)
      - [时间获取](#时间获取)
      - [时间格式化](#时间格式化)
      - [程序计时应用](#程序计时应用)
  - [8.文本进度条](#8文本进度条)
      - [1.多行输出](#1多行输出)
      - [2.单行动态刷新](#2单行动态刷新)
      - [3.文本进度条](#3文本进度条)
- [4.程序的控制结构](#4程序的控制结构)
  - [1.程序的循环结构](#1程序的循环结构)
    - [1.遍历循环](#1遍历循环)
    - [2.无限循环](#2无限循环)
    - [3.循环控制保留字](#3循环控制保留字)
  - [2.random库](#2random库)
    - [1.基本随机数函数](#1基本随机数函数)
    - [2.扩展随机数函数](#2扩展随机数函数)
    - [3.圆周率的计算](#3圆周率的计算)
- [5.函数和代码复用](#5函数和代码复用)
  - [1.函数的定义与使用](#1函数的定义与使用)
    - [1.可变参数传递](#1可变参数传递)
    - [2.函数返回值](#2函数返回值)
    - [3.局部变量和全局变量](#3局部变量和全局变量)
    - [4.lambda函数](#4lambda函数)
  - [2.七段数码管的绘制](#2七段数码管的绘制)
  - [3.代码复用与函数递归](#3代码复用与函数递归)

<!-- /TOC -->
# 1.python的基本语法元素
## 1.1.python程序语法元素分析
### 1.1.1 命名规则
> 大小写字母 数字 下划线 汉字等字符及其组合

注意：命名区分大小写，首字符不能是数字，且不能与保留字相同
保留字：被编程语言内部定义并保留使用的标识符,python内部的保留字如下：
![](1.png)
### 1.1.2 print函数的格式化
``` python
print("转换后的温度为：{:.2f}C".format(F))
```
{:.2f}表示将变量C填充到这个位置时取小数点后两位
![](2.png)
### 1.1.3 eval函数
作用：去掉参数最外侧引号并执行余下语句的函数
![](3.png)
# 2.python的基本图形绘制
## 2.1 python蟒蛇的绘制
### 2.1.1 引入绘图库 turtle
``` python
import turtle
```
```python

```
* 1.turtle.setup
turtle.setup(650, 350, 200, 200)
> 用于设置启动窗体的大小以及位置
650:绘图窗体本身的宽度
350:绘图窗体本身的高度
200:相对于屏幕左上角的x坐标
300:相对于屏幕左上角y轴的坐标
![](4.png)
#### 1.turtle空间坐标体系
##### 绝对坐标
* turtle.goto(x,y)
![](5.png)
下面具体解释一下turtle.goto
![](6.png)
表示从(0,0)->(100,100)->(100,-100)->(-100,100)->(-100,-100)->(-100,100)->(0,0)
##### 海龟坐标
![](7.png)
![](9.png)
#### 2.turtle的角度坐标体系
##### 1.绝对角度
* turtle.seth(angle):
> 只改变海龟的行进方向，但是不行进
> angle为绝对度数
![](10.png)
##### 2.海龟角度
* turtle.left
* turtle.right
![](11.png)
demo:
``` python
import turtle
turtle.left(45)
turtle.fd(150)
turtle.right(135)
turtle.fd(300)
turtle.left(135)
turtle.fd(150)
turtle.done()
```
![](12.png)
## 2.2 RGB色彩模式
![](13.png)
### 1.turtle的RGB色彩模式
默认采用小数值，可切换为整数值
``` python
turtle.colormode(mode)
```
mode:
* 1.0 RGB小数值模式
* 255 RGB整数值模式
# 3.基本数据类型
## 1.整数类型
* power(x,y):计算x的y次方
### 四种进制表现形式
* 10进制：1010，,9。-217
* 二进制：以0b或0B开头：ob010,-0B101
* 八进制：以0o或0O开头：0o123，-0O456
* 十六进制：以0x或0X开头：0x9a，-0X89
## 2.浮点数类型
注意：浮点数间运算存在不确定尾数
![](14.PNG)
由于浮点数运算存在不确定尾数，所以我们可以使用round函数来对小数部分进行截取
* round(x,d):对x进行四舍五入，d是对小数截取的位数
### 浮点数的科学计数法
使用字母e或E作为幂的符号，以10位基数

<font color=#FF0000>  < a> e< b></font>表示$$
a*10^b 
$$
## 3.复数类型
如果 $$x^2=-1$$那么x的值为多少？
* 定义 $$j=\sqrt[2]{-1}$$，以此为基础，构建数学体系
* -a+bj被称为复数，其中a为实部，b为虚部
比如 z=1.23e-4+5.6e+89j
-- 实部 使用z.real获取
-- 虚部 使用z.imag获取
## 4.数值运算操作符
### 基本的运算操作符
![](15.png)
![](16.png)
### 二元操作符对应的增强赋值操作符
![](17.png)
### 不同类型的混合运算
<font color=#FF0000>整数->浮点数->复数</font>
例如 123+4.0=127.0
## 5.数值运算函数
![](18.png)
![](19.png)
![](20.png)
## 6.字符串类型
### 1.字符串的表示方法
* 由一对单引号或双引号表示，但是这种表示方法仅仅能表示单行字符串
* 由一对三单引号或三双引号来表示，可以用来表示多行字符串
注意：由三单引号或三双引号表示的字符串若无变量引用则会被当做注释处理
``` python
a='''
这是多行字符串
你知道吗你
'''
print(a)
```
### 2.字符串的序号
#### 1.正向递增序号和反向递减序号
![](21.png)
#### 2.使用[]获取字符串中的一个或多个字符
##### 1.索引
返回字符串中的单个字符 
``` python
b="请输入带有符号的温度值"
print(b[0])
print("请输入带有符号的温度值"[0])
```
输入结果：![](22.png)
##### 2.切片
返回字符串中的一段字符子串
``` python
b="请输入带有符号的温度值"
print(b[0:-1])
print("请输入带有符号的温度值"[1:3])
```
输出结果：![](23.png)
**字符串切片的高级用法:**
* <字符串>[M:N],<font color=#FF0000>  M缺失表示至开头 </font>，<font color=#808080>  N缺失表示至结尾 </font>   
```python
c="零一二三四五六七八九十"
print(c[:3])
```
输出结果：![](24.png)
* <字符串>[M:N:K] 根据步长K对字符串进行切片
``` python
c="零一二三四五六七八九十"
print(c[1:8:2])
```
输出结果：![](25.png)
表示从第一位开始到第八位前结束，每次增加2的步长
字符串逆序：<字符串>[::-1] 表示从开头至结尾，步长为-1表示从后往前逐个的取出数据
``` python
c="零一二三四五六七八九十"
d=c[::-1]
print(d)
```
输出结果：![](26.png)
### 3.字符串的特殊字符
#### 1.转义符
\
* 1.转义符表示特定字符的本意
``` python
e = "这里有个双引号\""
print(e)
```
输出结果：![](27.png)
* 2.转义符形成一些组合，表达一些不可打印的含义

| 转义符 | 表示含义               |
| ------ | ---------------------- |
| \b     | 回退                   |
| \n     | 换行                   |
| \r     | 回车（光标移到本行首） |
### 4.字符串类型及操作
| 操作符及使用 | 描述                                  |
| ------------ | ------------------------------------- |
| x+y          | 连接两个字符串x和y                    |
| n*x 或 x*n   | 复制n次子字符串                       |
| x in s       | 如果x是s的子串，返回true否则返回false |
``` python
weekStr="星期一星期二星期三星期四星期五星期六星期日"
weekId=eval(input("请输入星期数字（1-7）："))
pos=(weekId-1)*3
print(weekStr[pos:pos+3])
```
或
``` python
weekStr="一二三四五六日"
weekId=eval(input("请输入星期数字（1-7）："))
print("星期"+weekStr[weekId-1])
```
输出结果：![](28.png)
### 5.字符串的处理函数
| 函数及使用     | 描述                                                                                 |
| -------------- | ------------------------------------------------------------------------------------ |
| len(x)         | 长度，返回字符串x的长度，len("123456")—结果为6                                       |
| str(x)         | 任意类型的x对应的字符串的形式，str(3.14)—对应结果为1.23 str([1,2]) 对应结果为"[1,2]" |
| hex(x)或oct(x) | 整数x的十六进制或八进制小写形式字符串 hex(425)结果为"0x1a9" oct(425)结果为"0o651"    |
| chr(x)         | x为unicode编码，返回其对应的字符                                                     |
| ord(x)         | x为字符，返回对应的unicode编码                                                       |
![](29.png)
### 6.python字符串的编码方式
* 统一字符编码，即覆盖几乎所有字符的编码方式
* 从0到1114111(Ox10FFFF)空间，每个编码对应一个字符
* Python字符串中每个字符都是Unicode编码字符
``` python
for i in range(12):
    print(chr(9800+i))
```
### 7.字符串的处理方法
#### 1.字符类型及操作
| 方法及使用                   | 描述                                                                                                     |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- |
| str.lower()或 str.upper()    | 返回字符串的副本，全部字符小写/大写 "AbCdEfGh". lower()结果为"abcdefgh"                                  |
| str.split(sep=None)          | 返回一个列表，由str根据sep被分隔的部分组成 "A,B,C".split(",")结果为['A','B' , 'C']                       |
| str.count(sub)               | 返回子串sub在str中出现的次数  "a apple a day" .count("a") 结果为4                                        |
| str.replace(old, new)        | 返回字符串str副本，所有old子串被替换为new   "python".replace(""n" , "n123.io")结果为"python123.io"       |
| str.center(width[,fillchar]) | 字符串str根据宽度width居中，fillchar可选"python".center(20,"=")结果为 '=======python======='             |
| str.strip(chars)             | 从str中去掉在其左侧和右侧chars中列出的字符 "= python= ".strip(" =np")结果为"ytho"                        |
| str.join(iter)               | 在iter变量除最后元素外每个元素后增加一个str   " , ".join("12345")结果为 "1,2,3,4,5”#主要用于字符串分隔等 |
#### 2.字符串类型的格式化
格式化是对字符串进行格式表达的方式
<模板字符串>.format(<逗号分隔的参数>).
![](30.png)
![](31.png)
![](32.png)
## 7.time库的使用
### 1.time库是干嘛的
time库是Python中处理时间的标准库
* 计算机时间的表达
* 提供获取系统时间并格式化输出功能
* 提供系统级精确计时功能，用于程序性能分析
### 2.time库的使用：
``` python
import time
time.<b>()
```
time库包括三类函数：
* 时间获取: time() ctime() gmtime()
* 时间格式化: strftime() strptime(）
* 程序计时: sleep(), perf_counter()
#### 时间获取
| 函数     | 描述                                                                                                                                                                                   |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| time()   | 获取当前时间戳，即计算机内部时间值，浮点数  <br>>>>time.time()<br>输入结果：1516939876.6022282                                                                                         |
| ctime()  | 获取当前时间并以易读方式表示，返回字符串 <br> >>>time.ctime()<br> 输出结果：'Fri Jan 26 12:11:16 2018'                                                                                 |
| gmtime() | 获取当前时间，表示为计算机可处理的时间格式<br> >>time.gmtime()<br> time.struct_time(tm_year=2018，tm_mon=1,tm_mday=26,tm_hour=4, tm_min=11, tm_sec=16,tm_wday=4,tm_yday=26,tm_isdst=0) |
#### 时间格式化
![](33.png)
| 函数               | 描述                                                                                                                                                                                                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| strftime(tpl, ts)  | tpl是格式化模板字符串，用来定义输出效果ts是计算机内部时间类型变量<br>>>>t = time.gmtime()<br>>>>time.strftime("%Y-%m-%d %H:%M:%S",t)<br>'2018-01-26 12:55:20'                                                                                                                   |
| strptime(str, tpl) | str是字符串形式的时间值<br>tpl是格式化模板字符串，用来定义输入效果<br>>>>timeStr = '2018-01-26 12:55:20'<br>>>>time.strptime(timeStr，"%Y-%m-%d %H:%M:%S")<br>time.struct_time(tm_year=2018,tm_mon=1,tm_mday=26,tm_hour=4, tm_min=11,tm_sec=16,tm_wday=4, tm_yday=26,m_isdst=0) |
![](34.png)
![](35.png)
#### 程序计时应用
程序计时是指测量起止动作所经历时间的过程
* 测量时间:time.perf_counter()
* 产生时间：time.sleep()

| 函数           | 描述                                                                                                                                                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| perf_counter() | 返回一个CPU级别的精确时间计数值，单位为秒<br>由于这个计数值起点不确定，连续调用差值才有意义<br>>>>start = time.perf_counter()<br> 318.66599499718114<br>>>>end = time.perf_counter()<br>341.3905185375658<br>>>>end - start<br>22.724523540384666 |
| sleep(s)       | s拟休眠的时间，单位是秒，可以是浮点数<br>>>>def wait():<br>time.sleep(3.3)<br>>>>wait() #程序将等待3.3秒后再退出                                                                                                                                  |
## 8.文本进度条
#### 1.多行输出
``` python
import time
scale = 10
print("---------开始执行---------")
for i in range(scale + 1):
    a = '*' * i
    b = '.' * (scale - i)
    c = (i / scale) * 100
    print("{:^3.0f}%[{}->{}]".format(c, a, b))
    time.sleep(0.1)
print("---------执行结束---------")

```
输出结果：![](36.png)
#### 2.单行动态刷新
* 刷新的本质是：用后打印的字符覆盖之前的字符
* 不能换行：print()需要被控制
* 要能回退：打印之后的光标回到之前的位置 \r

``` python
import time
for i in range(101):
    print("\r{:3}%".format(i), end="")
    time.sleep(0.1)
```
输出结果：![](37.png)
#### 3.文本进度条
``` python
import time
scale = 50
print("执行开始".center(scale // 2, "-"))
start = time.perf_counter()
for i in range(scale + 1):
    a = "*" * i
    b = "." * (scale - 1)
    c = (i / scale) * 100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end="")
    time.sleep(0.1)
print("\n" + "执行结果".center(scale // 2, "-"))
```
输出结果：![](38.png)
# 4.程序的控制结构
## 1.程序的循环结构
### 1.遍历循环
for <循环变量> in <遍历结构>:
    <语句块>
``` python
for i in range(9):
    print(i)
```
输出结果：![](39.png)
``` python
for i in range(1,6):
    print(i)
```
输出结果：![](40.png)
``` python
for i in range(1,6,2):
    print(i)
```
输出结果：![](41.png)
* 字符串循环
``` python
str = "python123"
for c in str:
    print(c, end="#")
```
输出结果：![](42.png)
### 2.无限循环
while <条件>:
    <语句块>
``` python
a = 3
while a > 0:
    a-=1
    print(a)

```
输出结果：![](43.png)
### 3.循环控制保留字
* break 跳出并结束当前整个循环，执行循环后的语句
注意:break只能跳出最内层循环
``` python
str = "PYTHON"
for c in str:
    if c == "T":
        break
    print(c, end=" ")
```
输出结果：![](45.png)
* continue 结束当次循环，继续执行后续次数的循环
``` python
str = "PYTHON"
for c in str:
    if c == "T":
        continue
    print(c, end=" ")
```
输出结果：![](44.png)
## 2.random库
random库是使用随机数的python的标准库
使用 import random进行引入
### 1.基本随机数函数
| 函数           | 描述                                                                                                                                                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|seed(a=None) | 初始化给定的随机数种子，默认为当前系统时间<br>>>>random.seed(10)#产生种子10对应的序列<br>|
| random()      | 生成一个[0.0,1.0)之间的随机小数<br>>>>random.random()<br> 0.5714025946899135|

``` python
import random
random.seed(10)
print(random.random())
```
输出结果：![](46.png)
### 2.扩展随机数函数
| 函数           | 描述                                                                                                                                                                                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|randint(a, b)| 生成一个[a, b]之间的整数<br>>>>random.randint(10，100)<br>64|
|randrange(m, n[, k])| 生成一个[m, n)之间以k为步长的随机<br>>>>random.randrange(10，100，10)<br>80|
|getrandbits(k)| 生成一个k比特长的随机整数<br>>>>random.getrandbits(16)<br>37885|
|uniform(a, b)| 生成一个[a, b]之间的随机小数<br>>>>random.uniform(10，100)<br>13.096321648808136|
|choice(seq)| 从序列seq中随机选择一个元素<br>>>>random.choice([1,2,3,4,5,6,7,8,9])<br>8|
|shuffle(seq)|将序列seq中元素随机排列，返回打乱后的序列<br>>>>5=[1,2,3,4,5,6,7,8,9];random.shuffle(s);print(s)<br>[3，5，8，9，6， 1，2，7，4]|
### 3.圆周率的计算
``` python
import random
import time
DARTS = 1000 * 1000
hits = 0.0  # 表示命中的数量
start = time.perf_counter()
for i in range(1, DARTS + 1):
    x = random.random()
    y = random.random()
    dist = pow(x ** 2 + y ** 2, 0.5)
    if dist <= 1.0:
        hits += 1
pi = 4 * (hits / DARTS)
print("圆周率的值为：{}".format(pi))
print("运行时间：{:.5f}".format(time.perf_counter() - start))
```
输出结果：![](47.png)
# 5.函数和代码复用
## 1.函数的定义与使用
### 1.可变参数传递
``` python
def fact(n, *b):
    s = 1
    for i in range(1, n + 1):
        s *= i
    for item in b:
        s *= item
    return s
result = fact(10, 1, 2, 3)
print(result)
```
输出结果：![](48.png)
### 2.函数返回值
函数可以返回0个或多个结果
``` python
def fact(n, m):
    s = 1
    for i in range(1, n + 1):
        s *= i
    return s // m, n, m
print(fact(5, 2))
a, b, c = fact(5, 2)
print("a:{},b:{},c:{}".format(a, b, c))
```
输出结果：![](49.png)
### 3.局部变量和全局变量
在函数内部在不使用global保留字声明的情况下所定义的变量都是局部变量
### 4.lambda函数
lambda函数是一种匿名函数，即没有名字的函数
<函数名>=lambda <参数>:<表达式>
等价于
def <函数名>(<参数>):
  <函数体>
  return <返回值>
 ``` python
f = lambda x, y: x + y
print(f(10, 15))
g=lambda :"lambda函数"
print(g())
 ```
## 2.七段数码管的绘制
 ``` python
import turtle
import time


# 绘制数码管间隔
def drawGap():
    turtle.penup()
    turtle.fd(5)


# 绘制单段数码管
def drawLine(draw):
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    drawGap()
    turtle.right(90)


# date为日期，格式为'%y-%m=%d+'
def drawDate(date):
    turtle.pencolor("red")
    for i in date:
        if i == "-":
            turtle.write('年', font=("Arial", 18, "normal"))
            turtle.pencolor("green")
            turtle.fd(40)
        elif i == "=":
            turtle.write("月", font=("Arial", 18, "normal"))
            turtle.pencolor("blue")
            turtle.fd(40)
        elif i == "+":
            turtle.write("日", font=("Arial", 18, "normal"))
        else:
            drawDigit(eval(i))


# 根据数字绘制七段数码管
def drawDigit(digit):
    drawLine(True) if digit in [2, 3, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 1, 3, 4, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 2, 3, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 2, 6, 8] else drawLine(False)
    turtle.left(90)
    drawLine(True) if digit in [0, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 2, 3, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if digit in [0, 1, 2, 3, 4, 7, 8, 9] else drawLine(False)
    turtle.left(180)
    turtle.penup()  # 为绘制后续数字
    turtle.fd(20)  # 为绘制后续数字确定位置


def main():
    turtle.setup(800, 350, 200, 200)
    turtle.penup()
    turtle.fd(-300)
    turtle.pensize(5)
    drawDate(time.strftime('%Y-%m=%d+', time.gmtime()))
    turtle.hideturtle()
    turtle.done()


main()

 ```
 输出结果：![](50.png)
 ## 3.代码复用与函数递归
 