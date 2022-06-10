## Effective C++
### 条款01：视c++为一个语言联邦  
请记住：  
* C++高效变成守则视情况而变化，取决于你使用C++的那一部分。

理解：  
* C++有多种次语言(C、Object-Oriented C++、Template C++、STL),每个次语言都有自己的规约。  

---  

### 条款02：尽量以const,enum,inline替换#define  
请记住：  
* 对于单纯常量，最好以const对象或enums替换#define。  
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
    // 对于不支持以上赋值操作的编译环境可以使用enums，这是一种比较hack的方法
    class Example
    {
    private:
        enum { NumTurns = 5 };
    }
    ```
* 对于形似函数的宏(macros)，最好改用inline函数替换#define。  
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
因为这个名字没有进入几号表，所以有时候很难debug。  
* 宏定义函数容易出错，例如`CALL_WITH_MAX(++a, b)`时a被加了两次,
其次内联函数也不用考虑括号啥问题，也遵守函数的作用域。  

---  

### 条款03：尽可能使用const  
请记住：  
* 将某些东西申明为const可以帮助编译器侦测出错误做法。const可被施加于任何作用域内的对象、函数参数、函数返回类型、成员函数本体。  
* 编译器强制实施bitwise constness，但你编写程序时应该使用“概念上的常量性”。  
* 当const和non-const成员函数有着实质等价的实现时，令non-const版本调用const版本可避免代码重复。
    ```C++
    class TextBlock
    {
    public:
        ...
        // 常函数且返回常引用
        const char& operator[](std::size_t position) const
        {
            ...
            ...
            ...
            return text[position]
        }
        // 普通函数
        char& operator[](std::size_t position)
        {
            // 返回值再转换为非常量
            const_cast<char&>(
                // 将当前类安全转换为常量后调用[]操作，相当于调用上面的函数
                static_cast<const TextBlock&>(*this)[position]
            );
        }
    ...
    }
    ```

理解：
* 比较常见的场景就是函数传参的时候，能够加const的就叫const。  

---

### 条款04：确定对象被使用前已先被初始化  
请记住：  
* 为内置型对象进行手工初始化，因为c++不保证初始化他们。  
* 构造函数最好使用成员初值列，而不是在构造函数本体内使用赋值操作。初值列列出的成员变量，其排列次序应该和它们在class中的声明次序相同。  
    ```C++
    class PhoneNumber {...}
    class ABEntry 
    {
    public:
        ABEntry(const std::string& name, const std::string& address, 
        const std::list<PhoneNumber>& phones);
    private:
        std::string theName;
        std::string theAddress;
        std::list<PhoneNumber> thePhones;
        int numTimesConsulted;
    };

    ABEntry::ABEntry(const std::string& name, const std::string& address, 
                    const std::list<PhoneNumber>& phones)
    {
        // 这些是赋值，而非初始化
        theName = name;
        theAddress = address;
        thePhones = phones;
        numTimesConsulted = 0;
    }
    // 替换为
    ABEntry::ABEntry(const std::string& name, const std::string& address, 
                    const std::list<PhoneNumber>& phones)
    // 这些都是初始化，次序和声明次序一致
    :theName(name),
    theAddress(address),
    thePhones(phones),
    numTimesConsulted(0)
    {}
    ```  
* 为避免“跨编译单元之初始化次序”问题，请以local static对象替换non-local static对象。  
    ```c++
    // 一个源码文件内容
    class FileSystem 
    {
    public:
        ...
        std::size_t numDisks() const;
        ...
    };
    extern FileSystem tfs;
    // 另一个源码文件内容
    class Directory
    {
    public:
        Directory(params);
        ...
    };
    Directory::Directory(params)
    {
        // 这个地方必须要tfs已经被初始化了
        // 但是不同源文件的初始化次序是不确定的
        ...
        std::size_t disks = tfs.numDisks();
        ...
    }
    // 客户决定创建一个Directory对象
    Directory tmpDir(params);

    // 替换为

    // 一个源码文件内容
    class FileSystem {...}; // 同前
    FileSystem& tfs()
    {
        static FileSystem fs;
        return fs;
    }
    // 另一个源码文件内容
    class Directory {...}; // 同前
    Directory::Directory(params)
    {
        // 这个地方必须要tfs是函数调用
        ...
        std::size_t disks = tfs().numDisks();
        ...
    }
    // 客户决定创建一个Directory对象
    Directory& tmpDir()
    {
        static Directory td;
        return td;
    }
    ```  

理解：  
* 构造函数里面已经是赋值操作，在构造函数之前，成员已经被default进行了初始化，所有使用初值列来进入构造函数之前对成员进行初始化  
* 为保证一个对象是被初始化的，可以用一个函数获取对象实例，函数内部维护一个local static对象，这其实就是单例模式的用法