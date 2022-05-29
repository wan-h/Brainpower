#include "AclLiteApp.h"
#include "AclLiteThreadMgr.h"

using namespace std;

namespace {
const uint32_t kWaitInterval = 10000;
const uint32_t kThreadExitRetry = 3;
}

AclLiteApp::AclLiteApp():isReleased_(false), waitEnd_(false){
    Init();
}

AclLiteApp::~AclLiteApp(){
    ReleaseThreads();
}

int AclLiteApp::Init() {
    AclLiteThreadMgr* thMgr = new AclLiteThreadMgr(nullptr, "main");
    threadList_.push_back(thMgr);
    thMgr->SetStatus(THREAD_RUNNING);
    return ACLLITE_OK;
}

int AclLiteApp::CreateAclLiteThread(AclLiteThread* thInst, const string& instName)
{
    int instId = CreateAclLiteThreadMgr(thInst, instName);
    if (instId == INVALID_INSTANCE_ID) {
        printf("Add thread instance %s failed", instName.c_str());
        return INVALID_INSTANCE_ID;
    }

    threadList_[instId]->CreateThread();	
    int ret = threadList_[instId]->WaitThreadInitEnd();
    if (ret != ACLLITE_OK) {
        printf("Create thread failed, error %d", ret);
        return INVALID_INSTANCE_ID;
    }

    return 	instId;
}

int AclLiteApp::CreateAclLiteThreadMgr(AclLiteThread* thInst, const string& instName){
    if (!CheckThreadNameUnique(instName)) {
        printf("The thread instance name is not unique");
        return INVALID_INSTANCE_ID;
    }

    int instId = threadList_.size();	
    int ret = thInst->BaseConfig(instId, instName);
    if (ret != ACLLITE_OK) {
        printf("Create thread instance failed for error %d", ret);
        return INVALID_INSTANCE_ID;
    }
        
    AclLiteThreadMgr* thMgr = new AclLiteThreadMgr(thInst, instName);	
    threadList_.push_back(thMgr);

    return instId;
}

bool AclLiteApp::CheckThreadNameUnique(const string& threadName) {
    if (threadName.size() == 0) return true;

    for (size_t i = 0; i < threadList_.size(); i++) {
        if (threadName == threadList_[i]->GetThreadName()) {
            return false;
        }
    }

    return true;
}

int AclLiteApp::Start(vector<AclLiteThreadParam>& threadParamTbl) {
    for (size_t i = 0; i < threadParamTbl.size(); i++) {
        int instId = CreateAclLiteThreadMgr(threadParamTbl[i].threadInst,
                                            threadParamTbl[i].threadInstName);
        if (instId == INVALID_INSTANCE_ID) {
            printf("Create thread instance failed");
            return ACLLITE_ERROR;
        }
        threadParamTbl[i].threadInstId = instId;
    }
    //Note:The instance id must generate first, then create thread,
    //for the user thread get other thread instance id in Init function
    for (size_t i = 0; i < threadParamTbl.size(); i++) {
        threadList_[threadParamTbl[i].threadInstId]->CreateThread();
    }

    for (size_t i = 0; i < threadParamTbl.size(); i++) {
        int instId = threadParamTbl[i].threadInstId;
        int ret = threadList_[instId]->WaitThreadInitEnd();
        if (ret != ACLLITE_OK) {
            printf("Create thread %s failed, error %d", 
                              threadParamTbl[i].threadInstName.c_str(), ret);
            return ret;
        } 
    }
    
    return ACLLITE_OK;
}

int AclLiteApp::GetAclLiteThreadIdByName(const string& threadName) {
    if (threadName.empty()) {
        printf("search name is empty");
        return INVALID_INSTANCE_ID;
    }

    for (uint32_t i = 0; i < threadList_.size(); i++) {
        if (threadList_[i]->GetThreadName() == threadName) {
            return i;
        }
    }
    
    return INVALID_INSTANCE_ID;
}

int AclLiteApp::SendMessage(int dest, int msgId, shared_ptr<void> data) {
    if ((uint32_t)dest > threadList_.size()) {
        printf("Send message to %d failed for thread not exist", dest);
        return ACLLITE_ERROR_DEST_INVALID;
    }

    shared_ptr<AclLiteMessage> pMessage = make_shared<AclLiteMessage>();
    pMessage->dest = dest;
    pMessage->msgId = msgId;
    pMessage->data = data;
    
    return threadList_[dest]->PushMsgToQueue(pMessage);
}

void AclLiteApp::Wait() {
    while (true) {        
        usleep(kWaitInterval);
        if (waitEnd_) break;
    }
    threadList_[kMainThreadId]->SetStatus(THREAD_EXITED);
}

bool AclLiteApp::CheckThreadAbnormal() {
    for (size_t i = 0; i < threadList_.size(); i++) {
        if (threadList_[i]->GetStatus() == THREAD_ERROR) {
            return true;
        }
    }

    return false;
}

void AclLiteApp::Wait(AclLiteMsgProcess msgProcess, void* param) {
    AclLiteThreadMgr* mainMgr = threadList_[0];

    if (mainMgr == nullptr) {
        printf("AclLite app wait exit for message process function is nullptr");
        return;
    }

    while (true) {
        if (waitEnd_) break;

        shared_ptr<AclLiteMessage> msg = mainMgr->PopMsgFromQueue();
        if (msg == nullptr) {
            usleep(kWaitInterval);
            continue;
        }
        int ret = msgProcess(msg->msgId, msg->data, param);
        if (ret) {
            printf("AclLite app exit for message %d process error:%d", msg->msgId, ret);
            break;
        }
    }
    threadList_[kMainThreadId]->SetStatus(THREAD_EXITED);
}

void AclLiteApp::Exit() {
    ReleaseThreads();
}

void AclLiteApp::ReleaseThreads() {
    if (isReleased_) return;
    threadList_[kMainThreadId]->SetStatus(THREAD_EXITED);

    for (uint32_t i = 1; i < threadList_.size(); i++) {
        if ((threadList_[i] != nullptr) && 
            (threadList_[i]->GetStatus() == THREAD_RUNNING))
             threadList_[i]->SetStatus(THREAD_EXITING);
    }

    int retry = kThreadExitRetry; 
    while(retry >= 0) {
        bool exitFinish = true;
        for (uint32_t i = 0; i < threadList_.size(); i++) {
            if (threadList_[i] == nullptr) 
                continue;
            if (threadList_[i]->GetStatus() > THREAD_EXITING) {
                delete threadList_[i];
                threadList_[i] = nullptr;
                printf("AclLite thread %d released\n", i);
            } else {
                exitFinish = false;
            }
        }

        if (exitFinish)
            break;

        sleep(1);
        retry--;
    }
    isReleased_ = true;
}

AclLiteApp& CreateAclLiteAppInstance() {
    return AclLiteApp::GetInstance();
}

AclLiteApp& GetAclLiteAppInstance() {
    return AclLiteApp::GetInstance();
}

int SendMessage(int dest, int msgId, shared_ptr<void> data) {
    AclLiteApp& app = AclLiteApp::GetInstance();
    return app.SendMessage(dest, msgId, data);
}

int GetAclLiteThreadIdByName(const string& threadName) {
    AclLiteApp& app = AclLiteApp::GetInstance();
    return app.GetAclLiteThreadIdByName(threadName);
}
