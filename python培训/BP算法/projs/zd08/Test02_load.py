# coding : utf-8
# 开发团队：lylg
# 开发人员：by
# 开发时间：2019/10/12 0012 16:54

import numpy as np
import NeutralNetwork as NN

# 0. 准备数据
# 训练数据
in_data = [
    [165, 55],
    [160, 53],
    [175, 55],
    [163, 55],
    [173, 49],
    [163, 56],
    [180, 77],
    [155, 54],
    [176, 79],
    [161, 49],
    [180, 60],
    [168, 57],
    [172, 69],
    [166, 50],
    [172, 90],
    [163, 51],
    [175, 70],
    [164, 53],
    [160, 45],
    [160, 56],

    [182, 70],
    [180, 74],
    [185, 73],
    [165, 55],
    [185, 75],
    [175, 71],
    [181, 62],
    [180, 72],
    [175, 70],
    [165, 55],
]
out_data = [
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],

    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [0, 1],
]

# 测试数据
in_test = [
    [175, 65],
    [170, 58],
    [162, 49],
    [182, 90],
    [160, 57],
]
out_test = [
    [1, 0],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
]

print(np.average(in_data, axis=0))
print('-' * 100)

r_data = []
for item in in_data:
    r = []
    r.append(item[0] - 171)
    r.append(item[1] - 62)
    r_data.append(r)
in_data = r_data

print('-' * 100)
r_data = []
for item in in_test:
    r = []
    r.append(item[0] - 171)
    r.append(item[1] - 62)
    r_data.append(r)
in_test = r_data

print('in_data:', len(in_data))
print('out_data:', len(out_data))
print('in_test:', len(in_test))
print('out_test:', len(out_test))

# # 1. 创建神经网络
nn = NN.NeutralNetwork(load = True)

# 2. 预测
for test in zip(in_test, out_test):
    ypred = nn.predict(test[0])
    print('in :', test[0], 'Ytrue :', test[1])
    print('predict :')
    print(ypred)
