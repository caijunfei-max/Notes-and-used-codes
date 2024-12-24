### 前言

本文档记录使用mac时遇到的一些问题和解决方案



### github构建和连接

我在使用mac的时候需要科学上网才能登陆上github。

但是在科学上网后，仍然不能进行git clone，所以需要修改一下配置。

即，输入以下内容：

```shell
git config --global http.proxy http://127.0.0.1:xxxx
git config --global https.proxy http://127.0.0.1:xxxx
```

其中xxxx的内容指的是你所用的代理http：后面那串数字，修改一下代理就能连上了，一般也能正常进行clone

参考：知乎——[配置代理](https://zhuanlan.zhihu.com/p/648164862)

### 更改mac终端的颜色。

因为mac的终端时纯黑白，很多脚本是否可执行，文件、目录傻傻分不清楚，所以安装一个omyzsh就可以了，这是一个非常受欢迎的开源项目，具体可见其[github界面](https://github.com/ohmyzsh/ohmyzsh)