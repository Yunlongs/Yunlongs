# VulSeeker 复现笔记

## Experiment 1
这里采用和Genimi Baseline 一样的设置。
openssl-1.0.1a和openssl-1.0.1f，在x86,arm,mips架构下，用编译器gcc，优化选项O0-O3编译。**min_nodes_threshold = 3**
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
多加了clang
arm :52200
x86 :55094
mips :55037
train dataset's num =3301 ,valid dataset's num=414 , test dataset's num =412