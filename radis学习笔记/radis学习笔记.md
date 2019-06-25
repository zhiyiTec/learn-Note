# 1.安装使用radis
### 1.下载安装：
* 1.下载地址：https://github.com/MSOpenTech/redis/releases
![](1.jpg)
* 2.配置全局路径：
> 在path中加入解压后的文件夹目录
* 3.radis牛刀小试：
> 打开一个 cmd 窗口 使用 cd 命令切换目录运行(注意如果第二步已经加入了环境变量中，就无需cd到该目录)：
> ```
> redis-server.exe redis.windows.conf
> ```
* 4.这时候另启一个 cmd 窗口，原来的不要关闭，不然就无法访问服务端了。切换到 redis 目录下运行(注意如果第二步已经加入了环境变量中，就无需cd到该目录):
```
redis-cli.exe -h 127.0.0.1 -p 6379
```
* 4.设置键值对（key——value）:
```
set myKey abc//用于设置键值
get myKey//根据键取出值
```
# 2.redis配置：
* 1.获取redis配置：
> config get config_set_name
例如：查看日志级别：
> config get loglevel
* 2.设置redis配置：
>  CONFIG SET CONFIG_SETTING_NAME NEW_CONFIG_VALUE   

比如设置日志级别：
> config set loglevel 'notice'   
> 此处将日志级别设置为notice
# 3.redis数据类型
* 1.String字符串
> 一个 key 对应一个 value,string 类型是二进制安全的。意思是 redis 的 string 可以包含任何数据。比如jpg图片或者序列化的对象。string 类型是 Redis 最基本的数据类型，string 类型的值最大能存储 512MB。
```
set name 'redis'
get name //此处就可以得到name对应的value值
```
* 2.Hash
> Redis hash 是一个键值(key=>value)对集合。Redis hash 是一个 string 类型的 field 和 value 的映射表，hash 特别适合用于存储对象。
```
HMSET myhash field1 "Hello" field2 "World" field "I love You"//此处用于设置值
HGET myhash field1//此处用于得到field1对应的值
```
> 实例中我们使用了 Redis HMSET, HGET 命令，HMSET 设置了两个 field=>value 对, HGET 获取对应 field 对应的 value。每个 hash 可以存储 232 -1 键值对（40多亿）。
* 3.List（列表）
Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）。（输出顺序为先入先出）
```
lpush runoob(这个是列表名) redis（这个是你要插入的元素）//lpush用于向队列中插入元素
lrange runoob 0 10//lrange用于输出列表中的元素，此处用于输出列表中的0——10号所有的元素
```
* 4.Set（集合）
Redis的Set是string类型的无序集合。集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。        
sadd 命令添加一个 string 元素到 key 对应的 set 集合中，成功返回1，如果元素已经在集合中返回 0，如果 key 对应的 set 不存在则返回错误。
```
sadd runoob redis
sadd runoob mongodb
sadd runoob rabitmq
sadd runoob rabitmq
//此处之上都是向set集合runoob中插入元素
smembers runoob//此处是用于输出遍历元素，其中输出的顺序为无序，尤其要注意的是set集合中元素不可以重复，最新的元素会把原来相同的元素覆盖掉
```
* 5.zset(sorted set：有序集合)
```
redis 127.0.0.1:6379> zadd runoob 0 redis
(integer) 1
redis 127.0.0.1:6379> zadd runoob 0 mongodb
(integer) 1
redis 127.0.0.1:6379> zadd runoob 0 rabitmq
(integer) 1
redis 127.0.0.1:6379> zadd runoob 0 rabitmq
(integer) 0
redis 127.0.0.1:6379> > ZRANGEBYSCORE runoob 0 1000
```
# 4.Redis 命令
* 1.启动redis服务，在cmd中输入：
```
redis-server.exe//前提是已经配置好了redis的全局变量
```
* 2.在打开一个cmd，输入：
```
redis-cli//用于启动客户端
```
如果需要在远程 redis 服务上执行命令，同样我们使用的也是 redis-cli 命令。
```
redis-cli -h host -p port -a password
比如：redis-cli -h 127.0.0.1 -p 6379 -a "mypass"
```
注意：有时候会有中文乱码。要在 redis-cli 后面加上 --raw
```
redis-cli --raw
```
# 5.Redis 键(key)
Redis 键命令用于管理 redis 的键。
命令：COMMAND KEY_NAME
```
SET runoobkey redis//用于设置键（String 类型）
DEL runoobkey//删除键（DEL 是一个命令， runoobkey 是一个键。 如果键被删除成功，命令执行后输出 (integer) 1，否则将输出 (integer) 0）
```

