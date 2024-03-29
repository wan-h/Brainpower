## Effective C++
### 让自己习惯C++
* [条款01：视c++为一个语言联邦](EffectiveC++#条款01视c为一个语言联邦)  
* [条款02：尽量以const,enum,inline替换#define](EffectiveC++#条款02尽量以constenuminline替换define)  
* [条款03：尽可能使用const](EffectiveC++#条款03尽可能使用const)  
* [条款04：确定对象被使用前已先被初始化](EffectiveC++#条款04确定对象被使用前已先被初始化)  

### 构造/析构/赋值运算
* [条款05：了解C++默默编写并调用哪些函数](EffectiveC++#条款05了解c默默编写并调用哪些函数)  
* [条款06：若不想使用编译器自动生成的函数，就该明确拒绝](EffectiveC++#条款06若不想使用编译器自动生成的函数就该明确拒绝)  
* [条款07：为多态基类声明virtual析构函数](EffectiveC++#条款07为多态基类声明virtual析构函数)  
* [条款08：别让异常逃离析构函数](EffectiveC++#条款08别让异常逃离析构函数)  
* [条款09：绝不在析构和析构过程中调用virtual函数](EffectiveC++#条款09绝不在析构和析构过程中调用virtual函数)  
* [条款10：令operator=返回一个reference to *this](EffectiveC++#条款10令operator返回一个reference-to-this)  
* [条款11：在operator=中处理“自我赋值”](EffectiveC++#条款11在operator中处理自我赋值)  
* [条款12：复制对象时勿忘其每一成分](EffectiveC++#条款12复制对象时勿忘其每一成分)  

### 资源管理
* [条款13：以对象管理资源](EffectiveC++#条款13以对象管理资源)  
* [条款14：在资源管理类中小心copying行为](EffectiveC++#条款14在资源管理类中小心copying行为)  
* [条款15：在资源管理类中提供对原始资源的访问](EffectiveC++#条款15在资源管理类中提供对原始资源的访问)  
* [条款16：成对使用new和delete时采用相同的形式](EffectiveC++#条款16成对使用new和delete时采用相同的形式)  
* [条款17：以独立语句将newed对象置入智能指针](EffectiveC++#条款17以独立语句将newed对象置入智能指针)  

### 设计与声明  
* [条款18：让接口容易正确使用，不易被误用](EffectiveC++#条款18让接口容易正确使用不易被误用)  
* [条款19：设计class犹如设计type](EffectiveC++#条款19设计class犹如设计type)  
* [条款20：宁以pass-by-reference-to-const替换pass-by-value](EffectiveC++#条款20宁以pass-by-reference-to-const替换pass-by-value)  
* [条款21：必须返回对象时，别妄想返回其reference](EffectiveC++#条款21必须返回对象时别妄想返回其reference)  
* [条款22：将成员变量声明为private](EffectiveC++#条款22将成员变量声明为private)  
* [条款23：宁以non-member、non-friend替换member函数](EffectiveC++#条款23宁以non-membernon-friend替换member函数)  
* [条款24：若所有参数皆需类型转换，请为此采用non-member函数](EffectiveC++#条款24若所有参数皆需类型转换请为此采用non-member函数)  
* [条款25：考虑写出一个不抛异常的swap函数](EffectiveC++#条款25考虑写出一个不抛异常的swap函数)  

### 实现  
* [条款26：尽可能延后变量定义式的出现时间](EffectiveC++#条款26尽可能延后变量定义式的出现时间)  
* [条款27：尽量少做转型动作](EffectiveC++#条款27尽量少做转型动作)  
* [条款28：避免返回handles指向对象内部成分](EffectiveC++#条款28避免返回handles指向对象内部成分)  
* [条款29：为异常安全而努力是值得的](EffectiveC++#条款29为异常安全而努力是值得的)  
* [条款30：透彻了解inlining的里里外外](EffectiveC++#条款30透彻了解inlining的里里外外)  
* [条款31：将文件间的编译依存关系将至最低](EffectiveC++#条款31将文件间的编译依存关系将至最低)  

### 继承与面向对象设计
* [条款32：确定你的public继承塑模出is-a关系](EffectiveC++条款32：确定你的public继承塑模出is-a关系)  
* [条款33：避免遮掩继承而来的名称](EffectiveC++条款33：避免遮掩继承而来的名称)  
* [条款34：区分接口继承和实现继承](EffectiveC++条款34：区分接口继承和实现继承)