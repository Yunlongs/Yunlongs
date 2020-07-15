---
layout:     post
title:      VulSeeker-Pro:Enhanced Semantic Learning Based Binary Vulnerability Seeker with Emulation
subtitle:   二进制代码相似性检测
date:       2020-07-13
author:     Yunlongs
catalog: true
tags:
    - 二进制代码相似性检测
    - 深度学习
---

## VulSeeker-Pro:Enhanced Semantic Learning Based Binary Vulnerability Seeker with Emulation

|期刊/会议： |ESEC/FSE ’18|
| ---|---|
|发表时间：|2018年11月4|
|发表机构：|Tsinghua University|


### 一、前言
这篇文章说是VulSeeker的升级版，但是却跟VulSeeker没有多大的关系，只是在之前特征相似性判别网络的结果后，使用动态分析的方法来 提高准确率。

当然，与此方法做对照试验的还是Gemini，指出了Gemini在现实中进行漏洞搜索时的准确率太低，真实样本的top rank排名不靠前的问题。

为此，VulSeeker Pro首先使用Gemini之类的相似性判别矩阵初步的选出相似性靠前的top-M个函数，然后在过滤后的结果上利用动态执行的方法来进一步的选出最好的top-N个结果。

### 二、VULSEEKER-PRO DESIGN
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/151.png)
如上图所示，VulSeeker-Pro主要包含如下两个模块：基于semantic learning的相似性预测，动态仿真引擎。

VulSeeker-Pro 利用语义学习模型的快速预测能力来得到初始的top-M个候选函数，以此来过滤掉那些非常不相似的函数。然后基于函数的动态执行路径来生成top-N个候选函数最为最后的预测结果。

#### 2.1 基于semantic learning的相似性预测器
这里只要是像Genimi、VulSeeker、binaryAI之类的神经网络预测器都可以。

论文中使用的是Gemini来做实验。

#### 2.2 Emulation Engine
##### 2.2.1. 参数识别
在对函数的执行进行仿真之前，需要先识别出函数的参数，可以使用IDApython来提取。

#### 2.2.2 函数仿真
在进行函数仿真之前，先生成一系列的随机整数来进行参数分配，然后使用PyVex来将每个汇编函数转化成VEX-IR的形式来更方便的进行函数仿真。

在分配完参数后，开始对此函数进行仿真，在仿真执行的过程中，记录下其动态执行路径（这里称作为语义指纹）。另外当仿真函数A时，若调用了一个函数B，那么也进入函数B中进行仿真，记录下其指纹，这样可以一定程度的解决函数内联问题。

VulSeeker-Pro的动态语义指纹包括：输入值、输出值、比较指令的操作码/操作数、库函数调用。

图3展示了仿真过程中的指纹记录流程。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/152.png)

*输入值*包括分配的参数值和从data段(eg.rodata,data)读取的数据。
*输出值*包括函数的返回值和写入内存的值
*比较指令操作码*是哪些根据条件进行跳转的操作码和对应的操作数
*库函数调用*为C语言标准库的调用名。

#### 2.2.3 相似性计算
在得到之前Top-M个候选函数的动态语义指纹后，使用Jaccard系数来计算它们的相似性，排序后选Top-N个作为输出结果。

### 三、实验结果
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/153.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/154.png)