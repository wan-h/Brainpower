//
// Created by wan on 2021/3/27.
//

#include <iostream>

using namespace std;

//没有设置的地方从0开始计数
enum Day { MONDAY, TUESDAY=2, WEDNESDAY, THURSDAY, FRIDAY };

int today = MONDAY;
Day workday = TUESDAY;
int tomorrow = workday;

int main(){
    cout << today << " " << tomorrow << endl;
}