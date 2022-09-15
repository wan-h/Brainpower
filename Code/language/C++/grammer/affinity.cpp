
#define _GNU_SOURCE
#include <iostream>
#include <thread>
#include <pthread.h>

using namespace std;

cpu_set_t cpuset, cpuget;

void f() {
    this_thread::sleep_for(chrono::seconds(3));
}

int main() {
    unsigned int n = thread::hardware_concurrency();
    // 这个一般是CPU的逻辑核心数
    cout << "CPU cores: " << n << endl; 
    thread t = thread(f);
    
    // 获取线程亲和性
    CPU_ZERO(&cpuset);
    int result = pthread_getaffinity_np(t.native_handle(), sizeof(cpu_set_t), &cpuset);
    if (result != 0) {
        cout << "Thread getaffinity failed" << endl;
    }
    cout << "affinity cpu id=";
    for (int i = 0; i < CPU_SETSIZE; i++) {
        if (CPU_ISSET(i, &cpuset)) {
            cout << i << ", ";
        }
    }
    cout << endl;

    // 设置亲和性
    CPU_ZERO(&cpuset);
    CPU_SET(0, &cpuset);
    CPU_SET(1, &cpuset);
    result = pthread_setaffinity_np(t.native_handle(), sizeof(cpu_set_t), &cpuset);
    if (result != 0) {
        cout << "Thread setaffinity failed" << endl;
    }

    // 再次查询
    CPU_ZERO(&cpuset);
    result = pthread_getaffinity_np(t.native_handle(), sizeof(cpu_set_t), &cpuset);
    if (result != 0) {
        cout << "Thread getaffinity failed" << endl;
    }
    cout << "affinity cpu id=";
    for (int i = 0; i < CPU_SETSIZE; i++) {
        if (CPU_ISSET(i, &cpuset)) {
            cout << i << ", ";
        }
    }
    cout << endl;

    t.join();
    return 0;
}


// g++ affinity.cpp -lpthread -o main