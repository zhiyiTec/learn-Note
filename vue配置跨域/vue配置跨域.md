# 1，引入 axious,cd 到你的工程

```xml
npm install --save axios vue-axios
```

在 main.js 中加入

```xml
import Vue from 'vue'
import axios from 'axios'
Vue.prototype.$axios = axios
```

注意 Vue.prototype.$axios = axios这句话就决定了你以后使用axious的时候就必须以$axious 这种方式进行
axious 引入结束之后在 config/index.js 文件中加入：

```js
 proxyTable: {
            '/api': {
                target: 'http://localhost:8080', //你要跨域的网址  比如  'http://news.baidu.com',
                // secure: true, // 如果是https接口，需要配置这个参数
                changeOrigin: true, //这个参数是用来回避跨站问题的，配置完之后发请求时会自动修改http header里面的host，但是不会修改别的
                pathRewrite: {
                    '^/api': '/api' //路径的替换规则
                        //这里的配置是正则表达式，以/api开头的将会被用用‘/api’替换掉，假如后台文档的接口是 /api/list/xxx
                        //前端api接口写：axios.get('/api/list/xxx') ， 被处理之后实际访问的是：http://news.baidu.com/api/list/xxx
                }
            }
        },
```

至此跨域的配置就结束了，然后 axious 发请求即可;

```js
 sub:function(){
        var _this=this;

    this.$axios({
    method: 'get',
    url:host+'shiro/login',
    params: {
           userName:_this.userName,
           passWord:_this.passWord
    },
     headers:{
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    }).then((res)=>{
      var st=res.data;
      }else{
        _this.showAlert()
      }
    })
      }
```

至于后端的怎么设置请求头请参考我的另一篇博客，[点击此处](https://blog.csdn.net/zhiyikeji/article/details/84865865)
