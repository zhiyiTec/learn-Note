# 1.先引入jquery
* 1.先使用指令:
> npm install jquery --save-dev
* 2.在webpack.base.conf.js（如果是是开发[dev]环境则在webpack.dev.conf.js；两个文件都在bulid目录下；请一定注意，我在操作的时候就是找错了文件，半天都没有弄对；）中添加如下内容：

``` js
 const webpack = require('webpack')
  plugins:[
new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        }),
]
```
* 3.在main.js进行注册
> import $ from 'jquery'
到此jquery就引入结束了，接着看如何引入传统的bootStrap
# 2.引入BootStrap
* 1.使用指令:
> npm install bootstrap --save-dev
* 2.安装成功后，能够在package.json文件夹中看到bootstrap这个模块。这时候需要在main.js中添加如下内容:
```js
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min'
```
至此bootStrap也引入结束，接下来我们的重点来了，因为BootStrap与VUE有一个专门的设计叫做bootstrap-vue.js，所以我们引入它之后就可以直接使用它们提供的专有样式，比原生的bootStrap要好看很多
* 1.使用指令:
> npm i vue bootstrap-vue bootstrap
* 2.在main.js文件中添加:
```js
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
```
至此所有的引用均都结束了
下面附上 bootStrap-vue的官方api，[点击此处查看](https://bootstrap-vue.js.org/docs/)

