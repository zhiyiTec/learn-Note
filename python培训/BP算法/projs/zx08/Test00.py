# coding : utf-8
# 开发团队：lylg
# 开发人员：by
# 开发时间：2019/10/12 0012 8:51

import numpy as np

# 1. 将列表 x 转换为二维列向量
# x = [1, 2]
# x = np.array(x, ndmin=2).T
# print(x)

# 2. 随机数生成
a = np.random.random((2, 2)) - 0.5
print(a)

b = np.random.normal([[0, 0],
                      [0, 0]])
print(b)

c = np.random.normal(np.zeros((3,2)))
print(c)
