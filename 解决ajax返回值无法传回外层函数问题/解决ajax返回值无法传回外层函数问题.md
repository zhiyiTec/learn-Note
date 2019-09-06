# 1.先解释一下原因

### 由于 ajax 是异步刷新，不会对 ajax 里面执行的任务进行任何阻塞，所以如果我们直接 return data，他会在未出结果之前把值传给函数，对此有一个特别简单的方法解决

# 2.具体解决办法：

## 2.1 先在函数内定义一个全局变量

```js
var result;
```

## 2.2 在 ajax 里面添加

> async:false  
> 表示执行完代码之后在返回结果

# 具体代码如下：

```js
function test() {
  var result;
  $.ajax({
    url: "localhost:8080....",
    data: "测试",
    type: "get",
    async: false, //此处必须要有这句话，否则任然会传值失败
    success: function(data) {
      result = data;
    }
  });
  return result;
}
```

-------------------------到此结束---------------------------------------
