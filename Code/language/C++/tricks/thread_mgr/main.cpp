#include <iostream>
#include "AclLiteThread.h"
#include "AclLiteApp.h"
#include "AclLiteError.h"

using namespace std;

class TestThread: public AclLiteThread
{
public:
    ~TestThread()
    {
        cout << "TestThread say goodbye." << endl;
    }
    int Init()
    {
        cout << "TestThread say hello." << endl;
        return ACLLITE_OK;
    }
    int Process(int msgId, shared_ptr<void> msgData)
    {
        string* data = (string*)msgData.get();
        cout << "Get msdId: " << msgId << endl;
        cout << "Get msg: " << *data << endl;
        return ACLLITE_OK;
    }
};

// #define MSG_APP_EXIT 1000
// int MainThreadProcess(uint32_t msgId,shared_ptr<void> msgData, void* userData) {
//     if (msgId == MSG_APP_EXIT) {
//         AclLiteApp& app = GetAclLiteAppInstance();
//         app.WaitEnd();
//         printf("Receive exit message, exit now");
//     }
//     return ACLLITE_OK;
// }

int main()
{
    AclLiteApp& app = CreateAclLiteAppInstance();
    const string name = "test1";
    AclLiteThread *testThread = new TestThread();
    app.CreateAclLiteThread(testThread, name);

    int dest = app.GetAclLiteThreadIdByName(name);
    int msgId = 0;
    shared_ptr<void> message = make_shared<string>("hello world");
    app.SendMessage(dest, msgId, message);
    // app.Wait(MainThreadProcess, nullptr);
    app.Exit();
    delete testThread;
    return 0;
}