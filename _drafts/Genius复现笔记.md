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


## 实验改进

但是在实验中我们发现上面**相似性计算公式有问题** ，问题就出现在上面公式用作**归一化的分母上**，他使用的是具有**最多节点的图的节点个数 来归一化** 。在一般情况下，例如下图（左），两个**不怎么相似**的图 G1 和 G2 之间的最小 cost 匹配分别是(node1,node5)和(node2,node6)
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/98.png)

根据此相似度计算如下：
$$
\kappa(g_1,g_2) = 1 - \frac{cost(g_1,g_2)}{5}=1-\frac{0.5+0.5}{5} = 0.8
$$

但如果这时如果将上图中的G2添加95个节点，cost最小的匹配关系不变，那么此时的相似度计算如下：
$$
\kappa(g_1,g_2) = 1 - \frac{cost(g_1,g_2)}{100}=1-\frac{0.5+0.5}{100} = 0.99
$$
**随着G2的节点的个数越来越多，G2与G1相似的可能性越来越低了，但是通过上面公式计算出来的相似度却越来越高！！**，这是因为上面公式归一化的是两个图之间的代价，并不是最后的相似度。

-----
针对上面问题的解决方案可以是**将相似度计算公式改用最小的节点归一化**，即将公式中的max换成min
$$\kappa\left(g_{1}, g_{2}\right)=1-\frac{\operatorname{cost}\left(g_{1}, g_{2}\right)}{\min \left(\operatorname{cost}\left(g_{1}, \Phi\right), \operatorname{cost}\left(\Phi, g_{2}\right)\right)}$$   

这样的话，针对上面的场景，我们的相似度计算都是0.5
$$
\kappa(g_1,g_2) = 1 - \frac{cost(g_1,g_2)}{2}=1-\frac{0.5+0.5}{2} = 0.5
$$
但是，现在仍然存在问题，因为上面G2的节点个数由6增加到了100，显然的和G1的不相似程度也加大了，但是上面计算的相似性分数却不变。

为此，我们可以再乘以两个图大小的比值，这样就可以将两个图之间节点个数的差异也考虑进去。
$$\kappa\left(g_{1}, g_{2}\right)=(1-\frac{\operatorname{cost}\left(g_{1}, g_{2}\right)}{\min \left(\operatorname{cost}\left(g_{1}, \Phi\right), \operatorname{cost}\left(\Phi, g_{2}\right)\right)})\times \frac{\min \left(\operatorname{cost}\left(g_{1}, \Phi\right), \operatorname{cost}\left(\Phi, g_{2}\right)\right)}{\max \left(\operatorname{cost}\left(g_{1}, \Phi\right), \operatorname{cost}\left(\Phi, g_{2}\right)\right)}$$  
现在，针对上面两种情况计算的相似性分数就为：
$$
\kappa(g_1,g_2) = (1 - \frac{cost(g_1,g_2)}{2})\times (\frac{2}{5})=(1-\frac{0.5+0.5}{2})\times (\frac{2}{5}) = 0.2
$$
$$
\kappa(g_1,g_2) = (1 - \frac{cost(g_1,g_2)}{2})\times (\frac{2}{100})=(1-\frac{0.5+0.5}{2})\times (\frac{2}{100}) = 0.02
$$
可以看出，这样相似度之间的差距就可以区分出来了。

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
