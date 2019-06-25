# 使用 elementui 与不使用 elementui 来监听键盘事件的方式不同:

- 使用 elementui 的:
  > <el-input v-model="id" placeholder="ID" @keyup.enter.native="handleClick"></el-input>
  > 否则的话就会出现大问题
  > 下面通过数据的双向绑定来实现动态的监听 input 的变化，并作出相应的判断:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Vue 测试实例 - 菜鸟教程(runoob.com)</title>
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.8/dist/vue.js"></script>
    <!-- 引入样式 -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/element-ui/lib/theme-chalk/index.css"
    />
    <!-- 引入组件库 -->
    <script src="https://unpkg.com/element-ui/lib/index.js"></script>
  </head>

  <body>
    <div id="vue_det">
      <el-form-item label="姓名" :label-width="formLabelWidth">
        <el-input
          v-model="form.name"
          autocomplete="off"
          @keyup.native="keyup()"
        ></el-input>
      </el-form-item>
    </div>
    <script type="text/javascript">
      var vm = new Vue({
        el: "#vue_det",
        data: {
          form: {
            name: ""
          }
        },

        methods: {
          keyup() {
            if (this.judgeNull(this.form.name)) {
              alert("输入的数据不能为空");
            }
          },

          //判空
          judgeNull(str) {
            if (str == "") return true;
            var regu = "^[ ]+$";
            var re = new RegExp(regu);
            return re.test(str);
          }
        }
      });
    </script>
  </body>
</html>
```

代码可以直接新建一个 html 文件然后拷贝过来尝试一下，其中 keyup()方法里面就是你想在输入值时想做怎么样的处理
