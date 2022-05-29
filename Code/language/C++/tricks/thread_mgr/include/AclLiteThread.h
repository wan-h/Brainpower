#pragma once
#include <iostream>
#include <thread>
#include "ThreadSafeQueue.h"
#include "AclLiteError.h"

using namespace std;

#define INVALID_INSTANCE_ID (-1)

class AclLiteThread{
public:
    AclLiteThread();
    virtual ~AclLiteThread() {};
    virtual int Init() { return ACLLITE_OK; };
    virtual int Process(int msgId, shared_ptr<void> msgData) = 0;                         
    int SelfInstanceId() { return instanceId_; }
    string& SelfInstanceName() { return instanceName_; }
    int BaseConfig(int instanceId, const string& threadName);

private:   
    int instanceId_;
    string instanceName_;
    bool baseConfiged_;
    bool isExit_;
};

struct AclLiteThreadParam {
    AclLiteThread* threadInst = nullptr;
    string threadInstName = "";
    int threadInstId = INVALID_INSTANCE_ID;
};