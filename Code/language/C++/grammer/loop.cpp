//
// Created by wanh on 2021/3/30.
//

#include <iostream>

using namespace std;

int main() {
    // for循环
    for (int a = 0; a < 3; a++) {
        cout << "for a 的值: " << a << endl;
    }
    // while循环
    int b = 0;
    while ( b < 3 ) {
        cout << "while b 的值: " << b << endl;
        b++;
    }
    // do while循环
    int c = 0;
    do {
        c++;
        switch (c) {
            case 0:
                continue;
            case 1:
                cout << "do while c 的值: " << c << endl;
            // １会打印两次，因为会依次执行
            case 2:
                cout << "do while c 的值: " << c << endl;
            // 3就进入默认被break了
            default:
                break;
        }
    } while (c < 5);
    return 0;
}