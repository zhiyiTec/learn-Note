# coding : utf-8
# 开发团队：lylg
# 开发人员：by
# 开发时间：2019/10/12 0012 10:58

import numpy as np
import NeutronNetwork as NN

# 创建空神经网络
nn = NN.NeutronNetwork(load=True)

# 测试数据
# 测试输入数据
test_in = np.array([
    [15, 0],
    [-8, -5],
    [5, 15],
    [-8, 0],
    [3, 11],
    [-15, -10]
])
# 测试输出数据
test_out = np.array([
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1]
])

# 4. 预测
print('-----------------------------------------')
for data in zip(test_in, test_out):
    y = nn.predict(data[0])
    print('X, Ytrue, Ypred :', data, [1,0] if y[0] > 0.5 else [0, 1])


