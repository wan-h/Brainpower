#include "jobTimer.h"
#include <unistd.h>

class mJob : public JobTimerListener {
    void onTimeout() {
        printf("==========> tic toc!!!\n");
    };
};

#define fps (2)

int main()
{
    mJob* job = new mJob();
    JobTimer timer(fps, job);
    
    printf("===> start\n");
    timer.start();
    // 5s
    usleep(5000000);
    timer.stop();
    printf("===> stop\n");

    delete job;
    return 0;
}


// 编译
// g++ jobTimer.cpp main.cpp -o main -I `pwd` -I /home/vastai/workspace/src/boost_1_83_0 -L /home/vastai/workspace/src/boost_1_83_0/stage/lib -lboost_thread -lpthread