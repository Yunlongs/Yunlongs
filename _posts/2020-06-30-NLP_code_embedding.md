---
layout:     post
title:      A Cross-Architecture Instruction Embedding Modelfor Natural Language Processing-Inspired Binary Code Analysis
subtitle:   二进制代码相似性检测
date:       2020-06-30
author:     Yunlongs
catalog: true
tags:
    - 二进制代码相似性检测
    - 深度学习
---


## A Cross-Architecture Instruction Embedding Modelfor Natural Language Processing-Inspired Binary Code Analysis
|期刊/会议： |NDSS19 BAR workshop|
| ---|---|
|发表时间：|2019年|
|发表机构：|South Carolina|

### 前言
这篇文章算是INNEREYE-BB的续作，但是主要的提升点在于跨机构的指令嵌入。利用指令序列的上下文信息来学习同架构下指令的相似性，使用语义等价的指令序列对来学习跨机构下指令的相似性。

### 跨架构指令嵌入模型
#### 设计目标
构建指令嵌入模型需要实现两个目标：单架构相似性目标，和跨架构语义相似性目标。

**单架构相似性**指的就是同一指令集内语义相近的指令在向量空间中的表征也相近。**跨架构相似性**是指不同指令集之间语义相近的指令其在向量空间中的表征也相近。

#### 系统总览
作者使用的跨机构指令嵌入方法借鉴了"Bilingual word representations with monolingual quality in mind"这篇文章中的*联合学习*方法，其主要包括单架构成分和多架构成分。

**单架构部分**利用相同架构下输入指令序列的上下文共现信息；**多架构部分**从不同架构的指令序列对中学习语义等价的信息。

**联合目标函数**：
$$J=\gamma \sum_{i=1}^{N} J\left(\operatorname{Mono}_{a_{i}}\right)+\beta \sum_{i=1}^{N-1} \sum_{j=i+1}^{N} J\left(\text { Multi } <a_{i}, a_{j}>\right)$$

在上式中，每个单架构成分$Mono_{a_i}$ 为针对架构$a_i$来捕捉其指令的聚类属性。J为目标函数。多架构成分$Multi<a_i,a_j>$被使用来学习多架构间的语义关系。超参数r和B用来平衡这两个之间的影响。

例如，如果只考虑两个结构的目标函数的话，x86和arm，上面的联合目标函数就为
$$J=\gamma\left(J\left(\operatorname{Mono}_ {x 86}\right)+J\left(\operatorname{Mono}_{A R M}\right)\right)+\beta J(\operatorname{Multi} <x 86, A R M>)$$

>此工作中的指令序列是一个基本块，因为我们把指令看作单词，基本块看作句子。这里不采用函数为基本单位的原因是，函数中的指令并不是顺序执行的。

为了解决包外指令的影响，需要先对指令数据进行预处理：
1. 数字常量用0替换，但正负号保留。
2. 字符串换成<STR>
3. 函数名称换成FOO
4. 其他符号常量换成<TAG>

#### 单架构部分目标函数
在处理单架构指令嵌入的目标函数时，作者利用了CBOW的训练方法，这里设当前指令$e_t$的上下文为其前n个和后n个指令， 那么根据CBOW模型， 我们所需要的目标函数就为

$$J=\frac{1}{T} \sum_{t=1}^{T} \log P\left(e_{t} \mid e_{t-n}, \ldots e_{t-1}, e_{t+1}, \ldots, e_{t+n}\right)$$
其中$T$为指令序列的长度，n为滑动窗口的大小。

#### 多架构部分目标函数
这一部分作者仍然使用CBOW来进行学习，但是对CBOW进行了一些扩展。

![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/104.png)
如上图展示了跨机构指令嵌入模型的工作方法。首先输入一对分别在x86和arm编译下语义相等的基本块指令序列，为了能够进行跨架构的指令预测，作者使用一个架构下的上下文来预测另一个架构下的指令。

比如说上图，我们知道`moveq [rip+<tag>],rax`在arm下对等的指令为`str r0,[r7]`，我们使用arm下`str r0,[r7]`的上下文`bl foo and cmp r0,0`来预测`moveq [rip+<tag>],rax`。

但是这又同样引出了另一个问题:怎么样找到不同架构之间指令序列的对等关系呢？
这里给出两种解决方案：
（1）假设不同架构的指令序列是一种线性对齐关系的，因此，在序列M中第i个位置上的指令对应的是序列N中第$i \times |N|/|M|$个指令。
（2）通过指令中包含的操作码来确定指令间的对齐关系。

但是在此方法中，作者只采用了第一种方法。

### 实验评估
#### 单架构指令相似性任务
**指令相似性测试：** 作者手工创建了一些指令对，来测试这些指令对之间的相似性，并随机选择了50个相似、50个不相似对，其ROC曲线如图：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/105.png)

**最近邻指令**：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/106.png)

#### 跨架构指令相似性任务
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/107.png)