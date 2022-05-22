#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

/*
unique_lock��һ����ģ��
���캯��������������������
���Կ�����Դ�����Զ��ӽ���������mutex�ֶ������������������Ǻ�����
*/

using namespace std;

mutex mtx;
condition_variable cv;
bool ready = false;

void print_id(int id)
{
    unique_lock<mutex> lck(mtx); // ���캯������
    while (!ready)
    {
        // cv.wait��������ǰ�߳�֪���յ�notify
        // ����ʱ���ͷ���mutex.unlock()�����������߳̿����õ���
        // �յ�notify֮�������mutex.unlock()Ȼ��ֹͣ��������ִ��
        cv.wait(lck);
    }

    cout << "thread " << id << endl;
    // �ֲ��ռ��ͷţ�unique_lock������������
}

void go()
{
    unique_lock<mutex> lck(mtx);
    ready = true;
    // ֪ͨ�ȴ������������������߳�
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