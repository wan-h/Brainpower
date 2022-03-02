#include <iostream>
#include <memory>

using namespace std;

class A{
public:
    A(){};
    ~A(){};
    // weak_ptr防止相互引用导致死锁
    // shared_ptr<A> p1 = std::make_shared<A>();
    // shared_ptr<A> p2 = std::make_shared<A>();
    // p1->a = p2;
    // p2->a = p1;
    weak_ptr<A> a;
};

int main(){
    // unique_ptr 只能通过构造函数将指针传入，而不能将一个指针直接进行赋值
    // unique_ptr<A> p1 = new A(); // 会报错
    // unique_ptr 只能在初始化的时候指向一片内存，之后他就不能被别人重新赋值，也不能赋值给其他指针，这是一个孤独的智能指针
    // 智能指针将普通的指针封装为一个栈对象，在初始化之后，就可以像普通指针那样操作这个智能指针，不一样的是，在使用完之后，不用去 delete 他，他会自动释放内存
    unique_ptr<A> p1(new A());
    // shared_ptr和unique_ptr的主要区别在于前者是使用引用计数的智能指针，当引用计数为0时自动销毁
    // make_shared 可以保留指针的关系，避免错误发生，也是 shared_ptr 推荐的方式
    shared_ptr<A> p2 = make_shared<A>();
    shared_ptr<A> p3 = p2;
    shared_ptr<A> p4 = make_shared<A>();

    // 如果A.a不使用weak_ptr会导致两个智能指针都没有被销毁，这种现象为“死锁”现象
    p2 -> a = p4;
    p4 -> a = p2;

    return 0;
}