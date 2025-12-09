## 编译vtst和vaspsol

此为在未名一号、未名二号的编译，北大超算平台自带了编译器，可以直接load，其他平台类似：

1. 先load编译器，我用的是以下版本，其他版本应该也没有问题。（选一个就行了，应该没有傻瓜到都输入吧？）

   ```shell
   # 未名一号：
   module load intel/2019.1
   module load mpi/2021.9.0
   
   # 未名二号：
   module load intel_parallel_studio/2019.1
   module load mpi/2021.8.0
   ```

2. 现在我在~/apps路径上面进行以下操作。

   * 准备好vasp, vaspsol, vtstcode的安装包

     我安装的是5.4.4的，可以直接在github里面搜，包括一个vasp.5.4.4.tar.gz压缩包以及patch.5.4.416052018.gz安装包。两个都解压缩

     ```shell
     tar –zxvf vasp.5.4.4.tar.gz
     gunzip patch.5.4.4.16052018.gz
     ```

   * vtst在[vtst.tools](https://henkelmanlab.org/vtsttools/download.html)官网下载，我下载的是vtstcode-204.tgz(可能会有更新)

     然后解压缩

     ```bash
     tar -zvxf vtstcode-204.tgz
     ```

   * vaspsol的包在[VASPsol](https://github.com/henniggroup/VASPsol)安装，可以直接下载一个zip文件，传到服务器然后解压：

     ```bash
     unzip VASPsol-master.zip
     ```

     当然也可以通过git来下载（不过你要是会这个想必也不用看这一步内容了）

   好了，然后路径下应该有：

   目录

   vasp.5.4.4

   VASPsol-master

   vtstcode-204

   文件：

   patch.5.4.4.16052018

3. VTST：

   依次输入以下内容：

   ```
   cp vasp.5.4.4/src/chain.F vasp.5.4.4/src/chain.F.bk
   cp vtstcode-204/vtstcode5/* vasp.5.4.4/src
   ```

   然后修改vasp5.4.4/src/main.F文件

   其中的

   ```fortran
   CALL CHAIN_FORCE(T_INFO%NIONS,DYN%POSION,TOTEN,TIFOR, &                         LATT_CUR%A,LATT_CUR%B,IO%IU6)
   替换为
   CALL CHAIN_FORCE(T_INFO%NIONS,DYN%POSION,TOTEN,TIFOR, &
              TSIF,LATT_CUR%A,LATT_CUR%B,IO%IU6)
   ```

   

   同样的，修改vasp.5.4.4/src/.objects文件

   在SOURCE的chain.o前面添加以下内容：

   ```forth
   		bfgs.o dynmat.o instanton.o lbfgs.o sd.o cg.o dimer.o bbm.o \
           fire.o lanczos.o neb.o qm.o opt.o \
   ```

   注意后面的斜杠

4. VASPsol编译

   使用VASPsol-master/src中的solvation.F文件替换 vasp.5.4.4/src/solvation.F

5. 进入到vasp.5.4.4，把patch.5.4.4.16052018复制进来。并且使用patch修bug，输入以下内容：

   ```shell
   patch -p0 < patch.5.4.4.16052018
   ```

6. 修改makefile.include

   输入

   ```shell
   cp vasp5.4.4/arch/makefile.include.linux_intel vasp.5.4.4/makefile.include
   ```

   在CPP_OPTIONS中添加：

   -Dsol_compat

   把OFLAG = -O2

   改成OFLAG = -O3

7. 输入

   ```
   make all 
   ```

   等待结束~~

8. 测试编译是否成功

   直接提交VASPsol的example试一下就行了。

编译完成！

参考：

http://bbs.keinsci.com/thread-11111-1-1.html

http://bbs.keinsci.com/thread-34606-1-1.html



