# 1.首先安装两个必要的插件:

- eslint
- Vetur

# 2.配置 eslint,按如下步骤打开配置文件:

> 文件->首选项->设置，在搜索设置中输入 eslint,如图:
> ![](1.png)
> 点击图中红色勾选的按钮之后,来到下图所示的位置:
> ![](2.png)
> 点击红色勾选的设置:
> 进行如下设置:

```json
{
  "workbench.iconTheme": "material-icon-theme",
  "window.zoomLevel": -1,
  "editor.accessibilitySupport": "on",
  "editor.fontSize": 18,
  "editor.formatOnPaste": true,
  "editor.formatOnSave": true,
  "eslint.autoFixOnSave": true,
  "vetur.format.defaultFormatter.js": "none",
  "vetur.format.defaultFormatter.html": "js-beautify-html",
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    {
      "language": "vue",
      "autoFix": true
    },
    "html",
    "vue"
  ],
  "eslint.options": {
    "plugins": ["html"]
  },
  "vetur.validation.template": false,
  "editor.largeFileOptimizations": false,
  "workbench.colorTheme": "Tiny Light",
  "powermode.enabled": true
}
```
