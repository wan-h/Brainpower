#pragma once

#include <unistd.h>
#include <string>

struct AclLiteMessage {
    int dest;
    int msgId;
    std::shared_ptr<void> data = nullptr;
};
