# Genimi

## Baseline 实验设置
### 数据集
openssl-1.0.1a和openssl-1.0.1f，在x86,arm,mips架构下，用编译器clang和gcc，优化选项O0-O3编译。
获得的数据集个数如下：
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 90300|
|x86| | | | 90344|
|mips| | | | 90240|

## Experiment 1
openssl-1.0.1a和openssl-1.0.1f，在x86,arm,mips架构下，用编译器clang和gcc，优化选项O0-O3编译。
在原论文中**只是用了gcc编译**，所以本次baseline评估使用的数据集规模如下：
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 44668|
|x86| | | | 44972|
|mips| | | | 44822|
|total(func)| 5088| 637|636 | |

![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/128.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/129.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/130.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/131.png)



## Experiment 2
>~~这里先说明下，对本实验结果并不如论文中所述的猜测：在对数据集的采样上，我们是根据函数名来进行采样，这样就意味着由相同源代码函数编译得到的不同的二进制函数仅会在一个划分过的数据集上，所以训练的时候模型是不知道任何关于测试集函数的内容的，这样训练起来会更难一些。然而有可能他们在实现的过程中，进行的是随机采样，所以测试集的中会有一部分函数和训练集中的函数其实是同一函数名。~~ 后来发现自己在对neighbor 的embed layer多加了一个relu，并设置min_nodes_threshold后效果提升巨大。

这里**再加上clang的数据集进行训练**
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 90300|
|x86| | | | 90344|
|mips| | | | 90240|
|total(func)| 5346| 669|668 | |




感觉这实验还是比较离谱，所以，这里**重新说明一下论文中的Baseline设置：**
1. 将所有的数据集按照811的比例划分为训练集、验证集、测试集，并保证任何两个集合之间没有相同原代码的函数
2. 对于每个训练集中的函数，随机选一个正样本和负样本，组成训练集样本对

**训练细节：**
1. Adam learning rate为0.0001
2. 100 epochs
3. mini batch 10
4. embedding size 64,embedding depth 2,T =5
5. 保存在验证集上AUC最高的模型

**Baseline evalute accuracy**:
1. 测试集取样的方式和训练集一样
2. 测试ROC曲线
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/124.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/125.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/126.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/127.png)


## Experiment 3
这里对cfg中最小的节点设了一个阈值，min_nodes_threshold>=3。
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 26061|
|x86| | | | 27518|
|mips| | | | 27487|
|total(func)| 3287| 412|410 | |