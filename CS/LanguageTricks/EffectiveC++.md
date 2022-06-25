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
    ```c++
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
    ```c++
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
    ```c++
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
    ```c++
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

---

### 条款05：了解C++默默编写并调用哪些函数  
请记住：  
* 编译器可以暗自为class创建default构造函数、copy构造函数、copy assignment操作符，以及析构函数。  
    ```c++
    class Empty
    {
    public:
        Empty() {...}                                   // default构造函数
        Empty(const Empty& rhs) {...}                   // copy构造函数
        ~Empty() {...}                                  // 析构函数

        Empty& operator=(const Empty& rhs) {...}        // copy assignment操作符
    }
    ```

理解：  
* 如果用户已经申明了对应的构造函数等，编译器就不会在为它创建默认的函数。  

---

### 条款06：若不想使用编译器自动生成的函数，就该明确拒绝  
请记住：  
* 为驳回编译器自动（暗自）提供的机能，可将相应的成员函数声明为private并且不予实现。使用像Uncopyable这样的base class也是一种做法。  
    ```c++
    class HomeForSale
    {
    public:
        ...
    private:
        ...
        // 这里不用实现函数，所以参数名字可以不写
        HomeForSale(const HomeForSale&);
        HomeForSale& operator=(const HomeForSale&);
    }
    ```

理解：  
* private中声明了就意味着编译器不会自动生成，放在private中意味着实例不可调用该函数，从而禁用了该函数。  

---  

### 条款07：为多态基类声明virtual析构函数
请记住：  
* polymorphic(带多态性质的)base classes应该声明一个virtual析构函数。如果class带有任何virtual函数，它就应该拥有一个virtual析构函数。  
    ```c++
    class TimeKeeper
    {
    public:
        TimeKeeper();
        ~TimeKeeper();
        ...
    };
    class AtomicClock: public TimeKeeper() {...}; // 原子钟
    class WaterClock: public TimeKeeper() {...}; // 水钟
    class WristClock: public TimeKeeper() {...}; // 腕表
    // 工厂函数
    TimeKeeper* ptk = getTimeKeeper();
    // 这个调用的是基类的析构函数而不是派生类的
    delete ptk;

    // TimeKeeper替换为
    class TimeKeeper
    {
    public:
        TimeKeeper();
        // 虚析构函数
        virtual ~TimeKeeper();
        ...
    };
    ```
* Classes的设计目的不是作为base classes使用，或不是为了具备多态性(polymorphically)，就不该声明virtual析构函数。  

理解：  
* 如果基类的析构函数不是虚函数，那么派生类在释放的时候调用的是基类的析构函数没有调用派生类的析构函数就有可能导致内存泄露等异常情况，如果基类是一个虚析构函数，那么就会先调用派生类的析构再调用基类的析构。  
* 声明析构函数会消耗额外的资源，所有有上面第二条。

---  

### 条款08：别让异常逃离析构函数
请记住：  
* 析构函数绝对不要吐出异常。如果一个被析构函数调用的函数可能抛出异常，析构函数应该捕捉任何异常，然后吞下它们（不传播）或结束程序。  
    ```c++
    // 假设一个数据库连接管理类在析构函数调用关闭连接
    class DBConn
    {
    public: 
        ...
        ~DBConn()
        {   
            // 如果这里报出异常就会导致异常传播，内存泄露等不明确行为，总之就是不好
            db.close();
        }
    private:
        DBConnection db;
    }

    // 修改析构函数
    DBConn::~DBConn()
    {
        try { db.close(); }
        catch (...)
        {
            // 记下对close的调用失败

            // 选项1
            // 如果不马上结束的话，程序会离开析构函数，导致异常传播，因此强迫当场结束
            // std::abort();

            // 选项2
            // 吞下这个异常，记录错误就行，这会导致程序继续执行，这种只能说是用来暂时规避一下无关紧要的错误
        }
    }

    ```
* 如果客户需要对某个操作函数运行期间抛出的异常做出反应，那么class应该提供一个普通函数（而非在析构函数中）执行该操作。  
    ```c++
    // 改写类，把异常处理交由用户处理，这样至少被异常转移到了析构函数之外，也给客户提供了处理机会
    class DBConn
    {
    public:
        ...
        // 提供客户使用的新函数
        void close()
        {
            db.close();
            closed = true;
        }
        ~DBCoon()
        {
            // 双保险
            if (!closed)
            {
                try {
                    db.close();
                } catch (...) {
                    // 记下调用失败
                    ...
                }
            }
        }
    private:
        DBConnection db;
        bool closed;
    }
    ```

