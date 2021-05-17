#include <iostream>
#include <vector>

using namespace std;

// 类似Python中的list, 封装了动态大小数组的顺序容器

int main(){
    // 初始化一个空的vector向量
    vector<char> value;
    // 向向量尾部依次添加字符
    value.push_back('S');
    value.push_back('T');
    value.push_back('L');

    cout << "元素个数为: " << value.size() << endl;

    // 使用迭代器遍历
    for (auto i = value.begin(); i < value.end(); i++){
        cout << *i << " ";
    }
    cout << endl;

    // 开头插入数据
    value.insert(value.begin(), 'C');
    cout << "首个元素为：" << value.at(0) << endl;

    return 0;
}