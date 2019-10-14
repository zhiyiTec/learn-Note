# coding : utf-8
# 开发团队：lylg
# 开发人员：by
# 开发时间：2019/10/12 0012 14:56

import numpy as np

# 1. 生成正太分布的随机数
a = np.random.normal(np.zeros((2, 2)))
print(a)

# 2. 输入列表转为 2 维行向量
x = np.array([1, 2], ndmin=2).T
print('x:')
print(x)

a = np.array([[10, 20],
             [30, 40]])
r = np.dot(a, x)
print(r)



