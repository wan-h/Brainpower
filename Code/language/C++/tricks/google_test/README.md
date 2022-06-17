# 安装
在cmake中直接使用FetchContent_Declare引入了gooletest三方库  
见google_test/unittest/CMakeLists.txt

# 使用
编译执行lib中的可执行文件显示以下结果
```bash
[==========] Running 3 tests from 2 test suites.
[----------] Global test environment set-up.
[----------] 1 test from HelloTest
[ RUN      ] HelloTest.BasicAssertions
[       OK ] HelloTest.BasicAssertions (0 ms)
[----------] 1 test from HelloTest (1 ms total)

[----------] 2 tests from FooTest
SetUpTestCase
[ RUN      ] FooTest.test1
Test set-up
Test SetUp
Test TearDown
Test clean-up
[       OK ] FooTest.test1 (1 ms)
[ RUN      ] FooTest.test2
Test set-up
Test SetUp
Test TearDown
Test clean-up
[       OK ] FooTest.test2 (1 ms)
TearDownTestCase
[----------] 2 tests from FooTest (2 ms total)

[----------] Global test environment tear-down
[==========] 3 tests from 2 test suites ran. (6 ms total)
[  PASSED  ] 3 tests.
```
从日志可以分析一下：  
* 整个测试开始和测试会有一个environment的set-up和tear-down
* 每个场景以及场景中的每一个测试都有可以控制的setup和teardown函数，根据需要写一个即可，可[参考](https://www.cnblogs.com/coderzh/archive/2009/04/06/1430396.html)