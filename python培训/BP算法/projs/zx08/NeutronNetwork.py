# coding : utf-8
# 开发团队：lylg
# 开发人员：by
# 开发时间：2019/10/11 0011 10:22

import numpy as np
import pickle
import time

# 激活函数
def activate(x):
    return 1 / (1 + np.exp(-x))

# 激活函数的导函数
def activate_de(x):
    return activate(x) * (1 - activate(x))

class NeutronNetwork:
    def __init__(self, struct = (2, 2, 2), rate = 0.2, epoch = 100,
                 filename = 'network/nn.obj', load = False):
        '''
        构造神经网络
        :param struct: 表示神经网络结构：例如：(2, 3, 2)
        '''
        # 隐藏层权重：初始值为随机数
        self.hw = np.random.normal(np.zeros((struct[1], struct[0])))
        # 输出层权重：初始值为随机数
        self.ow = np.random.normal(np.zeros((struct[2], struct[1])))

        # 学习速率
        self.r = rate
        # 训练次数
        self.epoch = epoch

        if(load):
            self.load(filename)

    def predict(self, x):
        ''' 根据输入向量预测结果
        :param x: 输入向量(行向量)
        :return: Ypred (列向量)
        '''
        # 计算隐藏层输入，结果为 列向量
        h_in = np.dot(self.hw, x.transpose())
        # 计算隐藏层输出：隐藏层激活函数处理，结果仍为列向量
        h_out = activate(h_in)
        # 计算输出层输入(列向量)
        output_in = np.dot(self.ow, h_out)
        # 计算输出层输出
        output_out = activate(output_in)

        return output_out

    def train(self, in_data, out_data):
        ''' 根据输入的数据集进行训练
        :param in_data: 输入数据集 (X)
        :param out_data: 输出数据集 (Ytrue)
        '''
        # 总体训练 epoch 次
        start = time.time()
        print('start :', start)
        for i in range(self.epoch):
            # 每次从训练数据集 in_data 中取出一个样本进行训练
            for data in zip(in_data, out_data):
                self.train_once(data[0], data[1])
            print('ow :')
            print(self.ow)
            # break
        end = time.time()
        print('end =', end)
        print('last :', (end - start), 'ms')

    def train_once(self, x, y):
        '''针对一个样本 x 进行一次训练
        :param x: 一个训练样本
        :param y: 样本的真实输出
        '''
        # 将输入和输出样本数据转换为二维列向量
        x = np.array(x, ndmin=2).T
        y = np.array(y, ndmin=2).T

        # 将 X 映射为 Ypred
        # 计算隐藏层输入
        h_in = np.dot(self.hw, x)
        # 计算隐藏层输出
        h_out = activate(h_in)
        # 计算输出层输入
        # print('ow:')
        # print(self.ow)
        # print('h_out:')
        # print(h_out)
        output_in = np.dot(self.ow, h_out)
        # 计算输出层输出，即：Ypred
        output_out = activate(output_in)

        # 输出层误差
        output_errors = y - output_out

        # 针对 output_in 计算激活函数的导数
        activate_output_in = activate(output_in)
        activate_output_in_de = activate_output_in * (1 - activate_output_in)

        # 更新输出层权重
        self.ow += self.r * np.dot(output_errors * activate_output_in_de, h_out.T)

        # 计算隐藏层误差
        hidden_errors = np.dot(self.ow.T, output_errors * activate_output_in_de)

        # 针对 h_in 计算好激活函数的导数
        activate_h_in = activate(h_in)
        activate_h_in_de = activate_h_in * (1 - activate_h_in)

        # 更新隐藏层权重
        self.hw += self.r * np.dot(hidden_errors * activate_h_in_de, x.T)

    def store(self, filename = 'network/nn.obj'):
        ''' 存储当前神经网络结构
        :param filename: 网络结构文件名
        '''
        # 写二进制文件
        file = open(filename, 'wb')
        pickle.dump(self.r, file)
        pickle.dump(self.epoch, file)
        pickle.dump(self.hw, file)
        pickle.dump(self.ow, file)
        file.close()

    def load(self, filename = 'network/nn.obj'):
        ''' 加载神经网络结构
        :param filename: 网络结构文件名
        '''
        # 读取二进制文件
        file = open(filename, 'rb')
        self.r = pickle.load(file)
        self.epoch = pickle.load(file)
        self.hw = pickle.load(file)
        self.ow = pickle.load(file)
        file.close()

if __name__ == '__main__':
    # 1. 准备数据
    # 训练数据
    # 输入：身高和体重
    # 平均身高：170， 平均体重：60
    in_data = np.array([
        [7, -3],
        [-5, -13],
        [3, -5],
        [-7, -5],
        [5, 5],
        [-9, -16],
        [4, 9],
        [-10, -18],
        [0, 0],
        [-10, -10],

        [3, 15],
        [3, -6],
        [5, -5],
        [-4, -10],
        [6, 22],

        [10, 15],
        [5, 10],
        [3, 12],
        [0, 22],
        [-4, -10],

        [3, 2],
        [-10, -10],
        [10, 12]
    ])
    # 输出：性别
    out_data = np.array([
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
        [0, 1],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [0, 1],
        [1, 0],
        [0, 1],
        [1, 0]
    ])
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

    # 2. 创建神经网络
    nn = NeutronNetwork(struct=(2, 2, 2), rate = 0.02, epoch=1000)

    # 3. 训练
    nn.train(in_data, out_data)

    # 存储当前神经网络结构
    nn.store()

    # 4. 预测
    print('-----------------------------------------')
    for data in zip(test_in, test_out):
        y = nn.predict(data[0])
        print('X, Ytrue, Ypred :', data, [1,0] if y[0] > 0.5 else [0, 1])

