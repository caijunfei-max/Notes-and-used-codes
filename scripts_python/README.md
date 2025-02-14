说明：

scripts_python里面的脚本是需要python环境的脚本，脚本有的是在windows环境或者mac的pycharm上编写的，因此可能格式有点乱，有一些各个系统特有的换行符。

如果需要在linux或者服务里面使用，可以输入

```shell
dos2unix filename # 把windows格式的脚本转化为unix
unix2dos filename # 把unix格式转化为windows格式
```



### 自定义库的使用

my_modules中包含的是日常中是使用到的可能泛用性比较强的函数和方法。引用自己本地库的方法——在引用的脚本中使用sys库添加my_modules所在的路径。

```python
import sys
sys.path.append("path")
import my_modules
```



### 文件

chop_plot : 在描述符课题中自动绘制布居分析的代码。代码中绘制的是COBI。需要import自定义库my_modules.

