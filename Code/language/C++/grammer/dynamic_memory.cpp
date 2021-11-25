#include <iostream>
using namespace std;

class Box{
    public:
        Box(){
            cout << "调用构造函数！" << endl;
        }
        ~Box(){
            cout << "调用析构函数！" << endl;
        }
};

int main(){
    // 初始化为null指针
    double* pvalue = NULL;
    // 变量申请内存
    pvalue = new double;

    // 
    *pvalue = 29494.99;
    cout << "Value of pvalue : " << *pvalue << endl;

    // 释放内存
    delete pvalue;

    // 对象的动态存储分配
    Box* myBoxArray = new Box[4];
    // [] 代表释放数组
    delete [] myBoxArray;

    return 0;
}