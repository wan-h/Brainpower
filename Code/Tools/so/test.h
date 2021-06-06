#ifndef TEST_H
#define TEST_H
#ifdef __cplusplus
// extern "C"的主要作用就是为了能够正确实现C++代码调用其他 C语言 代码。 
// 加上extern "C"后，会指示编译器这部分代码按C语言（而不是C++）的方式进行编译
extern "C"{
#endif

int sumOP(int a, int b);
int maxOP(int a, int b);

#ifdef __cplusplus
}
#endif
#endif