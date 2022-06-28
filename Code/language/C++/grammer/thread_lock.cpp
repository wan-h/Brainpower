#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

/*
unique_lock是一个类模板
构造函数上锁，析构函数解锁
所以可以针对代码块自动加解锁，避免mutex手动解锁繁杂且容易忘记后死锁
*/

using namespace std;

mutex mtx;
condition_variable cv;
bool ready = false;

void print_id(int id)
{
    unique_lock<mutex> lck(mtx); // 构造函数上锁
    while (!ready)
    {
        // cv.wait会阻塞当前线程知道收到notify
        // 阻塞时会释放锁mutex.unlock()，让其他的线程可以拿到锁
        // 收到notify之后就上锁mutex.unlock()然后停止阻塞继续执行
        cv.wait(lck);
    }

    cout << "thread " << id << endl;
    // 局部空间释放，unique_lock析构函数解锁
}

void go()
{
    unique_lock<mutex> lck(mtx);
    ready = true;
    // 通知等待该条件的其他所有线程
    cv.notify_all();
}

int main()
{
    thread threads[10];
    for (int i = 0; i < 10; i++)
    {
        threads[i] = thread(print_id, i);
    }
    cout << "10 threads ready to race ..." << endl;

    go();
    for (auto& th: threads)
    {
        th.join();
    }
    return 0;
}