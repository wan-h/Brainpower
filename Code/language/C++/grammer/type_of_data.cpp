 //
// Created by wanh on 2021/3/26.
//

# include <iostream>
# include <limits>

using namespace std;
// typedef 为一个已有的类型取一个新的名字
typedef int MYINT;

int main(){
    cout << "type: \t\t" << "************size**************" << endl;

    cout << "bool: \t\t" << "所占字节数" << sizeof(bool);
    cout << "\t最大值:" << (numeric_limits<bool>::max)();
    cout << "\t\t最小值:" << (numeric_limits<bool>::min)() << endl;

    cout << "char: \t\t" << "所占字节数" << sizeof(char);
    cout << "\t最大值:" << (numeric_limits<char>::max)();
    cout << "\t\t最小值:" << (numeric_limits<char>::min)() << endl;

    cout << "singed char: \t\t" << "所占字节数" << sizeof(char);
    cout << "\t最大值:" << (numeric_limits<signed char>::max)();
    cout << "\t\t最小值:" << (numeric_limits<signed char>::min)() << endl;

    cout << "unsinged char: \t\t" << "所占字节数" << sizeof(unsigned char);
    cout << "\t最大值:" << (numeric_limits<unsigned char>::max)();
    cout << "\t\t最小值:" << (numeric_limits<unsigned char>::min)() << endl;

    cout << "wchar_t: \t\t" << "所占字节数" << sizeof(wchar_t);
    cout << "\t最大值:" << (numeric_limits<wchar_t>::max)();
    cout << "\t\t最小值:" << (numeric_limits<wchar_t>::min)() << endl;

    cout << "short: \t\t" << "所占字节数" << sizeof(short);
    cout << "\t最大值:" << (numeric_limits<short>::max)();
    cout << "\t\t最小值:" << (numeric_limits<short>::min)() << endl;

    cout << "int: \t\t" << "所占字节数" << sizeof(MYINT);
    cout << "\t最大值:" << (numeric_limits<MYINT>::max)();
    cout << "\t\t最小值:" << (numeric_limits<MYINT>::min)() << endl;

    cout << "unsigned: \t\t" << "所占字节数" << sizeof(unsigned);
    cout << "\t最大值:" << (numeric_limits<unsigned>::max)();
    cout << "\t\t最小值:" << (numeric_limits<unsigned>::min)() << endl;

    cout << "long: \t\t" << "所占字节数" << sizeof(long);
    cout << "\t最大值:" << (numeric_limits<long>::max)();
    cout << "\t\t最小值:" << (numeric_limits<long>::min)() << endl;

    cout << "unsigned long: \t\t" << "所占字节数" << sizeof(unsigned long);
    cout << "\t最大值:" << (numeric_limits<unsigned long>::max)();
    cout << "\t\t最小值:" << (numeric_limits<unsigned long>::min)() << endl;

    cout << "double: \t\t" << "所占字节数" << sizeof(double);
    cout << "\t最大值:" << (numeric_limits<double>::max)();
    cout << "\t\t最小值:" << (numeric_limits<double>::min)() << endl;

    cout << "long double: \t\t" << "所占字节数" << sizeof(long double);
    cout << "\t最大值:" << (numeric_limits<long double>::max)();
    cout << "\t\t最小值:" << (numeric_limits<long double>::min)() << endl;

    cout << "float: \t\t" << "所占字节数" << sizeof(float);
    cout << "\t最大值:" << (numeric_limits<float>::max)();
    cout << "\t\t最小值:" << (numeric_limits<float>::min)() << endl;

    cout << "size_t: \t\t" << "所占字节数" << sizeof(size_t);
    cout << "\t最大值:" << (numeric_limits<size_t>::max)();
    cout << "\t\t最小值:" << (numeric_limits<size_t>::min)() << endl;

    cout << "string: \t\t" << "所占字节数" << sizeof(string) << endl;

    cout << "type: \t\t" << "************size**************" << endl;
    return 0;
}