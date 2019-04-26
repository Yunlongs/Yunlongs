---
layout:     post
title:      Deepwalk算法深度研究
subtitle:   网络嵌入
date:       2019-04-26
author:     Yunlongs
catalog: true
tags:
    - 机器学习
    - Network Embedding
---

>转载请注明本博客地址
# Deepwalk算法深度研究
## 1. 算法介绍
在介绍Deepwalk算法之前，这里先引出一个**分类问题**：对于一个网络拓扑结构来说，纵使其各个节点间的关系十分复杂，也可以转化成计算机所能直接处理的数据结构--图，如图1就是将一个带权网络拓扑转化为一个无向图的邻接矩阵的过程。因此给定一个图$\mathrm{G}=(\mathrm{V}, \mathrm{E})$,其中V是图中的顶点，E是顶点之间的边，$E \subseteq(V \times V)$，得到一个标注图$\mathrm{G_L}(\mathrm{V}, \mathrm{E}, \mathrm{X}, \mathrm{Y})$，顶点表示矩阵$X \in R^{|V|} \times S$，$|V |$为顶点的个数，S为顶点向量的维度，标注矩阵$Y \in R^{|V| \times |y|}$,$|y|$为标签集。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/1.jpg)
Deepwalk算法要做的就是学习出顶点的向量表示$X_{E} \in R^{|V| \times d}$，d是向量的维度，通常会比较小，社会网络中所具有的一些现象及氛围或者概念将会在该维度内的空间中表示出来。

在Deepwalk算法的实现过程中，采用了与对自然语言处理中词嵌入类似的方法。词嵌入是对文本中的单词作为基本元素进行处理，将每个单词转化为保留上下文信息的潜在语义表示，相对应的，Deepwalk采用对网络拓扑随机游走产生的节点游走序列中的网络节点作为基本元素进行处理，将每个节点转化为保留宏观网络结构特征的潜在网络表示。

至于随机游走产生的网络嵌入为什么能与语言模型中的词嵌入的联系在一起，是因为在现实生活中，随机游走中节点的幂律分布和自然语言中词的幂律分布十分相似。在图2中，第一幅图的数据来自大规模图中的一系列随机游走，第二幅图的数据来自英文维基百科10万篇文章的文本。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/2.jpg)

## 2. 随机游走
在正式介绍Deepwalk算法细节之前，需要先了解游走序列的生成方式。随机游走即在特定网络拓扑构成的图中，从图中的一个随机节点开始，根据此节点的连通情况随机的选择下一个节点，进行一定步长的游走，起止节点之间所经过的节点即为一条游走序列，图中所有节点都要进行一次以此节点为起点的游走，并重复游走数次。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/3.jpg)
如图3所示，在起始节点为$V_i$的情况下，以$V_i$为根节点进行了步长为4的游走，其游走序列$\mathrm{Wv}_{\mathrm{i}}$（图中绿色标识的路线）经过点标记为$\mathrm{W}^{1} \mathrm{v}_{\mathrm{i}}, \mathrm{W}^{2} \mathrm{v}_{\mathrm{i}}, \mathrm{W}^{3} \mathrm{V}_{\mathrm{i}},\mathrm{W}^{4} \mathrm{v}_{\mathrm{i}}$。随机游走序列可以作为一个基本工具来帮助我们从社会网络中提取信息，除此之外随机游走还能为在算法中提供两条额外的属性：
**并行化：** 随机游走是局部的，对于一个大的网络来说，可以同时在不同的顶点开始进行一定长度的随机游走，多个随机游走同时进行，可以减少采样的时间。
**适应性：** 因为短的随机游走只是局部范围内进行采样，因此当网络拓扑发生小的变动时，只需要在发生节点发生改变的区域进行随机游走，而不需要再重新学习一次。

