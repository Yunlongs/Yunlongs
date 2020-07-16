# Genimi

## Baseline 实验设置
### 数据集

这实验还是比较离谱，所以，这里**重新说明一下论文中的Baseline设置：**
1. 将所有的数据集按照811的比例划分为训练集、验证集、测试集，并保证任何两个集合之间没有相同原代码的函数
2. 对于每个训练集中的函数，随机选一个正样本和负样本，组成训练集样本对

**训练细节：**
1. Adam learning rate为0.0001
2. 100 epochs
3. mini batch 10
4. embedding size 64,embedding depth 2,T =5
5. 保存在验证集上AUC最高的模型




## Experiment 1(Baseline)
### 1.1 实验目标
根据论文中的baseline设置，来测试Gemini的baseline能力

### 1.2 实验设置
openssl-1.0.1a和openssl-1.0.1f，在x86,arm,mips架构下，用编译器clang和gcc，优化选项O0-O3编译。
在原论文中**只是用了gcc编译**，所以本次baseline评估使用的数据集规模如下：
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 26061|
|x86| | | | 27518|
|mips| | | | 27487|
|total(func)| 3287| 412|410 | |
```
## choose what binary you want to generate the dataset
version = ["openssl-101a","openssl-101f"]
arch = ["arm","x86","mips"]
compiler = ["gcc"]
optimizer = ["O0","O1","O2","O3"]
dir_name  = "../dataset/extracted-acfg/"

### some details about dataset generation
max_nodes = 500
min_nodes_threshold = 3
Buffer_Size = 1000
mini_batch = 10
```

### 1.3 实验结果
test step 1900: Loss: 0.994, Accuracy: 88.112%, AUC: 0.946

## Experiment 2
### 2.1 实验目标
将`min_nodes_threshold`设为0，与实验1做对比，观察小节点对方法的影响有多大。

### 2.2 实验设置
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 44668|
|x86| | | | 44972|
|mips| | | | 44822|
|total(func)| 5088| 637 | 636 | |
```
## choose what binary you want to generate the dataset
version = ["openssl-101a","openssl-101f"]
arch = ["arm","x86","mips"]
compiler = ["gcc"]
optimizer = ["O0","O1","O2","O3"]
dir_name  = "../dataset/extracted-acfg/"

### some details about dataset generation
max_nodes = 500
min_nodes_threshold = 0
Buffer_Size = 1000
mini_batch = 10

step_per_epoch = 15000
valid_step_pre_epoch = 3000
test_step_pre_epoch = 3000
```
>这里感觉增大数据集的话，有点不太公平，所以就使用和实验室相同规模的数据集进行训练，但是测试使用全部的进行测试

### 2.3 实验结果
test step 3000: Loss: 1.244, Accuracy: 84.199%, AUC: 0.904

## Experiment 3
### 3.1 实验设置
添加最小阈值`min_nodes_threshold=3，max_nodes=500`
```
version = ["openssl-101a","openssl-101f"]
arch = ["arm","x86","mips"]
compiler = ["gcc","clang"]
optimizer = ["O0","O1","O2","O3"]

### some details about dataset generation
max_nodes = 500
min_nodes_threshold = 3
Buffer_Size = 1000
mini_batch = 10

### some params about training the network
learning_rate  = 0.0001
epochs  = 100
step_per_epoch = 30000
valid_step_pre_epoch = 3800
test_step_pre_epoch = 38000
T = 5
embedding_size = 64
embedding_depth = 2
```
这里对cfg中最小的节点设了一个阈值，min_nodes_threshold>=3。
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 52245|
|x86| | | | 54952|
|mips| | | | 54895|
|total(func)| 3293| 413|411 | |

### 3.2 实验结果
test step 38000: Loss: 1.135, Accuracy: 85.890%, AUC: 0.931
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_9.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_10.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_11.png)

## Experiment 4
### 4.1 实验设置
更改`min_nodes_threshold=10`
```
version = ["openssl-101a","openssl-101f"]
arch = ["arm","x86","mips"]
compiler = ["gcc"]
optimizer = ["O0","O1","O2","O3"]

### some details about dataset generation
max_nodes = 500
min_nodes_threshold = 3
Buffer_Size = 1000
mini_batch = 10

### some params about training the network
learning_rate  = 0.0001
epochs  = 100
step_per_epoch = 15000
valid_step_pre_epoch = 1900
test_step_pre_epoch = 1900
T = 5
embedding_size = 64
embedding_depth = 2
```


### 4.2 实验结果
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_6.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_7.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_8.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_5.png)
