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