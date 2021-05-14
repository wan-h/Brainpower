#include <iostream>
#include <ctime>

using namespace std;

// struct tm {
//   int tm_sec;   // 秒，正常范围从 0 到 59，但允许至 61
//   int tm_min;   // 分，范围从 0 到 59
//   int tm_hour;  // 小时，范围从 0 到 23
//   int tm_mday;  // 一月中的第几天，范围从 1 到 31
//   int tm_mon;   // 月，范围从 0 到 11
//   int tm_year;  // 自 1900 年起的年数
//   int tm_wday;  // 一周中的第几天，范围从 0 到 6，从星期日算起
//   int tm_yday;  // 一年中的第几天，范围从 0 到 365，从 1 月 1 日算起
//   int tm_isdst; // 夏令时
// };

int main() {
    // 基于当前系统的当前日期/时间
    time_t now = time(0);

    cout << "1970年1月1日到目前经过的秒数:" << now << endl;

    tm *ltm = localtime(&now);

    // 输出tm结构的各个组成部分
    cout << "年: " << 1900 + ltm -> tm_year << endl;
    cout << "月: " << 1 + ltm -> tm_mon << endl;
    cout << "日: " << ltm -> tm_mday << endl;
    cout << "时间: " << ltm -> tm_hour << ":";
    cout << 1 + ltm -> tm_min << ":";
    cout << 1 + ltm -> tm_sec << endl;
}