#include<iostream>

using namespace std;

double vals[] = {10.1, 12.6, 33.1, 24.1, 50.0};

double& setvalues(int i) {
    double& ref = vals[i];
    return ref;
}

int main() {
    cout << "改变前的值" << endl;
    for (int i = 0; i < 5; i++) {
        cout << "vals[" << i << "] = ";
        cout << vals[i] << endl;
    }

    // 直接对引用修改原数据
    setvalues(1) = 20.23;
    setvalues(3) = 70.8;

    cout << "改变后的值" << endl;
    for (int i = 0; i < 5; i++) {
        cout << "vals[" << i << "] = ";
        cout << vals[i] << endl;
    }

    return 0;
}