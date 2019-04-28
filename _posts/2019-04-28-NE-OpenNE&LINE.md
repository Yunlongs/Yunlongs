---
layout:     post
title:      OpenNe源码解析之LINE
subtitle:   网络嵌入
date:       2019-04-28
author:     Yunlongs
catalog: true
tags:
    - 机器学习
    - Network Embedding
---

# OpenNe源码解析之LINE
直接贴源码了
```
from __future__ import print_function
import random
import math
import numpy as np
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from .classify import Classifier, read_node_label


class _LINE(object):

    def __init__(self, graph, rep_size=128, batch_size=1000, negative_ratio=5, order=3):
        self.cur_epoch = 0   # 进行训练次数
        self.order = order   # 嵌入的阶数
        self.g = graph       # 图
        self.node_size = graph.G.number_of_nodes()  # 节点数目
        self.rep_size = rep_size    # 嵌入向量的维数
        self.batch_size = batch_size    # 每一批次的大小（没太懂这个参数的作用）
        self.negative_ratio = negative_ratio  # 采样比例
        # 赋值

        self.gen_sampling_table()  # 初始化 alias 方法的边采样表
        self.sess = tf.Session()   # TensorFlow的会话
        cur_seed = random.getrandbits(32)  # 得到32为随机的整数
        initializer = tf.contrib.layers.xavier_initializer(
            uniform=False, seed=cur_seed)  # 返回一个初始化权重的函数“xavier”，使用正态分布随机初始化
        with tf.variable_scope("model", reuse=None, initializer=initializer):  # 变量域为“model”，拒绝重用
            self.build_graph()  # 这里构建TensorFlow的图
        self.sess.run(tf.global_variables_initializer())  # 初始化并运行所有的初始化变量

    def build_graph(self):
        self.h = tf.placeholder(tf.int32, [None])
        self.t = tf.placeholder(tf.int32, [None])
        self.sign = tf.placeholder(tf.float32, [None])  # 预定义占位符

        cur_seed = random.getrandbits(32)  # 得到32为随机的整数
        self.embeddings = tf.get_variable(name="embeddings"+str(self.order), shape=[
                                          self.node_size, self.rep_size], initializer=tf.contrib.layers.xavier_initializer(uniform=False, seed=cur_seed))
        self.context_embeddings = tf.get_variable(name="context_embeddings"+str(self.order), shape=[
                                                  self.node_size, self.rep_size], initializer=tf.contrib.layers.xavier_initializer(uniform=False, seed=cur_seed))
        # 上面两行意思是：创建一个名为“embeddings+阶数”的 （node*rep）的矩阵，并使用xavier来初始化

        # self.h_e = tf.nn.l2_normalize(tf.nn.embedding_lookup(self.embeddings, self.h), 1)
        # self.t_e = tf.nn.l2_normalize(tf.nn.embedding_lookup(self.embeddings, self.t), 1)
        # self.t_e_context = tf.nn.l2_normalize(tf.nn.embedding_lookup(self.context_embeddings, self.t), 1)

        self.h_e = tf.nn.embedding_lookup(self.embeddings, self.h)  # 得到嵌入矩阵中第h行的行向量，即顶点h的嵌入向量
        self.t_e = tf.nn.embedding_lookup(self.embeddings, self.t)  # 得到嵌入矩阵中第t行的行向量，即顶点t的嵌入向量
        self.t_e_context = tf.nn.embedding_lookup(
            self.context_embeddings, self.t)    # 得到上下文嵌入矩阵中第t行的行向量，即顶点t的上下文嵌入向量

        self.second_loss = -tf.reduce_mean(tf.log_sigmoid(
            self.sign*tf.reduce_sum(tf.multiply(self.h_e, self.t_e_context), axis=1)))
        # 二阶的损失函数（和网上看到的公式貌似不太对应）
        self.first_loss = -tf.reduce_mean(tf.log_sigmoid(
            self.sign*tf.reduce_sum(tf.multiply(self.h_e, self.t_e), axis=1)))
        # 一阶的损失函数
        if self.order == 1:  # 判断当前是要计算几阶的，并赋值
            self.loss = self.first_loss
        else:
            self.loss = self.second_loss
        optimizer = tf.train.AdamOptimizer(0.001)  # 使用adam算法来进行优化，学习速率是0.001
        self.train_op = optimizer.minimize(self.loss)  # 对损失函数进行最小化

    def train_one_epoch(self):
        sum_loss = 0.0
        batches = self.batch_iter()  # 获得h，t，sign分组
        batch_id = 0
        for batch in batches:  # 对获得的每个分组值进行迭代
            h, t, sign = batch
            feed_dict = {
                self.h: h,
                self.t: t,
                self.sign: sign,
            }  # feed用的参数表
            _, cur_loss = self.sess.run([self.train_op, self.loss], feed_dict)  # 注入参数
            sum_loss += cur_loss  # 总的损失
            batch_id += 1
        print('epoch:{} sum of loss:{!s}'.format(self.cur_epoch, sum_loss))
        self.cur_epoch += 1

    def batch_iter(self):
        look_up = self.g.look_up_dict  # 对每个节点都进行了编号的 字典

        table_size = 1e8    # 表的大小 1亿
        numNodes = self.node_size

        edges = [(look_up[x[0]], look_up[x[1]]) for x in self.g.G.edges()]  # 存储每条边(n1,n2)的编号 到edges中

        data_size = self.g.G.number_of_edges()  # 边的条数
        edge_set = set([x[0]*numNodes+x[1] for x in edges])   # 建立一个 每条边起始节点的编号*节点总数+尾结点编号 的集合
        shuffle_indices = np.random.permutation(np.arange(data_size))  #返回一个 经过打乱后的 从0--边总数  的数组

        # positive or negative mod
        mod = 0
        mod_size = 1 + self.negative_ratio  # mod_size = 6
        h = []
        t = []
        sign = 0

        start_index = 0
        end_index = min(start_index+self.batch_size, data_size)  # 确定终止索引为 分批大小和边的数目中 最小的 那个
        while start_index < data_size:
            if mod == 0:
                sign = 1.
                h = []
                t = []
                for i in range(start_index, end_index):
                    if not random.random() < self.edge_prob[shuffle_indices[i]]:  # 当选取的随机数 不小于 被打乱后节点数组中第i条边的概率时
                        shuffle_indices[i] = self.edge_alias[shuffle_indices[i]]   # 将打乱数组中这个节点 换成 alias表中 它的第二个节点
                    cur_h = edges[shuffle_indices[i]][0]
                    cur_t = edges[shuffle_indices[i]][1]  # h和t 即为随机边抽样 获得的 起始节点编号  和  尾节点编号
                    h.append(cur_h)
                    t.append(cur_t)    # 存储抽样得到的 边
            else:
                sign = -1.
                t = []
                for i in range(len(h)):
                    t.append(
                        self.sampling_table[random.randint(0, table_size-1)])

            yield h, t, [sign]
            mod += 1
            mod %= mod_size  # 即mod 为  0 1 2 3 4 5 当mod=6的时候退出循环
            if mod == 0:  # 此时循环进行了6次，该退出了
                start_index = end_index
                end_index = min(start_index+self.batch_size, data_size)

    def gen_sampling_table(self):
        table_size = 1e8  # 取样表的大小为1亿
        power = 0.75
        numNodes = self.node_size

        print("Pre-procesing for non-uniform negative sampling!")
        node_degree = np.zeros(numNodes)  # out degree

        look_up = self.g.look_up_dict
        for edge in self.g.G.edges():
            node_degree[look_up[edge[0]]
                        ] += self.g.G[edge[0]][edge[1]]["weight"]  # 计算每个节点的出度（当weight=1时）

        norm = sum([math.pow(node_degree[i], power) for i in range(numNodes)])  # 计算每个节点出度的0.75次方，并累加求和
        # 这里获得的是公式（7）中的Pn(v)


        self.sampling_table = np.zeros(int(table_size), dtype=np.uint32)  # 生成大小为1亿的0向量

        p = 0
        i = 0
        for j in range(numNodes):
            p += float(math.pow(node_degree[j], power)) / norm
            while i < table_size and float(i) / table_size < p:
                self.sampling_table[i] = j
                i += 1
                # 上面获得的是 递增的取样表


        data_size = self.g.G.number_of_edges()      # 边的个数
        self.edge_alias = np.zeros(data_size, dtype=np.int32)
        self.edge_prob = np.zeros(data_size, dtype=np.float32)
        large_block = np.zeros(data_size, dtype=np.int32)  # 存储概率比1大的
        small_block = np.zeros(data_size, dtype=np.int32)  # 存储概率比1小的

        total_sum = sum([self.g.G[edge[0]][edge[1]]["weight"]  # 计算所有边的权重的累加和
                         for edge in self.g.G.edges()])
        norm_prob = [self.g.G[edge[0]][edge[1]]["weight"] *
                     data_size/total_sum for edge in self.g.G.edges()]
        num_small_block = 0
        num_large_block = 0
        cur_small_block = 0
        cur_large_block = 0
        for k in range(data_size-1, -1, -1):  # 从datasize开始 逐个-1   到-1为止
            if norm_prob[k] < 1:
                small_block[num_small_block] = k
                num_small_block += 1
            else:
                large_block[num_large_block] = k
                num_large_block += 1                   # 以上就是存储比1大和比1小的值
        while num_small_block and num_large_block:
            num_small_block -= 1
            cur_small_block = small_block[num_small_block]  # 取出当前的小分组 的节点
            num_large_block -= 1
            cur_large_block = large_block[num_large_block]  # 取出当前的大分组 的节点
            self.edge_prob[cur_small_block] = norm_prob[cur_small_block]  # 当前这个小分组 对应的边的概率
            self.edge_alias[cur_small_block] = cur_large_block       # 找出这个小分组对应的 的alias
            norm_prob[cur_large_block] = norm_prob[cur_large_block] + \
                norm_prob[cur_small_block] - 1
            if norm_prob[cur_large_block] < 1:
                small_block[num_small_block] = cur_large_block
                num_small_block += 1
            else:
                large_block[num_large_block] = cur_large_block
                num_large_block += 1

        while num_large_block:
            num_large_block -= 1
            self.edge_prob[large_block[num_large_block]] = 1
        while num_small_block:
            num_small_block -= 1
            self.edge_prob[small_block[num_small_block]] = 1

    def get_embeddings(self):
        vectors = {}
        embeddings = self.embeddings.eval(session=self.sess)  # 运行获取嵌入矩阵
        # embeddings = self.sess.run(tf.nn.l2_normalize(self.embeddings.eval(session=self.sess), 1))
        look_back = self.g.look_back_list
        for i, embedding in enumerate(embeddings):
            vectors[look_back[i]] = embedding   # 获取每个节点的嵌入向量
        return vectors


class LINE(object):

    def __init__(self, graph, rep_size=128, batch_size=1000, epoch=10, negative_ratio=5, order=3, label_file=None, clf_ratio=0.5, auto_save=True):
        self.rep_size = rep_size
        self.order = order
        self.best_result = 0
        self.vectors = {}
        if order == 3:   # 一阶与二阶相似都进行
            self.model1 = _LINE(graph, rep_size/2, batch_size,
                                negative_ratio, order=1)
            self.model2 = _LINE(graph, rep_size/2, batch_size,
                                negative_ratio, order=2)  # 获取一阶 或者二阶 的优化模型
            for i in range(epoch):   # 进行10次 迭代
                self.model1.train_one_epoch()  # 对一阶模型训练一次
                self.model2.train_one_epoch()  # 对二阶模型训练一次
                if label_file:  # 如果有标签文件的话
                    self.get_embeddings()  # 得到嵌入的向量
                    X, Y = read_node_label(label_file)  # 读标签文件
                    print("Training classifier using {:.2f}% nodes...".format(
                        clf_ratio*100))  # 输出使用评估节点的百分比
                    clf = Classifier(vectors=self.vectors,
                                     clf=LogisticRegression())  # 初始化逻辑回归分类器
                    result = clf.split_train_evaluate(X, Y, clf_ratio)  #对结果进行评估

                    if result['macro'] > self.best_result:
                        self.best_result = result['macro']   # 存储训练结果最好的嵌入向量
                        if auto_save:
                            self.best_vector = self.vectors

        else:  # 当只进行一阶或只进行二阶时 ，与上面的相似，不再进行注释
            self.model = _LINE(graph, rep_size, batch_size,
                               negative_ratio, order=self.order)
            for i in range(epoch):
                self.model.train_one_epoch()
                if label_file:
                    self.get_embeddings()
                    X, Y = read_node_label(label_file)
                    print("Training classifier using {:.2f}% nodes...".format(
                        clf_ratio*100))
                    clf = Classifier(vectors=self.vectors,
                                     clf=LogisticRegression())
                    result = clf.split_train_evaluate(X, Y, clf_ratio)

                    if result['macro'] > self.best_result:
                        self.best_result = result['macro']
                        if auto_save:
                            self.best_vector = self.vectors

        self.get_embeddings()
        if auto_save and label_file:
            self.vectors = self.best_vector

    def get_embeddings(self):  # 得到嵌入的向量
        self.last_vectors = self.vectors
        self.vectors = {}
        if self.order == 3:  # 如果同时训练一阶和二阶的话
            vectors1 = self.model1.get_embeddings()
            vectors2 = self.model2.get_embeddings()  # 得到一阶和二阶的嵌入向量
            for node in vectors1.keys():  # 获取每个节点
                self.vectors[node] = np.append(vectors1[node], vectors2[node])  # 将一阶向量与二阶向量进行合并
        else:
            self.vectors = self.model.get_embeddings()

    def save_embeddings(self, filename): # 存储嵌入向量结果
        fout = open(filename, 'w')
        node_num = len(self.vectors.keys())
        fout.write("{} {}\n".format(node_num, self.rep_size))
        for node, vec in self.vectors.items():
            fout.write("{} {}\n".format(node,
                                        ' '.join([str(x) for x in vec])))
        fout.close()
```


