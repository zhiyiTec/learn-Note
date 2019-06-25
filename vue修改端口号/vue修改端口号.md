# 1.首先要更改配置就要先知道配置的主要文件存放在哪个位置，先打开package.json，可以看到下面一段代码:
``` js
"scripts": {
    "dev": "webpack-dev-server --inline --progress --config build/webpack.dev.conf.js",
    "start": "npm run dev",
    "unit": "jest --config test/unit/jest.conf.js --coverage",
    "e2e": "node test/e2e/runner.js",
    "test": "npm run unit && npm run e2e",
    "build": "node build/build.js"
  }
```
由此可知我们启动的环境是dev环境，对应的配置在 build/webpack.dev.conf.js      
# 2.于是我们来到这个文件，可以看到下面这个代码：
```js
const path = require('path')
```
这个path是干嘛的呢，看到名字就应该能立刻反应过来与配置有关
# 3.于是打开打开config目录下的index.js，可以看到下面这串代码：
```js
 dev: {

        // Paths
        assetsSubDirectory: 'static',
        assetsPublicPath: '/',
        proxyTable: {},

        // Various Dev Server settings
        host: 'localhost', // can be overwritten by process.env.HOST
        port: 8090, // can be overwritten by process.env.PORT, if port is in use, a free one will be determined
        autoOpenBrowser: false, //是否build之后自动打开浏览器
        errorOverlay: true,
        notifyOnErrors: true,
        poll: false, // https://webpack.js.org/configuration/dev-server/#devserver-watchoptions-


        /**
         * Source Maps
         */

        // https://webpack.js.org/configuration/devtool/#development
        devtool: 'cheap-module-eval-source-map',

        // If you have problems debugging vue-files in devtools,
        // set this to false - it *may* help
        // https://vue-loader.vuejs.org/en/options.html#cachebusting
        cacheBusting: true,

        cssSourceMap: true
    }
```
在上面这串代码里的port，就是我们要修改的端口号