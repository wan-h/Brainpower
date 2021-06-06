#include <stdio.h>
#include "test.h"

/*
生成动态链接库
-fPIC，这可以使gcc产生于位置无关的代码
使用-shared，指示生成一个共享库文件
gcc sum.cpp max.cpp -Wall -fPIC -shared -o libtest.so 

使用动态链接文件
gcc test.cpp -Wall -L. -ltest -o test

添加动态链接库环境变量共享使用
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
*/


int main(){
    printf("sum(4, 5)=%d\n", sumOP(4, 5));
    printf("max(4, 5)=%d\n", maxOP(4, 5));
    return 0;
}