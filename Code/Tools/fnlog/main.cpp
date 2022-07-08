#include "fn_log.h"

int main(int argc, char* argv[])
{
    int ret = FNLog::LoadAndStartDefaultLogger("../log.yaml");
    if(ret != 0)
    {
        return ret;
    }

    int limit_second = 5;
    while (limit_second > 0)
    {
        LogDebug() << "default channel.";
        LogDebugStream(0, 0, 0) << "channel:0, category:0.";
        LogDebugStream(0, 1, 0) << "channel:0, category:1.";
        LogDebugStream(0, 2, 0) << "channel:0, category:2.";
        LogDebugStream(0, 3, 0) << "channel:0, category:3.";
        LogDebugStream(0, 4, 0) << "channel:0, category:4.";
        LogDebugStream(0, 5, 0) << "channel:0, category:5.";
        LogDebugStream(1, 0, 0) << "channel:1, category:0.";
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        limit_second--;
    }


    LogAlarm() << "finish";
    return 0;
}