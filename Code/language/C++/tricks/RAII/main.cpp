
#include <iostream>

using namespace std;

template<typename T>
class RAII
{
private:
    T* data;
public:
    RAII() : data(nullptr) {};
    explicit RAII(T* rhs) : data(rhs) {};
    // 析构函数资源自动回收
    ~RAII() { if (data) delete data; };
    // 复写->操作符方便调用
    T* operator->()const {
        return data;
    };
    // 删除拷贝构造函数，这个是为了防止多个实例析构的时候发生多次资源释放
    RAII(const RAII<T>&) = delete;
    RAII& operator = (const RAII&) = delete;
    // move直接接管所有权，通过move来做传递，&&表示右值引用
    RAII(RAII<T>&& rhs) {
        data = rhs.data;
        rhs.data = nullptr;
    }
    void operator = (RAII<T>&& rhs) {
        data = rhs.data;
        rhs.data = nullptr;
    }
};

// 测试对象
struct A {
    int x, y, z;
    ~A() {
        cout << "~A()" << endl;
    }
};

int main(int argc, char* argv[]) {
    RAII<A> p1(new A{1, 2, 3});
    printf("Create A, x: %d, y: %d, z: %d\n", p1->x, p1->y, p1->z);
    // 通过作用域，p2获得所有权，并在作用域结束后就结束了生命周期
    {
        RAII<A>p2 = move(p1);
    }
    printf("End of main.\n");
}

// 编译 g++ main.cpp -o main