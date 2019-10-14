# coding : utf-8
# 开发团队：lylg
# 开发人员：by
# 开发时间：2019/10/12 0012 14:50

import numpy as np
import pickle
import time

# 激活函数
def activate(x):
    return 1 / (1 + np.exp(-x))

# 激活函数的导数
def activate_de(x):
    ac = activate(x)
    return ac * (1 - ac)

class NeutralNetwork:
    ''' 神经网络类
    '''
    def __init__(self, struct = (), r = 0.1, epoch = 100,
                 filename='network/nn.obj', load = False):
        '''
        构造神经网络
        :param struct: 神经网络结构 (2, 3, 2)
        :param r:
        :param epoch:
        '''
        if load:
            self.load(filename)
        else:
            # 隐藏层权重矩阵
            self.hw = np.random.normal(np.zeros((struct[1], struct[0])))

            # 输出层权重矩阵
            self.ow = np.random.normal(np.zeros((struct[2], struct[1])))

            # 学习速率
            self.r = r

            # 训练遍数
            self.epoch = epoch

    def predict(self, x):
        ''' 根据输入数据，预测结果
        :param x: 输入行向量
        '''
        # 将输入向量转为 nparray 列向量
        x = np.array(x, ndmin=2).T

        # 计算隐藏层输入 h_in
        h_in = np.dot(self.hw, x)
        # 计算隐藏层输出 h_out
        h_out = activate(h_in)
        # 计算输出层输入 ouput_in
        output_in = np.dot(self.ow, h_out)
        # 计算输出层输出 output_out
        output_out = activate(output_in)

        return output_out

    def train(self, x_data, ytrue_data):
        '''
        训练神经网络 epoch 遍
        :param x_data: 输入数据集
        :param ytrue_data: 输出数据集
        :return:
        '''
        start = time.time()
        print('start :', start, 'ms')
        # 训练 epoch 遍
        for i in range(self.epoch):
            # 针对每个样本训练一次
            for data in zip(x_data, ytrue_data):
                self.train_once(data[0], data[1])
        end = time.time()
        print('end :', end)
        print('last :', (end - start), 'ms')

    def train_once(self, x, ytrue):
        '''
        针对一个样本 (x, ytrue)，进行训练
        :param x: 输入行向量
        :param ytrue: 输出行向量
        '''
        # 将输入/输出向量转换为 列向量
        x = np.array(x, ndmin=2).T
        ytrue = np.array(ytrue, ndmin=2).T

        # 根据输入，计算 Ypred, output_out
        h_in = np.dot(self.hw, x)
        h_out = activate(h_in)
        output_in = np.dot(self.ow, h_out)
        output_out = activate(output_in)

        # 计算输出误差
        output_errors = ytrue - output_out
        cal_tmp = output_errors * activate_de(output_in)
        # 更新输出层权重
        self.ow += self.r * np.dot(cal_tmp, h_out.T)
        # 计算隐藏层误差
        hidden_errors = np.dot(self.ow.T, cal_tmp)
        # 更新隐藏层权重
        self.hw += self.r * np.dot(hidden_errors * activate_de(h_in), x.T)

    def store(self, filename = 'network/nn.obj'):
        '''
        存储当前神经网络
        :param filename: 文件名
        '''
        file = open(filename, 'wb')
        pickle.dump(self.hw, file)
        pickle.dump(self.ow, file)
        pickle.dump(self.r, file)
        pickle.dump(self.epoch, file)
        file.close()

    def load(self, filename = 'network/nn.obj'):
        '''
        加载指定神经网络数据
        :param filename: 文件名
        '''
        file = open(filename, 'rb')
        self.hw = pickle.load(file)
        self.ow = pickle.load(file)
        self.r = pickle.load(file)
        self.epoch = pickle.load(file)
        file.close()

if __name__ == '__main__':
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
        [160, 57]
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
    nn = NeutralNetwork((2, 3, 2), 0.1, 100)

    # 2. 训练
    nn.train(in_data, out_data)
    # 存储模型
    nn.store()

    # 3. 预测
    for test in zip(in_test, out_test):
        ypred = nn.predict(test[0])
        print('in :', test[0], 'Ytrue :', test[1])
        print('predict :')
        print(ypred)

