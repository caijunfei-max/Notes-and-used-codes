# Scripts and tutorials

用于保存

1. 一些日常工作学习中常用的脚本
2. 某些教程的集合



## 目录说明：

1. history: 记录科研过程中用到的软件和笔记
2. mac_tutorial：使用mac时的些许问题和搜集来的答案
3. scripts_bash：常使用到的bash脚本
4. scripts_python：常使用到的python代码
5. note_tutorial: 笔记和教程

每个文件建议放在系统设置的路径里面，这样可以成为一个常用的命令。



# 服务器设置

一些比较个人的设置和环境配置，不一定适用每个人





# 批量工作

哥们是真不想做重复性工作了T^T

## Linux shell批量操作

文件位置：scripts_bash/batch_x.sh

功能是当前在当前目录下的所有目录进行同样的操作

用法很简单，在第四行(cd "$dir" || continue)之后和地9行(cd \$CURRENT_DIR)之前输入需要进行的命令就行了



举个例子，批量使用vaspkit生成vasp输入文件，然后提交脚本

```bash
  1 #!/bin/bash
  2 CURRENT_DIR=$(pwd)
  3 for dir in *; do
  4     cd "$dir" || continue
  5
  6     echo -e "102\n2\n0.04\n" | vaspkit
  7     sbatch run.sh
  8
  9     cd $CURRENT_DIR
 10 done

```

这样就会进入所有目录提交任务啦。



## 生成提交脚本（未名一号）

文件：scripts/jobfile.sh

用于生成提交脚本，放到路径里面之后，在未名一号应该可以无缝使用。其他位置自己改改还能用

按照提示输入内容就行。可以搭配echo -e和batch_x.sh实现批量命名和批量提交。



# VASP输入文件

大部分的输入文件都只要vaspkit就能提供，但是有一些需要重复性操作或者重复建模的实在很烦，因此用一点点脚本偷偷懒是非常合理滴！

## INCAR

### 自动加U

文件位置：scripts_python/plusu

在工作路径下面存在INCAR、POSCAR的情况下，运行plusu，可以自动在INCAR中进行加U。具体U值可以自己在脚本中设定：

在脚本的第九行开始（如下），按照同样格式进行加入U值或者是修改U值。对于这个字典中没有的元素，会自动给一个U=0的矫正。已经设置的U值基本来自文献~
```
uValue = {"Cu":4.0, "Ni": 6.0, "Mn": 4.38, "Ag":1.5, "Ru": 4.0, 
        "Mo": 4.4, "Nb": 1.5, "Co": 3.4, "Fe": 4.0, "Cr": 3.5, 
        "Ti": 6.6, "Zr":5.0, "In":7.0, "Y": 5.0}
```



## POSCAR

### 自动生成全脱锂结构

文件位置：scripts_python/get_charged.py

非常简单的脚本，删除所有锂离子，获得一个charged_POSCAR
