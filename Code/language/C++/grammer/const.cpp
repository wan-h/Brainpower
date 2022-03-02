#include <iostream>

using namespace std;

class A{
    public:
        // 常量，不可被重新赋值
        const int a = 20;
        int b = 20;
        // 指针所指数据是个常量，不可通过解引用重新赋值
        const int* c = &b;
        // 指针本身是一个常量，指针所指数据可以解引用重新赋值但是指针指向的地址不可再修改
        int* const d = &b;

        // const修饰成员函数，该函数不可以修改任何成员变量，不能调用非const的成员函数
        int func() const {
            return 0;
        }
};

// const修饰函数返回值，返回值不可再被更改
const A& getA(){
    // static修饰的变量不会随着函数销往，存储在堆中，生命周期和程序保持一致
    static A aaa;
    return aaa;
};

int main(){
    const A& bbb = getA();
    cout << *(bbb.d) << endl;
    return 0;
}