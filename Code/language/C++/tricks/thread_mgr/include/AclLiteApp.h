#pragma once

#include "AclLiteThreadMgr.h"
#include "AclLiteError.h"

namespace {
    int kMainThreadId = 0;
}

typedef int (*AclLiteMsgProcess)(uint32_t msgId, shared_ptr<void> msgData, void* userData);

class AclLiteApp {
public:
    /**
    * @brief Constructor
    */
    AclLiteApp();
	AclLiteApp(const AclLiteApp&) = delete;
	AclLiteApp& operator=(const AclLiteApp&) = delete;

    /**
    * @brief Destructor
    */
    ~AclLiteApp();

    /**
     * @brief Get the single instance of AclLiteApp
     * @return Instance of AclLiteApp
     */ 
	static AclLiteApp& GetInstance() {
		static AclLiteApp instance;
		return instance;
	}

    /**
     * @brief Create one app thread
     * @return Result of create thread
     */ 
    int CreateAclLiteThread(AclLiteThread* thInst, const std::string& instName);
    int Start(vector<AclLiteThreadParam>& threadParamTbl);
    void Wait();
    void Wait(AclLiteMsgProcess msgProcess, void* param);
    int GetAclLiteThreadIdByName(const std::string& threadName);
    int SendMessage(int dest, int msgId, shared_ptr<void> data);
    void WaitEnd() { waitEnd_ = true; }
    void Exit();

private:
    int Init();
    int CreateAclLiteThreadMgr(AclLiteThread* thInst, const std::string& instName);
    bool CheckThreadAbnormal();
    bool CheckThreadNameUnique(const std::string& threadName);
    void ReleaseThreads();

private:
    bool isReleased_;
    bool waitEnd_;
    std::vector<AclLiteThreadMgr*> threadList_;
};

AclLiteApp& CreateAclLiteAppInstance();
AclLiteApp& GetAclLiteAppInstance();
int SendMessage(int dest, int msgId, shared_ptr<void> data);
int GetAclLiteThreadIdByName(const std::string& threadName);