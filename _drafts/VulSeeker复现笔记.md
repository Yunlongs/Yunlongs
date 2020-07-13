# VulSeeker 复现笔记

## Experiment 1
### 1.1 实验设置
这里采用和Genimi Baseline 一样的设置。
openssl-1.0.1a和openssl-1.0.1f，在x86,arm,mips架构下，用编译器gcc，优化选项O0-O3编译。**min_nodes_threshold = 3** （与实验2相比少了一个clang）
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 26135|
|x86| | | | 27586|
|mips| | | | 27551|
|total(func)| 3294| 413|411 | |

test step 1900: Loss: 1.067, Accuracy: 86.013%, AUC: 0.932
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/132.png)

![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/133.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/134.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/135.png)


## Experiment 2
### 2.1 实验设置：
```
## choose what binary you want to generate the dataset
version = ["openssl-101a","openssl-101f"]
arch = ["arm","x86","mips"]
compiler = ["gcc","clang"]
optimizer = ["O0","O1","O2","O3"]

### some details about dataset generation
max_nodes = 200
min_nodes_threshold = 3
Buffer_Size = 1000
mini_batch = 10
vulseeker_feature_size = 8（no of str,no of constant,...）

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
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 52200|
|x86| | | | 55094|
|mips| | | | 55037|
|total(func)| 3301| 414|412 | |

### 实验结果
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_2.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_3.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_4.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/experiment_result/Figure_1.png)