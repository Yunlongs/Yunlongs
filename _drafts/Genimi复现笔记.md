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



## Experiment 2
>这里先说明下，对本实验结果并不如论文中所述的猜测：在对数据集的采样上，我们是根据函数名来进行采样，这样就意味着由相同源代码函数编译得到的不同的二进制函数仅会在一个划分过的数据集上，所以训练的时候模型是不知道任何关于测试集函数的内容的，这样训练起来会更难一些。然而有可能他们在实现的过程中，进行的是随机采样，所以测试集的中会有一部分函数和训练集中的函数其实是同一函数名。

这里**再加上clang的数据集进行训练**
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 90300|
|x86| | | | 90344|
|mips| | | | 90240|
|total(func)| 5346| 669|668 | |
```
step 000: Loss: 1.375, Accuracy: 80.000%
step 100: Loss: 1.358, Accuracy: 81.485%
step 200: Loss: 1.310, Accuracy: 82.289%
step 300: Loss: 1.324, Accuracy: 82.392%
step 400: Loss: 1.354, Accuracy: 81.845%
step 500: Loss: 1.338, Accuracy: 81.816%
step 600: Loss: 1.347, Accuracy: 81.930%
step 700: Loss: 1.368, Accuracy: 81.697%
step 800: Loss: 1.376, Accuracy: 81.760%
step 900: Loss: 1.371, Accuracy: 81.731%
step 1000: Loss: 1.376, Accuracy: 81.658%
step 1100: Loss: 1.385, Accuracy: 81.599%
step 1200: Loss: 1.392, Accuracy: 81.565%
step 1300: Loss: 1.392, Accuracy: 81.507%
step 1400: Loss: 1.396, Accuracy: 81.399%
step 1500: Loss: 1.405, Accuracy: 81.299%
step 1600: Loss: 1.413, Accuracy: 81.168%
step 1700: Loss: 1.426, Accuracy: 81.076%
step 1800: Loss: 1.431, Accuracy: 81.066%
step 1900: Loss: 1.438, Accuracy: 80.953%
step 2000: Loss: 1.443, Accuracy: 80.815%
----------------------------
```


这里选了一些的实验结果出来，明显好多了
```
frist query hwcrhk_log_message
hwcrhk_log_message
hwcrhk_log_message
hwcrhk_log_message
hwcrhk_log_message
hwcrhk_log_message
ec_GFp_simple_point_set_affine_coordinates
ec_GFp_simple_point_set_affine_coordinates
NCONF_load_fp
EVP_PKEY_get1_DH
EC_POINT_set_affine_coordinates_GF2m
----
hwcrhk_log_message
hwcrhk_log_message
UI_get_result_minsize
UI_get_result_minsize
UI_get_result_minsize
UI_get_result_minsize
cms_encode_Receipt
hwcrhk_log_message
hwcrhk_log_message
hwcrhk_log_message
-------
-------
frist query cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
cb_leak_LHASH_DOALL_ARG
OCSP_crl_reason_str
EVP_MD_CTX_clear_flags
----
EVP_seed_cfb128
EVP_aes_256_ctr
TLSv1_2_server_method
EVP_aes_192_ccm
EVP_mdc2
X509_get_default_cert_area
TLSv1_2_server_method
EVP_sha512
SSL_cache_hit
EVP_aes_256_cbc
```

```
top1 recall: 0.681
top10 recall: 0.29196666666666704
top25 recall: 0.17789944444444455
top50 recall: 0.13288111953694395
top75 recall: 0.154174651644963
top100 recall: 0.17020104469285516
top125 recall: 0.18606709198893773
top150 recall: 0.20042879592489513
top175 recall: 0.2137407060267548
top200 recall: 0.2256441322367937
```


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

![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/120.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/121.png)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/122.png)

![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/123.png)


## Experiment 3
这里对cfg中最小的节点设了一个阈值，min_nodes_threshold>=3。
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 26061|
|x86| | | | 27518|
|mips| | | | 27487|
|total(func)| 3287| 412|410 | |