## 3. 算法设计
在语言模型中所使用的词嵌入技术描绘如下：给定一组由单词组成的长度为n的句子
$W_{1}^{n}=\left(w_{0}, w_{1}, \ldots, w_{n}\right)$
$w_i$代表着此句子中的第i个单词，我们的目标是使在给定前n-1个词的情况下，出现$w_n$的概率最大，即最大化参数使得$\operatorname{Pr}\left(w_{n} | w_{0}, w_{1}, \cdots, w_{n-1}\right)$取最大值。
将此思想推广到网络拓扑中，可以得到网络嵌入的雏形：给定一条由网络节点组成的随机游走序列
$V_{1}^{N}=\left(v_{0}, v_{1}, \ldots, v_{n}\right)$
这条随机游走序列看作为一种特殊语言中的一个句子，将这条特殊的文本按照正常语言来处理，此时的目标是在给定游走序列中前n-1个节点的情况下，使第n个节点为$v_i$的概率
$\operatorname{Pr}\left(v_{i} |\left(v_{1}, v_{2}, \ldots, v_{i-1}\right)\right)$
达到最大化。
但是我们的目标不仅仅是会哦的这些节点同时存在时的概率分布，我们还要获得他们的潜在表示，这里将引入映射函数$\Phi : v \in V \rightarrow R^{|V| \times d}$，它是一个|V | × d维的矩阵，$\Phi\left(v_{i}\right)$代表的是节点$v_i$所在图中所具有的潜在社会表示。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/4.jpg)
因此，当使用节点的映射代替节点时，我们的优化目标就变成了
$\operatorname{Pr}\left(v_{i} |\left(\Phi\left(v_{1}\right), \Phi\left(v_{2}\right), \ldots, \Phi\left(v_{i-1}\right)\right)\right)$
但是从上式中也可以看出一个问题，为了得到$v_i$的优化目标函数，需要之前i-1个点的潜在社会表示，这就使得当游走序列越来越长时，计算出目标函数几乎是不可行的。为了解决这个问题，**Deepwalk采用了词嵌入技术中的Skip-gram方法思想：**（1）不再使用上下文来预测一个缺失词，而是使用缺失词来预测上下文。（2）上下文由目标词的左右两侧组成，不仅仅是一边。（3）最大化词在上下文中出现的概率，并且不需要知道对于给定词的相对偏移位置。新的优化目标总结如下：
$\log \operatorname{Pr}\left(\left\{v_{i-w}, \ldots, v_{i-1}, v_{i+1}, \ldots, v_{i+w}\right\} | \Phi\left(v_{i}\right)\right)$
当解决了这个优化问题时，我们将获得在局部节点之间存在相似性的潜在社会表示，即当两个节点有相同的邻居节点时，这两个节点将获得相同的表示，并且这性质还可以进行推广到更大的范围中。
## 4. 嵌入向量产生过程
通过以上的讨论，已经可以了解到Deepwalk算法中一段随机游走序列如何转化为每个游走节点潜在表示的过程，这里将详细介绍得到目标优化函数及游走序列后如何产生潜在网络结构表示的过程，因为Deepwalk是将游走序列当成一种特殊的语言文本来进行处理，故对目标函数的优化直接采用的是word2vec中的基于Hierarchical Softmax的Skip-gram模型。接下来将详细介绍这种模型产生词向量的过程。
**基于Hierarchical Softmax的Skip-gram模型如图5(a)显示**，是在已知当前词wt的情况下，预测其上下文$w_{t-2},w_{t-1},w_{t+1},w_{t+2}$，包括输入层、投影层、输出层三层。**更为详细点的模型图如图5(b)所示**，输入层的输入为当前样本中心词的词向量v(w)，投影层的功能只是个恒等映射，故投影层的输出仍然为v(w)，而输出层则是经过Huffman树进行目标优化后再经过softmax后的词概率。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/5.jpg)
这里我们将图5(b)中输出层的Huffman树建立过程描述如下：由语料中所有出现过的词作为叶子节点，根据每个词在语料中出现的次数作为叶子节点的权重，并依此建立起Huffman树。Huffman树的根节点的向量表示为输出层的输入v(w)（之后用Xw表示），所有新增的非叶节点的向量表示为辅助向量θ，所有叶子节点的向量表示为对应词的词向量。


