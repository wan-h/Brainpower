//
// Created by wan on 2021/4/7.
//

#include <iostream>
using namespace std;

void swap_1(int x, int y);
void swap_2(int* x, int* y);
void swap_3(int& x, int& y);

// 传值调用
// 把参数的实际值复制给函数的形式参数, 修改函数内的形式参数不会影响实际参数
void swap_1(int x, int y) {
    int temp;
    temp = x; // 保存 x 的值
    x = y;    // 把 y 赋值给 x
    y = temp; // 把 x 赋值给 y
    return;
}

// 指针调用
// 把参数的地址复制给形式参数, 该地址用于访问调用中要用到的实际参数
void swap_2(int* x, int* y) {
    int temp;
    temp = *x; // 保存地址 x 的值
    *x = *y;   // 把 y 赋值给 x
    *y = temp; // 把 x 赋值给 y
    return;
}

// 引用调用
// 把引用的地址复制给形式参数, 该引用用于访问调用中要用到的实际参数
void swap_3(int& x, int& y) {
    int temp;
    temp = x; // 保存地址 x 的值
    x = y;    // 把 y 赋值给 x
    y = temp; // 把 x 赋值给 y
    return;
}


int main() {
    int a = 100;
    int b = 200;

    cout << "交换前，a的值: " << a << endl;
    cout << "交换前，b的值: " << b << endl;

    swap_1(a, b);
    cout << "swap_1交换后，a的值: " << a << endl;
    cout << "swap_1交换后，b的值: " << b << endl;

    a = 100;
    b = 200;
    swap_2(&a, &b);
    cout << "swap_2交换后，a的值: " << a << endl;
    cout << "swap_2交换后，b的值: " << b << endl;

    a = 100;
    b = 200;
    swap_3(a, b);
    cout << "swap_3交换后，a的值: " << a << endl;
    cout << "swap_3交换后，b的值: " << b << endl;

    return 0;
}