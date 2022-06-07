## Effective C++
### 条款01：视c++为一个语言联邦  
请记住：  
* C++高效变成守则视情况而变化，取决于你使用C++的那一部分

理解：  
* C++有多种次语言(C、Object-Oriented C++、Template C++、STL),每个次语言都有自己的规约  

---  

### 条款02：尽量以const,enum,inline替换#define  
请记住：  
* 对于单纯常量，最好以const对象或enums替换#define  
```C++
#define ASPECT_RATIO 1.653
// 替换为
const double AspectRation = 1.653;

// 如果是定义个常量指针，需要写两个const
const char* const authorNmae = "Wan Hui";

// 如果是定义类的专属常量
class Example
{
private:
    static const double AspectRation = 1.653;
}
```
* 对于形似函数的宏(macros)，最好改用inline函数替换#define  
```C++
#define CALL_WITH_MAX(a, b) f((a) > (b) ? (a) : (b))
// 替换为
template<typename T>
inline void callWithMax(const T& a, const T& b)
{
    f(a > b ? a : b);
}
```

理解：  
* define会导致编译器在编译阶段就将宏替换掉，如果存在错误不会出现宏的名字，
因为这个名字没有进入几号表，所以有时候很难debug  
* 宏定义函数容易出错，例如`CALL_WITH_MAX(++a, b)`时a被加了两次,
其次内联函数也不用考虑括号啥问题，也遵守函数的作用域