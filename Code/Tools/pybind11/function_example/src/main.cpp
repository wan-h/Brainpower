#include <iostream>
#include <pybind11/pybind11.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

int add(int i, int j) {
    return i + j;
}

// 使用python对象作为参数
void print_dict(const py::dict& dict){
    for (auto item: dict){
        std::cout << "key=" << std::string(py::str(item.first)) << ", " 
        << "value=" << std::string(py::str(item.second)) << std::endl;
    }
}

// 接收*args和**kwargs参数
void generic(py::args args, const py::kwargs& kwargs){
    for (auto item: kwargs){
        std::cout << "key=" << std::string(py::str(item.first)) << ", " 
        << "value=" << std::string(py::str(item.second)) << std::endl;
    }
}

PYBIND11_MODULE(function_example, m) {
m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
        .. currentmodule:: cmake_example
        .. autosummary::
           :toctree: _generate
           add
           subtract
    )pbdoc";

m.def("add", &add, R"pbdoc(
        Add two numbers
        Some other explanation about the add function.
    )pbdoc",
    // 暴露关键字参数（可以带有默认参数），可以通过参数名字进行传参
    // example.add(i=1, j=2)
    py::arg("i") = 1, py::arg("j") = 2
    );

m.def("print_dict", &print_dict);
m.def("generic", &generic);

}