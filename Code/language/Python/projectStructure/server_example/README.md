# srv-server-example
python服务代码架构示例

## TODO
- [x] 新起镜像，工作目录映射
- [x] 安装python库(dockerfile中安装)
- [x] 新写代码
  - [x] 逻辑代码
  - [x] 服务代码
- [x] 单元测试
- [x] 使用gunicorn起多进程
- [x] 性能测试
- [ ] 上线

## 代码结构
>server_example(项目)
>>benchmark(性能测试)

>>bin(http服务接口)
>>> app.py

>>config(配置文件)

>>docs(文档)

>>lib(库实现)
>>>modules(数据库的接口逻辑实现)

>>logs(日志文件)

>>src(资源文件)

>>test(单元测试)
>>>run_pytest.py(单元测试启动脚本)

>>Dockerfile

>>requirements.txt

>>start.sh(启动搅拌)

>>stop.sh(停止脚本)


## 研发流程
* 启动镜像
* 编码
* 单元测试
* 性能测试


## 测试流程
* 启动镜像
* 单元测试
```
python test/run_pytest.pu
```
* 性能测试
单进程测试
```
cd bin
nohup python app.py &
cd ../benchmark
locust -f test.py --host http://0.0.0.0:5000 --web-host 0.0.0.0 # test on web
ps -ef | grep app && kill (pids)
```
多进程测试
```
sh start.sh
# 修改gunicorn.py中的workers更改同时启用的服务进程数
cd benchmark
locust -f test.py --host http://0.0.0.0:800 --web-host 0.0.0.0 # test on web
sh stop.sh # 停掉多进程
```

## 记录
将先关文档输出到docs
* 单元测试情况
* 性能测试情况