![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/6.jpg)
根据图6的Huffman树，还需要定义以下符号：（1）$p^w$为从根节点出发到达词w所对应叶子节点的路径；（2）$l^w$为$p^w$上所包含的节点个数；（3）${d_j}^w$代表着$p^w$中第j个节点对应的编码，左节点编码为0，右节点编码为1。
现在继续考虑之前的优化目标（1.1），根据乘法公式，可以将其展开为
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/7.jpg)
将网络节点替换为图6中所使用的词向量后，优化目标就变成了
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/8.jpg)
基于Hierarchical Softmax的Skip-gram模型中是这样来表示在已知中心词$x^w$求其上下文词的概率，即$\operatorname{Pr}\left(u | x_{w}\right)$：以图6为例，从中心词$x^w$所对应的根节点开始形成到一叶节点$x_i$的路径$p^i$，在$p^i$中从根节点开始每遇到一个非叶节点就要做一次二分类，使用逻辑回归分别计算出到该非叶节点2个孩子的概率，规定该飞叶子节点到其左边孩子节点的概率为$1-\sigma\left(x_{w}^{T} \theta\right)$，到其右边孩子节点的概率为$\sigma\left(x_{w}^{T} \theta\right)$，将$p^i$所有经过节点的概率相乘，就得到了$\operatorname{Pr}\left(x_{i} | x_{w}\right)$。
但是这里得到的是$\operatorname{Pr}\left(x_{i} | x_{w}\right)$，$x_i$只是语料中心词w上下文的一个，若我们对上下文所有词都进行这样的计算，同时将目标函数（1.3）进行最大化，再经过softmax归一化后得到的将是语料中每个词成为中心词w上下文的概率，概率最大的2w个词即可作为预测出的上下文。
但是我们的任务是获得词向量，研究目标函数的优化过程可以发现，所需的词向量其实只是优化过程中产生的一个副产品，所以为了获得词向量并不需要完整的Skip-gram模型，优化过程如下：对目标函数(1.3)使用随机梯度上升算法进行最大化，可以得到参数xw和θ的更新公式为：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/9.jpg)
**由此可得基于Hierarchical Softmax的Skip-gram模型运作流程总结如下：**
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/10.jpg)
这是根据文献【1】中词嵌入技术发明者提出skip-gram模型的理论实现方案，由流程中的c)可得该模型运行一次仅能得出中心词w的词向量，嵌入效率低于能一次更新所有上下文词向量的CBOW模型。在之后的word2vec技术实现中，根据上下文的作用是相互的，期望最大化$\operatorname{Pr}\left(u | x_{w}\right)$等同于期望最大化$\operatorname{Pr}\left(x_{w} | u\right)$，因此将优化目标由变成了$\operatorname{Pr}\left(x_{w} | u\right)$。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/11.jpg)
如图7所示，Huffman树的输入变成了上下文中的词的向量xi，目标路径通往中心词w对应的节点。优化后的基于Hierarchical Softmax的Skip-gram模型运作流程如下：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/12.jpg)

## 5. Deepwalk算法流程
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/13.jpg)
## 6. OpenNE中Deepwalk算法实现流程
在OpenNE中Deepwalk算法的实现过程中，将上述流程做了些调整，加入了随机游走的并行化处理，并将Huffman树的建立放在了获得所有的游走序列后，根据随机游走中的出现过的节点建立Huffman树并进行训练。
>源码解析见[OpenNe源码解析之DeepWalk
](https://yunlongs.cn/2019/01/24/NE-Deepwalk/)

![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/OpenNe/Deepwalk/14.jpg)