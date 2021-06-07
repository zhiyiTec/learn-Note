当我们提交代码提示husky > pre-commit hook failed (add --no-verify to bypass)时，是由于pre-commit(客户端)它会在Git键入提交信息前运行做代码风格检查。如果代码不符合相应规则，则报错。导致无法提交，解决方案如下:
* 1.进入项目文件夹⁨/.git⁩/hooks⁩文件夹下
* 2.删除pre-commit文件