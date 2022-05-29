#include "AclLiteThread.h"

AclLiteThread::AclLiteThread():
  instanceId_(INVALID_INSTANCE_ID),
  instanceName_(""),
  baseConfiged_(false) {
}

int AclLiteThread::BaseConfig(int instanceId,
                                   const string& threadName) {
    if (baseConfiged_) {
        return ACLLITE_ERROR_INITED_ALREADY; 
    }

    instanceId_ = instanceId;
    instanceName_.assign(threadName.c_str());

    baseConfiged_ = true;

    return ACLLITE_OK;
}

