# Genius

1 `LoadFuncs`从文件中提取所有的函数名
输入：/path/func_candid
格式要求：一行一个函数名，以\n结尾
```
func1\n
func2\n
...
```
2.`retrieveFeatures(n, base_dir, filename, funcs):`从目标路径中获取feature
输入参数：
```
n:第几个文件
base_dir : 输入训练语料目录
filename: target function
funcs: 函数名 （未用）
```
路径规则：
`basedir/5000/filename_cbn.feature`
输入文件格式要求：字典形式
```
func1:feature1
func2:feature2
```

3.`retrieveVuldb(base_input_dir)`获得漏洞数据库

### 实验记录
#### Accuracy
oneline search top 10的准确度
1. 我修改的公式：
```
total accury: 0.36

```
2. genius自身的
total accury: 0.34

top 100
1. 修改的
0.318 0.268

2. genius
0.324 0.279

top 1000
1. 0.2906
2. 0.2937
#### efficiency
top 100
96s

1012

## 实验设置
### Baseline evaluate
这里的baseline实验主要有两个，第一个是在Dataset I上与DiscovRe的比较：

**第一个实验：** 
Baseline 数据集的组成：从Dataset I总随机取样1w个函数，但是要满足每个函数至少有一个query实例和search 实例。

从baseline 数据集上随机选取1000个函数加入到Query集合中baseline 数据集剩下的都作为codebase。然后用这1000个Query set作为query在target 中进行寻找。

>在实验过程中，发现，若是将所有得语料当作codebase来训练得话，内存会爆炸，所以应该是1000个函数除去query剩下得作为codebase。

需要记录下，每个query的Top-K召回率，然后取平均。