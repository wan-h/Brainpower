//
// Created by wan on 2021/3/29.
//
#include <iostream>

using namespace std;

// 函数申明
void func(void);

//static 存储类指示编译器在程序的生命周期内保持局部变量的存在，而不需要在每次它进入和离开作用域时进行创建和销毁
static int count = 10;
extern int extern_test;
extern void extern_func();

// g++ storage_class.cpp other.cpp -o storage_class
// 使用other中的extern_test全局变量和extern_func函数，寻找路径为编译包含的文件路径
// extern 存储类用于提供一个全局变量的引用，全局变量对所有的程序文件都是可见的
// extern 修饰符通常用于当有两个或多个文件共享相同的全局变量或函数
int main(){
    while (count --){
        func();
    }
    return 0;
}

void func(void){
    // 使用 static 修饰局部变量可以在函数调用之间保持局部变量的值， 编译器在程序的生命周期内保持局部变量的存在
    static int i = 5;
    i ++;
    cout << "变量i为 " << i;
    cout << ", 变量count为 " << count << endl;
}
