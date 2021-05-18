#include <iostream>
#include <map>

using namespace std;
int main(){
    map <int, int> m1, m2, m3;
    map <int, int> :: iterator m1_iter;
    // Map 中的元素是自动按 key 升序排序, 后续遍历打印是按照key的升序打印出来的
    m1.insert(pair <int, int> (2, 20));
    m1.insert(pair <int, int> (1, 10));
    m1.insert(pair <int, int> (3, 30));

    m2.insert(pair <int, int> (10, 100));
    m2.insert(pair <int, int> (20, 200));
    m2.insert(pair <int, int> (30, 300));
    cout << "The original map m1 is:" << endl;
    // map的遍历
    for( m1_iter = m1.begin(); m1_iter != m1.end(); m1_iter++){
        // 展示第二元素
        cout << " " << m1_iter -> second << "." << endl;
    }
    // 两个容器的交换
    m1.swap(m2);
    cout << "After swapping with m2, map m1 is:" << endl;
    for( m1_iter = m1.begin(); m1_iter != m1.end(); m1_iter++){
        cout << " " << m1_iter -> second << "." << endl;
    }

    swap(m1, m3);
    cout << "After swapping with m3, map m1 is:" << endl;
    for( m1_iter = m1.begin(); m1_iter != m1.end(); m1_iter++){
        cout << " " << m1_iter -> second << "." << endl;
    }
    return 0;
}