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



## 实验设置
### Baseline evaluate
这里的baseline实验主要有两个，第一个是在Dataset I上与DiscovRe的比较：

**第一个实验：** 
Baseline 数据集的组成：从Dataset I总随机取样1w个函数，但是要满足每个函数至少有一个query实例和search 实例。

从baseline 数据集上随机选取1000个函数加入到Query集合中baseline 数据集剩下的都作为codebase。然后用这1000个Query set作为query在target 中进行寻找。

>在实验过程中，发现，若是将所有得语料当作codebase来训练得话，内存会爆炸，所以应该是1000个函数除去query剩下得作为codebase。

需要记录下，每个query的Top-K召回率，然后取平均。

#### 实验记录
Baseline的数据集按照上面的设置进行生成，但是这里只取了节点个数小于100的函数来生成数据集。

结果最后的实验很不理想，下面是记录的实验结果：
这里举一个例子进行分析
- 我们选用的query函数为“openssl-101a_x86_gcc_O2_openssl-level_find_node”
- 在训练集中与query对应的函数为“openssl-101a_arm_clang_O0_openssl-level_find_node”
- 但是通过LSH返回的函数为“openssl-101f_mips_clang_O0_openssl-DES_ede3_ofb64_encrypt”

这三个函数所经过VLAD后的编码特征如下所示：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/99.png)
可以看到，第一行和第二行分别为我们的query和target，但是特征编码的差异却很大。
下面计算出了query和这两个函数的欧几里得距离，但奇怪的是返回的距离比较大的"openssl-101f_mips_clang_O0_openssl-DES_ede3_ofb64_encrypt”这个函数，正确的应该是要返回训练集中的target函数。
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/100.png)
