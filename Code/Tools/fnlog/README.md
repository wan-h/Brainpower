# fnlog
[code](https://github.com/zsummer/fn-log)

## 安装
fnlog是一个only header的库，所以只需要下载包含头文件即可  

* 下载版本库
* include引入

## 使用
```bash
mkdir build
cd build
cmake ..
make
./fzlog_example
```

## 解析
* 根据配置文件，会在相应的路径生成log日志文件  
* 对于输出的过滤就是根据调用的指定channel、category
    ```c++
    // 转移到(0, 0, 0)
    LogDebug() << "default channel.";
    // channel: 1, category: 1
    LogDebugStream(1, 1, 0) << "channel:0, category:0.";
    ```
* 配置文件中的 category=0 && category_extend=0 基本表示不做过滤，否则就表示取一个过滤范围