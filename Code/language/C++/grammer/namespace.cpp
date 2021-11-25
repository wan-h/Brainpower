#include <iostream>
using namespace std;

namespace first_space{
    void func(){
        cout << "Inside first_space" << endl;
    }

    namespace second_space{
        void func(){
            cout << "Inside second_space" << endl;
        }
    }
}

namespace third_space{
    void func(){
        cout << "Inside third_space" << endl;
    }
}

using namespace first_space::second_space;

int main(){
    // 使用using空间
    func();
    // 指定空间
    third_space::func();

    return 0;
}