# 1.安装
### 目前没有时间总结，[点击此处查看](http://www.runoob.com/vue2/vue-install.html)
# 2.Vue.js 起步
### 在本节会告诉你在compont中编写的组件，怎么使用，主要分四步走:
* 1.在component中编写对应的组件
* 2.在App.vue中导入这个组件，比如你第一步编写的组件名叫：Hellow.vue,则在<script></script>中导入：
> import Hello from './components/Hello'
* 3.在App.vue的 components里面进行注册:
```js
export default {
  name: 'app',
  components: {
    Hello
  }
}
```

* 4.在<templte></templte>中进行使用:
```js
<template>
  <div id="app">
   
    <hello></hello>
  </div>
</template>
```
注意:一个template中只能有一个根组件，也就是所有的内容只能包裹在一个div中
# 3.Vue.js 模板语法
### 1.v-model 指令:
> 用来在 input、select、text、checkbox、radio 等表单控件元素上创建双向数据绑定，根据表单上的值，自动更新绑定的元素的值。
```vue
<template>
  <div class="TemplateSyntax">
  <h1>v-model</h1>
  <p style="color:red;font-size:20px;">仔细观看后面的内容是否有变化:</p><h3>{{msg}}</h3>
  <input type="text" v-model='msg'/>输入数据来检测实现数据的双向绑定
  </div>
</template>

<script>
export default {    
  name: 'TemplateSyntax',
  data () {
    return {
      msg: 'TemplateSyntax',
    }
  }
}   
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

```
### 2. v-on :
> 按钮的事件我们可以使用 v-on 监听事件，并对用户的输入进行响应。
```vue
<template>
  <div class="TemplateSyntax">
  <h1>字符反转</h1>
   <input type="text" v-model='msg1'/>输入数据
   <button v-on:click="reverseMessage()">点击反转</button>
  </div>
</template>

<script>
export default {    
  name: 'TemplateSyntax',
  data () {
    return {
      
      msg1:"",
    }
  },
  methods:{
      reverseMessage:function(){
          this.msg1= this.msg1.split('').reverse().join('')
      },
  },
}   
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

```
### 3.过滤器
#### Vue.js 允许你自定义过滤器，被用作一些常见的文本格式化。由"管道符"指示, 格式如下
> {{ message | capitalize }}
其中第一个message是参数，capitalize是你自己定义的规则
```vue
<template>
  <div class="TemplateSyntax">
  
    <h1>过滤器</h1>
    {{msg2|capitalize|sub}
  </div>
</template>

<script>
export default {    
  name: 'TemplateSyntax',
  data () {
    return {
   
      msg2:"abcdefghi",
      
    }
  },
  methods:{
     
  },
  filters:{
      capitalize:function(value){
          if(value){
              return value.charAt(0).toUpperCase() + value.slice(1)
          }else{
              return ""
          }
      },
      sub:function(value){
          if(value&&value.length>=4){
              return value.substring(0,4);
          }else if(value){
              return value
          }else{
              return ""
          }
      },
  }
}   
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

```
### 4.v-bind,v-on的简写：
* 1.v-bind
```vue
<!-- 完整语法 -->
<a v-bind:href="url"></a>
<!-- 缩写 -->
<a :href="url"></a>
```
* 2.v-on
```vue
<!-- 完整语法 -->
<a v-on:click="doSomething"></a>
<!-- 缩写 -->
<a @click="doSomething"></a>
```
# 4.Vue.js 条件与循环
### 1.if else
直接看例子吧
```vue
<template>
  <div class="ConditionAndCycle">
      <input type="checkbox" v-model="sig">点击让下面这句话
      <span v-if="sig">{{msg}}</span>
      <span v-else>{{msg2}}</span>
  <div v-if='sig'>
      <p>我出来了</p>
  </div>
  <div v-else>
      <p>我消失了</p>
  </div>
  </div>
  
</template>

<script>
export default {
  name: 'ConditionAndCycle',
  data () {
    return {
      msg: '消失',
       msg2: '显示',
      sig:true,
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

```
### 2.v-show 指令来根据条件展示元素：
```vue
<template>
  <div class="ConditionAndCycle">
     
  <h1>v-show</h1>
  <input type="checkbox" v-model="sig">点击让下面这句话
   <span v-if="sig">{{msg}}</span>
      <span v-else>{{msg2}}</span>
  <h1 v-show="sig">Hello!</h1>
  </div>
  
</template>

<script>
export default {
  name: 'ConditionAndCycle',
  data () {
    return {
      msg: '消失',
       msg2: '显示',
      sig:true,
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

```
# 5.循环语句
> v-for 指令需要以 site in sites 形式的特殊语法， sites 是源数据数组并且 site 是数组元素迭代的别名。
注意: v-for只支持 Array | Object | number | string
```vue
<template>
  <div class="Loop">
    <h1>遍历数组</h1>
    <ul  v-for="a in array">
      <li><input type="radio" value='s' id='a'>A{{a}}</li>
    </ul>
      <h1>遍历键值数组</h1>
     <ul  v-for="a1 in arr1">
      <li>{{a1}}</li>
    </ul>
   
  </div>
  
</template>

<script>
var arr=new Array(1,2,3,4,5,6);
var arr1={1:'a',2:'b',3:'c'};

export default {
  name: 'Loop',
  data () {
    return {
      array:arr,
      arr1:arr1,
      
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul li{
list-style-type:none;
}
</style>

```
