#include <iostream>
#include <ctime>
// c++11中的新特性
#include <chrono>
#include <ratio>

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

    // 使用chrono,duration默认的单位就是秒
    typedef chrono::duration<int> second_type;
    typedef chrono::duration<int, milli> milliseconds_type;
    typedef chrono::duration<int, ratio<60 * 60>> hours_type;

    hours_type h_oneday(24);
    second_type s_oneday(60*60*24);
    milliseconds_type ms_oneday(s_oneday);
    // count()返回Rep类型的Period数量
    cout << ms_oneday.count() << "ms in 1 day" << endl;

    chrono::milliseconds foo(6000); // 6s
    cout << "duration (in periods): " << foo.count() << " milliseconds." << endl;
    // chrono::microseconds::period实际上就是s和ms的换算比例
    cout << "duration (in periods): " << foo.count() * chrono::milliseconds::period::num / chrono::milliseconds::period::den << " seconds." << endl;

    // time_point表示一个时间点
    time_t tt;
    chrono::system_clock::time_point _now = chrono::system_clock::now();
    tt = chrono::system_clock::to_time_t(_now);
    cout << "today is: " << ctime(&tt);
    typedef chrono::duration<int, std::ratio<60*60*24>> days_type;
    // time_point_cast将时间转换为以天为单位
    // chrono::time_point<chrono::system_clock, days_type> today = chrono::time_point_cast<days_type>(chrono::system_clock::now());
    chrono::system_clock::time_point today = chrono::system_clock::now();
    chrono::duration<int, std::ratio<60*60*24> > one_day (1);
    chrono::system_clock::time_point tomorrow = today + one_day;
    tt = chrono::system_clock::to_time_t ( tomorrow );
    cout << "tomorrow will be: " << ctime(&tt);
    // time_since_epoch计算1970年1月1日到time_point时间经过的duration
    cout << today.time_since_epoch().count() << " days since epoch" << endl;

    // 计算时间差, chrono::steady_clock 为了表示稳定的时间间隔
    chrono::steady_clock::time_point t1 = chrono::steady_clock::now();
    for (int i=0; i<1000; ++i) {cout << "*";}
    chrono::steady_clock::time_point t2 = chrono::steady_clock::now();
    chrono::duration<double> time_span = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    cout << "It took me " << time_span.count() << " seconds." << endl;

    return 0;
}