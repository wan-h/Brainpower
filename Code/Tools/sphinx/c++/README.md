## steps

### 安装
```shell
# 基础安装
pip install sphinx
# HTTP服务支持
pip install sphinx-autobuild
# 主题修改，在[https://sphinx-themes.org]可以找到
# 在conf.py文件中修改html_theme
pip install sphinx_rtd_theme
# 扩展支持markdown文件
# 在 conf.py 配置文件中添加extensions支持
pip install recommonmark
pip install sphinx_markdown_tables
# c++文档支持，桥接Sphinx和Doxygen两个文档系统
# 文档参见 [https://exhale.readthedocs.io/en/latest]
pip install exhale
# 安装doxygen
apt install doxygen
```

### 初始化
```shell
# 创建一个用于存放文档的文件夹，然后在该文件夹路径下运行下列命令快速生成Sphinx项目
sphinx-quickstart
```
项目创建后的目录为：
```shell
.
├── Makefile
├── build
├── make.bat
└── source
    ├── _static
    ├── _templates
    ├── conf.py
    └── index.rst
# build:用来存放通过make html生成文档网页文件的目录
# source：存放用于生成文档的源文件
# conf.py: Sphinx的配置文件
# index.rst: 主文档
```

### 修改构建文档
* 创建文档
* 指定文档  
在index.rst下指定文档位置
* 构建文档  
```shell
# 编译成html文档，生成在build
make html
```

### 访问文档
直接在build/html中打开index.html获取使用构建器启动http服务
```shell
# 访问 http://127.0.0.1:8000
sphinx-autobuild source build/html
```

### c++支持步骤
* 参照初始化sphinx[Exhale](https://exhale.readthedocs.io/en/latest/quickstart.html#quickstart-guide)
* 解析方式
   * 主要解析头文件，所以设置里面需要指定头文件位置