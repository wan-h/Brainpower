#include <iostream>
using namespace std;

int main(){
    double Array1[2][3] = {{1, 2, 3}, {4, 5, 6}};
    double Array2[3] = {7, 8, 9};
    double* p;
    p = Array2;

    // 输出数组中的每一个元素
    cout << "使用指针的数组值 " << endl;
    for (int i = 0; i < 3; i++) {
        cout << "*(p + )" << i << ") : ";
        cout << *(p + 1) << endl;
    }

    // 使用Array1作为地址的数组值
    for (int i = 0; i < 2; i++) {
        cout << "*(Array1 + " << i << ") : ";
        for (int j = 0; j < 3; j++) {
            cout << *(Array1[i] + j);
        }
        cout << endl;
    }

    return 0;
}