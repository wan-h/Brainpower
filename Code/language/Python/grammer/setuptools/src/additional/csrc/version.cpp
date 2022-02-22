#include <pybind11/pybind11.h>
#include "hello.h"

// 这个第一个参数一定要和extension_name是匹配的，这样才能import到
// 这里的_C就是最后一层，表示需要bind上的模块的名字
PYBIND11_MODULE(_C, m) {
  m.def("hello", &Hello, "hello!");
}