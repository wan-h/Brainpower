#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <stdexcept>

using namespace std;

// 函数模板
template <typename T>
// inline表示内联函数， 编译时直接将此部分插入调用者， 避免高频调用时内部实现过于简单， 主要耗时在函数调用
inline T const& Max(T const& a, T const& b){
    return a < b? b: a;
}

// 类模板
template <class T>
class Stack{
    private:
        vector<T> elems;
    public:
        // 入栈 
        void push(T const&);
        // 出栈
        void pop();
        // 返回栈顶元素
        // 最后一个const代表类中的常函数， 常函数不能修改本类中任意的成员变量， 除非本类数据成员有“mutable”关键字修饰
        T top() const;
        // 如果为空返回真
        bool empty() const{
            return elems.empty();
        }
};

template <class T>
void Stack<T>::push(T const& elem){
    elems.push_back(elem);
}

template <class T>
void Stack<T>::pop(){
    if(elems.empty()){
        throw out_of_range("Stack<>::pop(): empty stack");
    }
    // 删除最后一个元素
    elems.pop_back();
}

template <class T>
T Stack<T>::top() const{
    if(elems.empty()){
        throw out_of_range("Stack<>::pop(): empty stack");
    }
    // 返回最够一个元素的副本
    return elems.back();
}

int main(){
    int i = 39;
    int j = 20;
    cout << "Max(i, j): " << Max(i, j) << endl;

    string s1 = "Hello";
    string s2 = "World";
    cout << "Max(s1, s2): " << Max(s1, s2) << endl;

    try
    {
        Stack<int> intStack;
        Stack<string> stringStack;

        intStack.push(7);
        cout << intStack.top() << endl;

        stringStack.push("hello");
        cout << stringStack.top() << endl;

        intStack.pop();
        stringStack.pop(); 
    }catch(exception const& ex){
        cout << "Exception: " << ex.what() << endl;
    }
    

    return 0;
}