#include "AclLiteThreadMgr.h"

namespace {
    const uint32_t kMsgQueueSize = 256;
    const uint32_t kWait10Milliseconds = 10000;
    const uint32_t kWaitThreadStart = 1000;
}

AclLiteThreadMgr::AclLiteThreadMgr(AclLiteThread* userThreadInstance, const string& threadName):
  isExit_(false),
  status_(THREAD_READY),
  userInstance_(userThreadInstance),
  name_(threadName),
  msgQueue_(kMsgQueueSize) {
}

AclLiteThreadMgr::~AclLiteThreadMgr() {
    userInstance_ = nullptr;
    while(!msgQueue_.Empty()) {
        msgQueue_.Pop();
    }
}

void AclLiteThreadMgr::CreateThread() {
    thread engine(&AclLiteThreadMgr::ThreadEntry, (void *)this);
    engine.detach();
}

void AclLiteThreadMgr::ThreadEntry(void* arg){
    AclLiteThreadMgr* thMgr = (AclLiteThreadMgr*)arg;
    AclLiteThread* userInstance = thMgr->GetUserInstance();
    if (userInstance == nullptr) {
        printf("AclLite thread exit for user thread instance is null");
        return;
    }
    
    string& instName = userInstance->SelfInstanceName();
    
    int ret = userInstance->Init();
    if (ret) {
        printf("Thread %s init error %d, thread exit", 
                          instName.c_str(), ret);
        thMgr->SetStatus(THREAD_ERROR);
        return;
    }

    thMgr->SetStatus(THREAD_RUNNING);
    while(THREAD_RUNNING == thMgr->GetStatus()) {
        // get data from queue
        shared_ptr<AclLiteMessage> msg = thMgr->PopMsgFromQueue();
        if(msg == nullptr) {
            usleep(kWait10Milliseconds);
            continue;
        }
        // call function to process thread msg
        ret = userInstance->Process(msg->msgId, msg->data);
        msg->data = nullptr;
        if (ret) {
            printf("Thread %s process function return "
                              "error %d, thread exit", instName.c_str(), ret);
            thMgr->SetStatus(THREAD_ERROR);
            return;
        } 
        usleep(0);
    }
    thMgr->SetStatus(THREAD_EXITED);

    return;
}

int AclLiteThreadMgr::WaitThreadInitEnd() {
	while(true) {
		if (status_ == THREAD_RUNNING) {
			break;
		} else if (status_ > THREAD_RUNNING) {
            string& instName = userInstance_->SelfInstanceName();
			printf("Thread instance %s status change to %d, "
							  "app start failed", instName.c_str(), status_);							
			return ACLLITE_ERROR_START_THREAD;
		} else {
			usleep(kWaitThreadStart);
		}
	}

	return ACLLITE_OK;
}

int AclLiteThreadMgr::PushMsgToQueue(shared_ptr<AclLiteMessage>& pMessage) {
    if (status_ != THREAD_RUNNING) {
        printf("Thread instance %s status(%d) is invalid, "
                          "can not reveive message", name_.c_str(), status_);
        return ACLLITE_ERROR_THREAD_ABNORMAL;
    }
    return msgQueue_.Push(pMessage)? ACLLITE_OK : ACLLITE_ERROR_ENQUEUE;
}