序号|命令|描述                        
:----|:----:|----:                     
1|del key|该命令用于在 key 存在时删除 key。如果键被删除成功，命令执行后输出 (integer) 1，否则将输出 (integer) 0
2|dump key|序列化给定 key ，并返回被序列化的值。     
3|exists key|检查给定 key 是否存在。     
4|expire key seconds|为给定 key 设置过期时间，以秒计。     
5|expireat key timestamp|EXPIREAT 的作用和 EXPIRE 类似，都用于为 key 设置过期时间。 不同在于 EXPIREAT 命令接受的时间参数是 UNIX 时间戳(unix timestamp)。                  
6|PEXPIRE key milliseconds |设置 key 的过期时间以毫秒计。     
7|PEXPIREAT key milliseconds-timestamp | 设置 key 过期时间的时间戳(unix timestamp) 以毫秒计    
8|KEYS pattern |查找所有符合给定模式( pattern)的 key 。     
9| MOVE key db |将当前数据库的 key 移动到给定的数据库 db 当中。
10|PERSIST key |  移除 key 的过期时间，key 将持久保持。   
11|	PTTL key | 以毫秒为单位返回 key 的剩余的过期时间。    
12|	TTL key |     以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)。
13|RANDOMKEY |  从当前数据库中随机返回一个 key 。   
14|RENAME key newkey|修改 key 的名称     
15|RENAMENX key newkey | 仅当 newkey 不存在时，将 key 改名为 newkey 。    
16|TYPE key | 返回 key 所储存的值的类型。    
# 6.Redis 字符串(String)
Redis 字符串数据类型的相关命令用于管理 redis 字符串值，基本语法如下：
```
 COMMAND KEY_NAME
```
比如：
```
SET runoobkey redis//设置键runoobkey 对应的值为redis
GET runoobkey//获取键runoobkey对应的值
```
### 常用的 redis 字符串命令：
![](2.png)
![](3.png)
![](4.png)
# 7.Redis 哈希(Hash)
Redis hash 是一个string类型的field和value的映射表，hash特别适合用于存储对象。Redis 中每个 hash 可以存储 232 - 1 键值对（40多亿）。
举一个实例：
```
127.0.0.1:6379>  HMSET runoobkey name "redis tutorial" description "redis basic commands for caching" likes 20 visitors 23000
OK
127.0.0.1:6379>  HGETALL runoobkey
1) "name"
2) "redis tutorial"
3) "description"
4) "redis basic commands for caching"
5) "likes"
6) "20"
7) "visitors"
8) "23000"
``` 
###  redis hash 基本的相关命令：
![](5.png)
![](6.png)
# 8.Redis 列表(List)
Redis列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）一个列表最多可以包含 232 - 1 个元素 (4294967295, 每个列表超过40亿个元素)。
下面举一个小例子：
```
redis 127.0.0.1:6379> LPUSH runoobkey redis
(integer) 1
redis 127.0.0.1:6379> LPUSH runoobkey mongodb
(integer) 2
redis 127.0.0.1:6379> LPUSH runoobkey mysql
(integer) 3
redis 127.0.0.1:6379> LRANGE runoobkey 0 10

1) "mysql"
2) "mongodb"
3) "redis"
```
在以上实例中我们使用了 LPUSH 将三个值插入了名为 runoobkey 的列表当中。      
列表相关的基本命令：
![](7.png)
![](8.png)
# 10.Redis 集合(Set)
Redis 的 Set 是 String 类型的无序集合。集合成员是唯一的，这就意味着集合中不能出现重复的数据。Redis 中集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)。集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)。          
下面举一个小例子：
```
redis 127.0.0.1:6379> SADD runoobkey redis
(integer) 1
redis 127.0.0.1:6379> SADD runoobkey mongodb
(integer) 1
redis 127.0.0.1:6379> SADD runoobkey mysql
(integer) 1
redis 127.0.0.1:6379> SADD runoobkey mysql
(integer) 0
redis 127.0.0.1:6379> SMEMBERS runoobkey

1) "mysql"
2) "mongodb"
3) "redis"
```
Redis set集合基本命令：
![](9.png)
![](10.png)
# 11.Redis 有序集合(sorted set)
Redis 有序集合和集合一样也是string类型元素的集合,且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。有序集合的成员是唯一的,但分数(score)却可以重复。集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。 集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)。
下面举一个小demo：
```
redis 127.0.0.1:6379> ZADD runoobkey 1 redis
(integer) 1
redis 127.0.0.1:6379> ZADD runoobkey 2 mongodb
(integer) 1
redis 127.0.0.1:6379> ZADD runoobkey 3 mysql
(integer) 1
redis 127.0.0.1:6379> ZADD runoobkey 3 mysql
(integer) 0
redis 127.0.0.1:6379> ZADD runoobkey 4 mysql
(integer) 0
redis 127.0.0.1:6379> ZRANGE runoobkey 0 10 WITHSCORES

1) "redis"
2) "1"
3) "mongodb"
4) "2"
5) "mysql"
6) "4"
```
注意：如果出现重复元素，后来的会覆盖掉原来的         
redis 有序集合的基本命令:
![](11.png)
![](12.png)
![](13.png)
# 12.Redis HyperLogLog
Redis 在 2.8.9 版本添加了 HyperLogLog 结构。      
Redis HyperLogLog 是用来做基数统计的算法，HyperLogLog 的优点是：    
在输入元素的数量或者体积非常非常大时，计算基数所需的空间总是固定 的、并且是很小的。在 Redis 里面，每个 HyperLogLog 键只需要花费 12 KB 内存，就可以计算接近 2^64 个不同元素的基 数。这和计算基数时，元素越多耗费内存就越多的集合形成鲜明对比。但是，因为 HyperLogLog 只会根据输入元素来计算基数，而不会储存输入元素本身，所以 HyperLogLog 不能像集合那样，返回输入的各个元素。
### 什么是基数?
> 比如数据集 {1, 3, 6, 7, 6, 7, 8}， 那么这个数据集的基数集为 {1, 3, 5 ,7, 8}, 基数(不重复元素)为5。 基数估计就是在误差可接受的范围内，快速计算基数。
下面举一个实例：
```
redis 127.0.0.1:6379> PFADD runoobkey "redis"
1) (integer) 1
redis 127.0.0.1:6379> PFADD runoobkey "mongodb"
1) (integer) 1
redis 127.0.0.1:6379> PFADD runoobkey "mysql"
1) (integer) 1
redis 127.0.0.1:6379> PFCOUNT runoobkey
(integer) 3
```
redis HyperLogLog 的基本命令：
![](14.png)
# 13.Redis事务
### 1.一个事务从开始到执行会经历以下三个阶段：
* 开始事务。
* 命令入队。
* 执行事务。
### 2.Redis 事务可以一次执行多个命令， 并且带有以下两个重要的保证：
* 批量操作在发送 EXEC 命令前被放入队列缓存
* 收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行
* 在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中
下面举一个实例：
```
redis 127.0.0.1:6379> MULTI   //标记一个事务块的开始。
OK

redis 127.0.0.1:6379> SET book-name "Mastering C++ in 21 days"
QUEUED

redis 127.0.0.1:6379> GET book-name
QUEUED

redis 127.0.0.1:6379> SADD tag "C++" "Programming" "Mastering Series"
QUEUED

redis 127.0.0.1:6379> SMEMBERS tag
QUEUED

redis 127.0.0.1:6379> EXEC //执行所有事务块内的命令。
1) OK
2) "Mastering C++ in 21 days"
3) (integer) 3
4) 1) "Mastering Series"
   2) "C++"
   3) "Programming"
```
> redis事务的实现原理是把事务中的命令先放入队列中，当client提交了exec命令后，redis会把队列中的每一条命令按序执行一遍。如果在执行exec之前事务中断了，那么所有的命令都不会执行；如果执行了exec命令之后，那么所有的命令都会按序执行。但如果在事务执行期间redis被强制关闭，那么则需要使用redis-check-aof 工具对redis进行修复，删除那些部分执行的命令。
### 3.redis 事务的相关命令：
![](15.png)
# 14.Redis 服务器
Redis 服务器命令主要是用于管理 redis 服务。
一些常用的指令：
![](16.png)
![](17.png)
![](18.png)
![](19.png)
# 15.Redis 安全
### 1.设置密码
```
CONFIG get requirepass password
```
查看密码：
```
auth password//先进行身份验证
config get requirepass//获取当前密码
```
# 16.redis性能测试
基本语法：
> redis-benchmark [option] [option value]     
> 
同时执行 m 个请求来检测性能:
```
redis-benchmark -n m  -q
```
注意：
> redis-benchmark [option] [option value] 不是redis-cli命令的一部分，想要执行这条语句：     
![](20.png)
![](21.png)

redis 性能测试工具可选参数如下所示：
![](22.png)
下面举一个实例,使用了多个参数来测试 redis 性能：
```
$ redis-benchmark -h 127.0.0.1 -p 6379 -t set,lpush -n 10000 -q

SET: 146198.83 requests per second
LPUSH: 145560.41 requests per second
```
# 17.redis客户端连接
Redis 通过监听一个 TCP 端口或者 Unix socket 的方式来接收来自客户端的连接，当一个连接建立后，Redis 内部会进行以下一些操作：
* 首先，客户端 socket 会被设置为非阻塞模式，因为 Redis 在网络事件处理上采用的是非阻塞多路复用模型。
* 然后为这个 socket 设置 TCP_NODELAY 属性，禁用 Nagle 算法
* 然后创建一个可读的文件事件用于监听这个客户端 socket 的数据发送    
### 获取最大连接数：
```
config get maxclients
```
### 设置最大连接数：
```
redis-server --maxclients 100000
```
