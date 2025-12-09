README: 记录一些在科研过程中遇到的error问题解决办法



# Linux

## bash: python^M: bad interpreter: No such file or directory

windows编写的脚本放到linux之后如果转化到bin里面做脚本，会出现不可见字符导致的解释器异常。需要把文件格式改掉。

直接在vim里面改就行，将文件格式从dos改成unix。

修改方式如下：

1. vim命令模式，输入“: set ff”或者“: set fileformat”查看文件格式
2. 如果显示“fileformat=dos 或 fileformat=dos”，则需通过"set ff=unix",将文件格式改掉就可以正常在linux里面运行。



# Windows

## Win11右键卡死

直接将右键菜单改回win10

用管理员权限打开powershell

然后输入引号内的内容

"reg add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve"



## power shell “conda init”  出现错误

```powershell
no action taken
```

因为

powershell的profeile.ps1文件路径中存在中文，所以conda init powershell 没有办法找到profile文件，初始化才会失败，可以直接用管理员权限打开，然后对所有用户和终端进行初始化:

```
coda init --system --all
```





# Git

## "warning: LF will be replaced by CRLF"

使用git来add含有ipynb或者其他相关文本的文件时，会出现<font color=red>"warning: LF will be replaced by CRLF"</font>的报错，原因是因为windows上面编辑器的换行文本协议问题，可以通过在git上敲以下代码解决：

```python
git config --global core.autocrlf true
```

即，打开自动识别换行并转化为回车或换行的功能。

源：https://blog.csdn.net/u012757419/article/details/105614028



# Vasp

## num prob rmm

使用IALGO = 48的时候，如果体系是金属体系，使用Gaussian smearing(ISMEAR = 0)会导致此错误，因此可以改用ISMEAR=-1,此方法同时适用于。此错误的解决的方法是使用quasi newton算法（RMM-DIIS, IBRION=1）时好用，如果是共轭梯度下降算法出现这个问题那么可能会不奏效

## Error reading item '**' from file INCAR.

除了设置有问题，每个参数后面不要加tab，有tab会导致参数设置失败。空格好像可以



## ZBRENT

指IBRION设置有问题时会出现此警告，取IBRION=2时计算会更慢而且找不到局部最优值，设置为IBRION=1并且设置POTIM=0.5之后可以加快计算收敛。具体原因我也不知道为什么。但是一般来说计算不会出现问题



## VERY BAD NEWS! internal error in subroutine IBZKPT







## The linear tetrahedron method can not  be used with the KPOINTS file

算无序超胞的能带的时候，高对称点kpath文件设置kpoints之后，不能正确计算，出现了以上的错误。stackexchange上面说改成ISMEAR=0（使用Gaussian smearing的方法）。——问题解决



## old and new charge differ

1. 一种可能是并行和vasp出现了问题根据（https://www.bilibili.com/read/cv8607700/）B站的经验：

   在提交到集群的运行脚本（run.sh）里面加入以下内容：

   > export I_MPI_ADJUST_REDUCE=3
   > export MPIR_CVAR_COLL_ALIAS_CHECK=0 

   可以解决并行和vasp的冲突

2. 直接换算法，用IALGO=48的算法把任务成功进行下去了



## Error EDDDAV: Call to ZHEGV failed. Returncode = \****

大概率是MGMOM的设置有问题，某些非磁性元素被设置为高磁矩会导致此结果。另外如果怎么调MGMOM都没有办法改变报错，可以通过调节AMIX，默认值是0.4， 出现这个问题适当减小，可以从0.02到0.2慢慢调看结果





## forrtl: severe：SIGSEGV, segmentation fault occurred

提交vaspsol任务的时候出现了这个问题，原因在于vaspsol使用的数组越界了。可以在run.sh中添加以下内容：

```shel
ulimit -s unlimited
```

