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

在原论文中**只是用了gcc编译**，所以本次baseline评估使用的数据集规模如下：
| |Training|Validation|Testing|total|
|--|--|--|--|--|
|arm| | | | 44668|
|x86| | | | 44972|
|mips| | | | 44822|
|total(func)| 5088| 637|636 | |

测试集上的结果：
```
step 000: Loss: 0.715, Accuracy: 80.000%
step 100: Loss: 1.495, Accuracy: 80.000%
step 200: Loss: 1.465, Accuracy: 80.199%
step 300: Loss: 1.455, Accuracy: 80.399%
step 400: Loss: 1.451, Accuracy: 80.349%
step 500: Loss: 1.434, Accuracy: 80.639%
step 600: Loss: 1.409, Accuracy: 81.248%
step 700: Loss: 1.403, Accuracy: 81.241%
step 800: Loss: 1.391, Accuracy: 81.573%
step 900: Loss: 1.372, Accuracy: 81.865%
step 1000: Loss: 1.368, Accuracy: 81.858%
step 1100: Loss: 1.368, Accuracy: 81.826%
step 1200: Loss: 1.357, Accuracy: 81.957%
step 1300: Loss: 1.357, Accuracy: 81.945%
step 1400: Loss: 1.348, Accuracy: 82.077%
step 1500: Loss: 1.345, Accuracy: 82.099%
step 1600: Loss: 1.333, Accuracy: 82.286%
step 1700: Loss: 1.333, Accuracy: 82.246%
step 1800: Loss: 1.333, Accuracy: 82.210%
step 1900: Loss: 1.336, Accuracy: 82.189%
step 2000: Loss: 1.335, Accuracy: 82.254%
```
可以看出，准确率还挺高。


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