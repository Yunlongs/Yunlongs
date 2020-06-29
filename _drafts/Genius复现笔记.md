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

>~~在实验过程中，发现，若是将所有得语料当作codebase来训练得话，内存会爆炸，所以应该是1000个函数除去query剩下得作为codebase。~~
错了！对于那些不能scalable的方法，我们才取1w个作为baseline。对于本方法，应当是除了query外所有的函数全部进行训练。所以从下面的实验结果可以看出来，在同样的数据集规模下，该方法在准确率上的提升并没有那么大！

需要记录下，每个query的Top-K召回率，然后取平均。

#### 实验记录
Baseline的数据集按照上面的设置进行生成，但是这里只取了节点个数小于100和大于3的函数来生成数据集。

**这里展示的是跨编译器和优化选项的结果，数据集均是x86下openssl的**
首先，我们将query中随机抽选10个来进行search，其中有3个返回了正确的结果，并且均是top3。
```
for the 99st query:  openssl-101a_x86_clang_O3_openssl-BN_GF2m_mod_mul  accuracy: 0.01
funcname: openssl-101a_x86_clang_O3_openssl-BN_GF2m_mod_exp  distance: 0.0002481410293551007
funcname: openssl-101a_x86_gcc_O1_openssl-BN_GF2m_mod_mul  distance: 0.014597954434989562

for the 99st query:  openssl-101a_x86_clang_O1_openssl-OCSP_archive_cutoff_new  accuracy: 0.01
funcname: openssl-101a_x86_clang_O3_openssl-PEM_ASN1_read_bio  distance: 0.029056688820376143
funcname: openssl-101a_x86_clang_O2_openssl-d2i_X509_AUX  distance: 0.02962471064099212
funcname: openssl-101a_x86_gcc_O1_openssl-OCSP_archive_cutoff_new  distance: 0.030663739619894628

for the 99st query:  openssl-101a_x86_clang_O1_openssl-print_error  accuracy: 0.01
funcname: openssl-101a_x86_clang_O2_openssl-print_error  distance: 0.0
```
>因为我们对于每个query，在进行的search数据库中可能只有一个正确的匹配,而且上面的结果平别进行了跨平台、编译器，初步来看，Genius的确能起到一些作用。

在此测试集上的结果
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/101.png)
```
top 1  recall: 8.62189576775096
top 25  recall: 15.937390696047565
top 50  recall: 17.651276670164393
top 75  recall: 19.3389296956978
top 100  recall: 20.36201469045121
top 125  recall: 21.09129066107031
top 150  recall: 21.78384050367262
top 175  recall: 22.3539699195523
top 200  recall: 23.088492479888078
top 1000  recall: 29.375655823714595
total time: 669.6987557411194

```

针对openssl的所有跨架构、编译器、优化选项的实验结果：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/102.png)
```
top 1  recall: 5.340048209366395
top 25  recall: 9.201224911452186
top 50  recall: 10.070961235733963
top 75  recall: 11.056793585202671
top 100  recall: 12.062303227075951
top 125  recall: 12.342950609996063
top 150  recall: 12.662460645415191
top 175  recall: 13.044692050373866
top 200  recall: 13.469967532467528
total time: 281.4467844963074

Process finished with exit code 0

```

下面是使用自己修正过的第三种相似性计算方法（包含了节点比例）的实验结果：
![](https://yunlongs-1253041399.cos.ap-chengdu.myqcloud.com/image/Similary_Detection/103.png)
```
top 1  recall: 5.6718120479588405
top 25  recall: 12.158997136061355
top 50  recall: 15.12729964564827
top 75  recall: 17.328285034707054
top 100  recall: 19.057205960875685
top 125  recall: 20.300228144264842
top 150  recall: 21.62807630697539
top 175  recall: 22.742585311392652
top 200  recall: 23.52555701179555
total time: 1181.8974475860596
```