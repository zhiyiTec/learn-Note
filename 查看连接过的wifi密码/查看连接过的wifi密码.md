# 1.先找到曾经连接过哪些wifi，找到他们的名字:
```
netsh wlan show profiles
```
# 2.接着使用这个指令就可以测试出wifi的密码:
```
netsh wlan show profile name="wifi的名字" key=clear
```
比如：
```
netsh wlan show profile name="360Free" key=clear
```
找到安全设置中的关键内容，就是我们要找的wifi密码