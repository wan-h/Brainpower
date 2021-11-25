#include <iostream>
using namespace std;

int main(){
    char grade = 'D';
    switch(grade) {
        case 'A':
            cout << "很棒！" << endl; 
            break;
        // 没有break的直接往下走
        case 'B' :
        case 'C' :
            cout << "做得好" << endl;
            break;
        case 'D' :
            cout << "您通过了" << endl;
            break;
        case 'F' :
            cout << "最好再试一下" << endl;
            break;
        // 其他情况默认执行
        default :
            cout << "无效的成绩" << endl;
        }
        cout << "您的成绩是 " << grade << endl;
    return 0;
}