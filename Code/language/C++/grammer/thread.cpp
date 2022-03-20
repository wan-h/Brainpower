#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>

using namespace std;

mutex mtx;

int x = 0;
// std::atomic_int只是std::atomic<int>的别名
// 定义对y的操作都是原子操作，避免了在多线程中使用mutex反复加解锁消耗资源
atomic_int y(0);

void f1(int n)
{
    for (int i = 0; i < n; i++)
    {
        cout << "Thread " << this_thread::get_id() << " executing." << endl;
        // 睡1 ms
        this_thread::sleep_for(chrono::milliseconds(1));
        // mutex加锁防止多线程篡改
        mtx.lock();
        x++;
        mtx.unlock();
    }
}

void f2(int& n)
{
    for (int i = 0; i < n; i++)
    {
        cout << "Thread " << this_thread::get_id() << " executing." << endl;
        this_thread::sleep_for(chrono::milliseconds(1));
        mtx.lock();
        x++;
        mtx.unlock();
    }
}



int main()
{
    thread t1;
    // joinable返回线程是否可以执行join函数
    cout << "before t1 starting, joinable: " << t1.joinable() << endl;
    // 执行线程
    int n = 2;
    t1 = thread(f1, n);
    cout << "after t1 starting, joinable: " << t1.joinable() << endl;
    thread t2(f2, ref(n));
    // 获取线程id
    thread::id t1_id = t1.get_id();
    thread::id t2_id = t2.get_id();
    cout << "t1_id: " << t1_id << " ; t2_id: " << t2_id << endl;
    // join等待自线程执行结束
    t1.join();
    // 从主线程分离，独立运行
    t2.detach();
    return 0;
}