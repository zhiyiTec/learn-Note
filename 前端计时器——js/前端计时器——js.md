# 里面用到了两个js函数：
### setTimeout   
#### 语法：
```html
setTimeout(code,millisec)
```
参数|描述                   
:----|:----:|----:                  
code|必需。要调用的函数后要执行的 JavaScript 代码串               
millisec|必需。在执行代码前需等待的毫秒数
#### 提示和注释:
> setTimeout() 只执行 code 一次。如果要多次调用，请使用 setInterval() 或者让 code 自身再次调用 setTimeout()。
### clearTimeout   
#### 语法：
```html
clearTimeout(id_of_settimeout)
```
参数|描述                   
:----|:----:|----:                  
id_of_settimeout|由 setTimeout() 返回的 ID 值。该值标识要取消的延迟执行代码块。               
方法1：
```html
<!DOCTYPE html>
<html lang="en" ng-app="myApp">
<head>
    <meta charset="UTF-8">
    <title>demo</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body ng-controller="myCtrl">
    <div class="box">
        <h2>confirm确认框</h2>
        <button type="button" class="btn btn-success" id="button">点我</button>
    </div>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdn.bootcss.com/bootbox.js/4.4.0/bootbox.js"></script>
    <script>
        $("#button").click(function() {
            count(3)
        });
        var count = (function() {
            var timer;
            var i = 0;
            function change(tar) {

                i++;
                if (i >= 3) {
                    alert("you win")
                }
                console.log(i);
                if (i === tar) {
                    clearTimeout(timer);
                    return false;
                }
                timer = setTimeout(function() {
                    change(tar)
                }, 1000)

            }
            return change;
        })()
    </script>
</body>
</html>
</script>
</body>
</html>
```
方法2：
```html
<html>
<head>
<script type="text/javascript">
var c=0
var t
function timedCount()
{
document.getElementById('txt').value=c
c=c+1
t=setTimeout("timedCount()",1000)
if(c>=3){
alert("a")}
}
function stopCount()
{
clearTimeout(t)
}
</script>
</head>
<body>
<form>
<input type="button" value="开始计时！" onClick="timedCount()">
<input type="text" id="txt">
<input type="button" value="停止计时！" onClick="stopCount()">
</form>
<p>
请点击上面的“开始计时”按钮。输入框会从 0 开始一直进行计时。点击“停止计时”可停止计时。
</p>
</body>
</html>

```