理解：  
* 编写析构函数的时候，注意异常抛出的问题，最好让客户自己去调用可能产生异常的操作，不要自作聪明包到析构函数里面去。  

---

### 条款09：绝不在析构和析构过程中调用virtual函数
请记住：  
* 在构造和析构期间不要调用virtual函数，因为这类调用从不下降至derived class(比起当前执行构造函数和析构函数的那层)。
    ```c++
    class Transaction()
    {
    public:
        Transaction()
        {
            // 这里调用了non-virtual
            // 正是因为这里包了一层，编译的时候是不会报错的
            init();
        }
        virtual void logTransaction() const = 0;
    private:
        void init()
        {
            ...
            // 这里调用的virtual
            logTransaction();
        }
    }
    // 派生类
    class BuyTransaction: public Transaction
    {
    public:
        virtual void logTransaction() const;
        ...
    }
    // 实例化
    // 这里由于会先调用父类的构造函数，但是父类又调用的虚函数，派生类都还没有实例化，所以逻辑上就是不同的
    // 如果父类是纯虚函数就会报错，如果不是就坑了，就会调用父类的虚函数实现
    BuyTransaction b;

    // 修改类实现
    class Transaction
    {
    public:
        explicit Transaction(const std::string& logInfo)
        {
            ...
            logTransaction(logInfo);
        }
        // non-virtual函数
        void logTransaction(const std::string& logInfo) const;
        ...
    }
    // 派生类
    class BuyTransaction: public Transaction
    {
    public:
        // 派生类把必要信息传递给基类构造函数，让基类调用non-virtual函数
        BuyTransaction(parameters)
        : Transaction(createLogString(parameters))
        {
            ...
        }
        ...
    private:
        // 因为构造函数还没执行的时候(初值列)就调用的该函数，所以是static定义的
        static std::string createLogString(parameters);
    }
    ```  

理解：  
* 凡是遇到构造和析构函数调用虚函数的都要改写一下。  

---

### 条款10：令operator=返回一个reference to *this
请记住：  
* 令赋值(assignment)操作符返回一个reference to *this。  
    ```c++
    class Widget
    {
    public:
        ...
        Widget& operator=(const Widget& rhs)
        {
            ...
            // this是一个指向当前实例的指针
            // *this就是接指针引用，拿到的就是当前实例对象本身
            return *this;
        }
        // 使用所有赋值相关运算
        Widget& operator+=(const Widget& rhs)
        {
            ...
            return *this;
        }
        Widget& operator+=(int rhs)
        {
            ...
            return *this;
        }
        ...
    }
    ```
  
理解：  
* 这就是一个标准协议，大家都是这么玩的，跟着这样玩就行  

---

### 条款11：在operator=中处理“自我赋值”  
请记住：  
* 确保当前对象自我赋值时operator=有良好的行为。其中技术包含“来源对象”和“目标对象”的地址、精心周到的语句顺序、以及copy-and-swap。  
    ```c++
    class Bitmap {...};
    class Widget 
    {
    public:
        // 这是一份不安全的实现
        // 如果赋值对象rhs就是自己，那么就会导致销毁pb的时候就是销毁的自己的
        Widget& operator=(const Widget& rhs)
        {
            delete pb;
            pb = new Bitmap(*rhs.pb);
            return *this;
        }
    private:
        Bitmap* pb;
    }

    // 修改类实现
    class Widget 
    {
    public:
        // 这是一份不安全的实现
        // 如果赋值对象rhs就是自己，那么就会导致销毁pb的时候就是销毁的自己的
        Widget& operator=(const Widget& rhs)
        {
            // 一种方法是加一个证同测试，这个加上提高效率
            // if (this == &rhs) return *this;

            // 另一种只要严格控制语句顺序就可以了
            // 先赋值再删除
            Bitmap* pOrig = pb;
            pb = new Bitmap(*rhs.pb);
            delete pOrig;
            return *this;
        }
    private:
        Bitmap* pb;
    }
    ```
* 确定任何函数如果操作一个以上的对象，而其中多个对象是同一个对象时，其行为仍然正确。  


理解：  
* 写运算符的时候要考虑到对象就是自己本身，这是一种异常情况，按照上面的套路写就行。