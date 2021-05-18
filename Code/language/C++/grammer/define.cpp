#include <iostream>
using namespace std;
#define DEBUG

#define MIN(a, b) (((a) < (b)) ? a: b)

int main(){
    int i, j;
    i = 100;
    j = 30;
#ifndef DEBUG
    cerr << "Trace: Inside main function" << endl;
#endif

#if 0
    // 注释代码部分
    cout << "IF 0 TEST" << endl;
#endif

    cout << "The minimum is " << MIN(i, j) << endl;
    // C++中已提供的预定义宏
    // 当前行号
    cout << "Value of __LINE__ : " << __LINE__ << endl;
    // 当前文件名
    cout << "Value of __FILE__ : " << __FILE__ << endl;
    // 当前日期
    cout << "Value of __DATE__ : " << __DATE__ << endl;
    // 当前时间
    cout << "Value of __TIME__ : " << __TIME__ << endl;

    return 0;
}