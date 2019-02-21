---
layout:     post
title:      OpenNe源码解析之DeepWalk
subtitle:   网络嵌入
date:       2019-01-24
author:     Yunlongs
catalog: true
tags:
    - 机器学习
    - OpenNe
    - 网络嵌入
---

>关于DeepWalk算法很好的讲解教程：https://zhuanlan.zhihu.com/p/45167021
OpenNe代码可以在github上找到
# OpenNe源码解析之DeepWalk

## Deepwalk算法伪代码
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%871.jpg)

**参数：** 图，游走窗口大小，嵌入的规模，每个节点游走几次，每次游走长度
**第一步：** 初始化节点和向量之间的映射关系
**第二步：** 建立Hierarchical Softmax模型中的Huffman树。
**第三步：** 总共对这个图进行γ次游走
**第四步：** 每次游走都要将自己从生成的图顺序打乱，重新一次新的游走
**第五，六步：** 对于打乱后的每一个节点，以此为根节点，进行长度为t的游走。
**第七步：** 对于生成的每一段游走序列，使用skipgram算法来生成该节点的向量

## Deepwalk源码解读
### 1.在__main.py__第110行，初始化图对象
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%872.jpg)
其在graph.py中的构造函数如下
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%873.jpg)
第__main.py__113行，读取文件，将其装换为所要用的数据结构：图
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%874.jpg)
在graph.py第38行，读取节点转化为图。第39.40行，将图所有边权值初始化为1
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%875.jpg)
第23，24，25行：遍历所有节点，为每个节点从小到大编号，并存储。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%877.jpg)


### 2.在__main.py__ 第129行，调用deepwalk：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%878.jpg)
判断方法是否deepwalk，调用node2vec的算法。
参数如下：

    graph：由输入的网络节点构成的图；
    path_length：游走长度，默认80；
    num_paths:游走次数，默认10次；
    dim：向量维数，默认128；
    workers：并发数，默认8；
    windows：窗口大小，默认10。
    dw：是否deepwalk算法。

### 3.在node2vec.py 第12行，判断是否Deepwalk，并将参数p，q=0。
node2vec.py第19行初始化deepwalk的类。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%879.jpg)
>在walk.py中存在两个类，一个是deepwalk算法简单随机游走的类BasicWalker和node2vec算法中所要使用的带参数游走的类Walker。

### 4.构造类完成后，在node2vec.py第25行
调用deepwalk的真正核心算法
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8710.jpg)
walk.py第36行调用deepwalk算法的主程序
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8711.jpg)

>第40.41行，初始化变量
第42行，将之前读取文件获取的图的节点，转化成列表存储。
第44行，对应图2中的第三步，进行10次游走。
第47行，每次游走前，先将节点（list）的顺序打乱，以进行10次不同的游走。对应图2第四步。
第48，49行，遍历每个节点，并以每个节点为起始节点进行长度为80的游走。并将游走序列进行存储。对应图2中的第五，六行。

### 5.具体的游走序列的生成算法如下：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8712.jpg)
>在walk.py中的第17行，对每个节点调用deepwalk_walk算法，进行游走。
第21-23行，参数初始化
（其中look_up_dict中存储的是读入文件时，每个节点的从1-size的编号）
第25-33行代码的意思如下：
walk刚开始是一个只有根节点的列表，判断walk中节点的个数是否超过设定的游走长度（80），若没有，则取最后一个节点，获取这个节点的邻居节点，若存在邻居节点，则随便选择一个存入walk列表中，知道walk中充满80个节点。

从而生成随机游走序列。

### 6.当完成10次游走后，游走函数开始返回游走结果，并进行处理。
此时已经获得节点数目*游走次数（size*10）条游走序列，并全部返回到了node2vec.py中25行的sentences变量中。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8713.jpg)

下面这一段代码就是准备word2vec算法的参数，然后运行算法。
由于先前的代码中也有一部分参数，这里就把运行deepwalk所用的kwargs参数整理下：
第11行： works代表线程数，但是并发数，此处使用的默认值8
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/TIM%E6%88%AA%E5%9B%BE20190131132533.jpg)
第13行，hs为1代表hierarchical softmax模型，0为negative sampling模型
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8714.jpg)
第27行，sentences代表要训练的语料，这里就是所有的游走序列。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8715.jpg)
第28行，min_count代表低频词丢弃，这里使用默认值0，即不丢弃任何低频词。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8716.jpg)
第29行，size代表向量维度，这里使用默认的180
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8717.jpg)
第30行，sg代表为0，对应CBOW算法；sg=1则采用skip-gram算法。这里采用skip-gram
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8718.jpg)

第34行，即进行hierarchical softmax下的skip-gram算法，进行训练
第36，37行，存储每个节点及其对应的向量
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8719.jpg)

### 7.返回__main.py__，输出运行时间，调用存储函数
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8720.jpg)

调用node2vec中的存储函数。
第43行，第一行存储节点总数目，以及向量维数
第44，45行，剩下每一行，写出当前节点id，与其每一向量分量
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/%E5%9B%BE%E7%89%8721.jpg)

##总结
OpenNe中的Deepwalk算法与图2中算法的区别在于，图2是每获得一个游走序列就进行学习算法，而OpenNe中，是等待获得所有的游走序列后，才进行学习算法。