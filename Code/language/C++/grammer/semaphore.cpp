#include <iostream>
#include <unistd.h>
#include <thread>
#include <semaphore.h>

sem_t sem;

void func1() {
    // 等到信号量>0后执行减1
    // 这里相当于会等待func2的+1操作，起到了阻塞作用
    printf("func1 runing...\n");
    sem_wait(&sem);
    printf("func1 endding.\n");
}

void func2() {
    printf("func2 runing...\n");
    sleep(2);
    // 信号量值+1
    sem_post(&sem);
    printf("func2 endding.\n");
}

int main() {
    // 中间参数为0表示当前进程所有线程共享
    // 中间参数为1表示在进程间共享
    // 最后参数是默认初始值
    sem_init(&sem, 0, 0);
    std::thread t1 = std::thread(func1);
    std::thread t2 = std::thread(func2);

    t1.join();
    t2.join();

    // 销毁信号量
    sem_destroy(&sem);
    return 0;
}

// g++ -o main -pthread semaphore.cpp