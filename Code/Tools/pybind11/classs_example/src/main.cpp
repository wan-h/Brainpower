#include <iostream>
#include <pybind11/pybind11.h>


using namespace std;
namespace py = pybind11;

class Pet{
private:
    int age;
public:
    enum Kind {
        Dog = 0,
        Cat
    };
    struct Attributes {
        string gender="girl";
    };

    string name;
    Kind type;
    Attributes attr;
    Pet(const string& _name, Kind _type){
        name = _name;
        type = _type;
    };
    void setName(const string& _name){
        name = _name;
    }
    const string& getName() const {
        return name;
    }
    void setAge(const int _age){
        age = _age;
    }
    const int getAge() const {
        return age;
    };

    virtual string go() const {
        return "haha!";
    };

    void set(const int _age){
        age = _age;
    };

    void set(const string& _name){
        name = _name;
    };
};

class Dog : public Pet {
public:
    Dog(const string& _name, Pet::Kind _type): Pet(_name, _type){ };
    string go() const {
        return "woof!";
    };
};

PYBIND11_MODULE(class_example, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------
    )pbdoc";
    // py::dynamic_attr表示支持动态属性，先将pet定义成一个变量，方便后续其他定义操作
    py::class_<Pet> pet(m, "Pet", R"pbdoc(Pet class)pbdoc", py::dynamic_attr());

    pet.def(py::init<const string&, Pet::Kind>())
        // 定义共有成员变量
        // def_readwrite 方法可以导出公有成员变量,可以获取成员变量重新赋值
        // def_readonly 方法则可以导出只读成员
        .def_readwrite("name", &Pet::name)
        .def_readwrite("attr", &Pet::attr)
        // 定义私有成员变量，其中set和get方法定义赋值操作，并没有向外暴露函数接口
        // def_property_readonly() 定义只读私有成员
        // 最好不要把私有变量暴露出去
        .def_property("age", &Pet::getAge, &Pet::setAge)
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName)
        .def("go", &Pet::go)
        // 函数重载
        .def("set", py::overload_cast<const int>(&Pet::set), "set pet's age.")
        .def("set", py::overload_cast<const string&>(&Pet::set), "set pet's name.");
        
    
    // 绑定类中的枚举
    py::enum_<Pet::Kind>(pet, "Kind")
        .value("Dog", Pet::Kind::Dog)
        .value("Cat", Pet::Kind::Cat)
        // export_values将枚举导出到父作用域，可以直接使用pet.Cat获取变量
        .export_values();

    // 绑定类中的结构体
    py::class_<Pet::Attributes> (pet, "Attributes")
        .def(py::init<>())
        .def_readwrite("gender", &Pet::Attributes::gender);

    // 定义继承类，Pet已经定义的就都继承了
    py::class_<Dog, Pet>(m, "Dog")
        .def(py::init<const string&, Pet::Kind>())
        .def("go", &Dog::go);
    // []()是c++中的lambda
    m.def("pet_store", []() {return unique_ptr<Pet>(new Dog("xiaohei", Pet::Kind::Dog));});
}