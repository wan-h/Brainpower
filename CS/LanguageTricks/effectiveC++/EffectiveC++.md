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

---

### 条款12：复制对象时勿忘其每一成分
请记住：  
* Copying函数应该确保复制“对象内的所有成员变量”及“所有base class成分”。  
    ```c++
    class PriorityCustomer: public Customer
    {
    public:
        ...
        PriorityCustomer(const PriorityCustomer& rhs);
        PriorityCustomer& operator=(const PriorityCustomer& rhs);
        ...
    private:
        int priority;
    };
    // 初值列调用父类复制构造函数
    PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs)
    : Customer(rhs)
    priority(rhs.priority)
    {
        logCall("PriorityCustomer copy constructor");
    }
    PriorityCustomer& 
    PriorityCustomer::operator=(const PriorityCustomer& rhs)
    {
        logCall("PriorityCustomer copy assignment operator");
        // 调用父类的赋值操作
        Customer::operator(rhs);
        priority = rhs.priority;
        return *this;
    }
    ```
* 不要尝试以某个copying函数实现另一个copying函数。应该将共同机能放进第三个函数，并由两个copying函数共同调用。  

理解：  
* 派生类在自己编写拷贝函数或赋值操作符时要考虑到父类的所有成员，不然部分成员变量将被默认初始化。  

---

### 条款13：以对象管理资源
请记住：  
* 为防止资源泄露，请使用RAII(Resource Acquisition Is Initialization 资源取得时机便是初始化)对象，他们在构造函数中获得资源并在构析函数中释放资源。  
* 两个常被使用的RAII classes分别是tr1::shared_ptr和auto_ptr。前者通常是较佳选择，因为其copy行为比较直观。若选择auto_ptr，复制动作会使他（被复制物）指向null。  
    ```c++
    class Investment {...};
    void f()
    {
        // 工厂函数获取Investment实例
        Investment* pInv = createInvestnebt();
        // 中间处理就有可能导致提前退出以致于没有释放对象
        ...
        // 释放对象
        delete pInv;
    }

    // 由于上面释放资源都是自己管理的，容易出错，我们希望对象离开区块时自己释放
    // 修改f
    void f()
    {
        std::auto_ptr<Investment> pInv1(createInvestment());
        ...
        // 该方法唯一的问题就是，这样的copy会导致pInv1=null
        // 因为智能指针的获得者具有唯一拥有权
        std::auto_ptr<Investment> pInv2(pInv1);
    } // 函数块结束时会调用智能指针的析构函数删除对象

    // 于是我们可以使用“引用计数型智慧指针”(RCSP)可以避免以上的问题，只要不被环状引用
    void f()
    {
        std::tr1::shared_ptr<Investment> pInv1(createInvestment());
        // pInv1 pInv2指向同一个对象
        std::auto_ptr<Investment> pInv2(pInv1);
        ...
    }
    ```  

理解:  
* 删除对象这种资源操作尽可能不要自己来做，通过智能指针等方式，让对象析构函数自我管理，避免出现纰漏。  

---

### 条款14：在资源管理类中小心copying行为
请记住：  
* 复制RAII(Resource Acquisition Is Initialization 资源取得时机便是初始化)对象必须一并复制它所管理的资源，所以资源的coping行为决定RAII对象的coping行为。  
* 普遍而常见的RAII class copying行为是：抑制coping、施引引用计数法。不过其他行为也都可能被实现。  
    ```c++
    class Lock
    {
    public:
        explicit Lock(Mutex* pm): mutexPtr(pm)
        {
            lock(mutexPtr);
        }
        ~Lock()
        {
            unlock(mutexPtr);
        }
    private:
        Mutex* mutexPtr;
    };
    // 用户对于Lock的用法符合RAII方式
    Mutex m; //定义互斥器
    ...
    {
        Lock ml(&m); // 构造函数锁定互斥锁
        ...
        // Lock ml2(ml1) 这个操作不允许，会报错
    } // 区块结束，析构函数释放互斥锁

    // 针对以上的copy操作有两种解法，一种是禁止coping操作
    class Lock: private Uncopyable // 禁止赋值操作，见条款6
    {
    public:
        ...
    }
    // 一种是对资源引用计数
    // 关键点就是shared_ptr允许指定删除器，默认是delete指向的资源
    class Lock
    {
    public:
        explicit Lock(Mutex* pm)
        :mutexPtr(pm, unlock) // 以unlock作为函数作为shared_ptr的删除器
        {
            lock(mutexPtr.get());
        }
    private:
        // 使用shared_ptr替代raw pointer
        std::tr1::shared_ptr<Mutex> mutexPtr;
    };
    ```

理解：  
* 对于资源管理类本身的copying操作使用引用计数来解决。

---

### 条款15：在资源管理类中提供对原始资源的访问
请记住：  
* APIs往往要求访问原始资源，所以每一个RAII class应该提供一个“取得其所管理之资源”的办法。  
* 对原始资源的访问可能经由显式转换或隐式转换。一般而言显式转换比较安全，但隐式转换对客户比较方便。  
    ```c++
    class Font
    {
    public:
        explicit Font(FontHandle fh)
        :f(fh)
        { }
        ~Font() { releaseFont(f); }
        // 显式转换函数
        FontHandle get() const { return f; }
    private:
        FontHandle f;
    }
    // 当我们想要调用原始资源时
    Font f(getFont()); // 工厂生产Font实例便通过Font管理类进行管理
    changeFontSize(f.get(), newSize); // 通过Font的get方法显示转换调用
    ```

理解：  
* 资源管理类暴露一个显示获取原始资源的方法来有效处理源码对于原始资源的使用。  

---

### 条款16：成对使用new和delete时采用相同的形式  
请记住：  
* 如果你在new表达式中使用[]，必须在相应的delete表达式中也是用[]。如果你在new表达式中不使用[]，一定不要在相应的delete表达式中使用[]。  
    ```c++
    std::string* stringPtr1 = new std::string;
    std::string* stringPtr2 = new std::string[100];
    ...
    // 删除一个对象
    delete stringPtr1;
    // 删除一个由对象组成的数据
    delete stringPtr2[];
    ```

理解：  
* 注意数据对象删除一定要加delete。

---

### 条款17：以独立语句将newed对象置入智能指针
请记住：  
* 以独立语句将newed对象存储于（置于）智能智能内。如果不这样做，一旦异常被抛出，有可能导致难以察觉的资源泄露。  
    ```c++
    int priority();
    void processWidget(std::tr1::shared_ptr<Widget> pw, int priority);
    // 对processWidget函数调用可能存在问题
    // 如果priority调用在构造智能指针之前切抛出异常就会导致智能指针没有管理资源
    processWidget(std::tr1::shared_ptr<Widget>(new Widget), priority());

    // 分离语句即可
    std::tr1::shared_ptr<Widget> pw(new Widget);
    processWidget(ow, priority());
    ```

理解：  
* 当使用智能智能做资源管理的时候单独写这一句。

---

### 条款18：让接口容易正确使用，不易被误用
请记住：  
* 好的接口很容易被正确使用，不容易被误用。你应该在你所有接口中努力达成这些性质。  
* “促进正确使用”的办法包括接口的一致性，以及与内置类型的行为兼容。  
* “阻止误用”的办法包括建立新类型、限制类型上的操作，束缚对象值，以及消除客户的资源管理责任。  
    ```c++
    class Date
    {
    public:
        Date(int month, int day, int year);
    }

    //参数只做了int限制，很容易传递错误,通过类型定义做限制
    class Date
    {
    public:
        Date(const Month& month, const Day& day, const Year& year);
    }
    class Month
    {
    public:
        static Month Jan() { return Month(1); }
        static Month Fed() { return Month(2); }
        ...
        static Month Dec() { return Month(12); }
    private:
        explicit Month(int m);
        ...
    };
    class Day {...}
    class Year {...}

    Date d(Month::Mar(), Day(30), Year(1995));
    ```
* tr1::shared_ptr支持定制型删除器。这可防范DLL问题，可被用来自动接触互斥锁等等。
    ```c++
    // 工厂函数
    Investment* createInvestment();
    // 为了避免客户忘记使用智能指针进行管理，直接返回一个智能指针对象
    // 这样阻止用户产生内存泄露
    // 设置专属的deleter
    std::tr1::shared_ptr<Investment> createInvestment()
    {
        // getRidOfInvestment是引用为0时的删除器
        std::tr1::shared_ptr<Investment> retVal(static_cast<Investment*>(0), getRidOfInvestment);
        retVal = ...; // 令retVal指向正确对象
        return retVal;
    }
    ```

理解：  
* 接口设计尽可能保持和常见内置类型（容器等）命名等行为一致。  
* 接口设计竟可能避免客户犯错机会。  

---

### 条款19：设计class犹如设计type
请记住：  
* Class的设计就是type的设计，所以定义高效的classes是一种挑战，请确定你已经考虑过本条款覆盖的所有讨论主题。  
    * 新type的对象应该如何被创建和销毁？  
    * 对象的初始化和对象的赋值该有什么样的差别？  
    * 新type的对象如果被passed by value(以值传递)，意味着什么？  
    * 什么是新type的“合法值”？
    * 你的新type需要配合某个集成图系吗？  
    * 你的新type需要什么样的转换？  
    * 什么样的操作符和函数对此新type而言是合理的？  
    * 什么样的标准函数应该驳回？  
    * 谁该取用新type的成员？  
    * 什么是新type的“未声明接口”？  
    * 你的新type有多么一般化？  
    * 你真需要一个新type吗？  

理解：  
* 这个估计就得多练习，多看看优秀的类设计。  

---

### 条款20：宁以pass-by-reference-to-const替换pass-by-value
请记住：  
* 尽量以pass-by-reference-to-const替换pass-by-value。前者通常比较高效，并可避免切割问题。  
* 以上规则并不适用于内置类型，以及STL的迭代器和函数对象。对它们而言，pass-by-value往往比较适当。  

理解：  
* 编码规则就是在传递对象的时候尽可能的使用常引用传递，因为值传递会有多余的拷贝动作，但对于c++内置的一些int之类的，传值反而更快，所以内置对象传值就可以了。

---

### 条款21：必须返回对象时，别妄想返回其reference  
请记住：  
* 绝不要返回pointer或reference指向一个local stack对象，或返回reference指向一个heap-allocated对象，或返回pointer或reference指向一个local static对象而有可能同时需要多个这样的对象。条款4已经为“在单线程环境中合理返回reference指向一个local static对象”提供一份设计实例。  
    ```c++
    // 错误写法1
    const Rational& operator*(const Rational& lhs, const Rational& rhs)
    {
        Rational result(lhs.n * rhs.n, lhs.d * rhs.d);
        // result是一个local对象，函数退出就销毁了，所以这个实现很拉垮
        return result;
    }

    // 错误写法2
    const Rational& operator*(const Rational& lhs, const Rational& rhs)
    {
        Rational* result = new Rational(lhs.n * rhs.n, lhs.d * rhs.d);
        // 用户来delete合适?
        return *result;
    }
    Rational w, x, y, z;
    // 这种写法根本没有机会delete，直接就内存泄露了
    w = x * y * z;

    // 错误写法3
    const Rational& operator*(const Rational& lhs, const Rational& rhs)
    {
        static Rational result;
        result = ...;
        return *result;
    }
    // 遇到这种判断永远都是相等的
    if (operator==(operator*(a, b) operator*(c, d)))

    // 正确写法
    inline const Rational& operator*(const Rational& lhs, const Rational& rhs)
    {
        return Rational(lhs.n * rhs.n, lhs.d * rhs.d);
    }
    ```

理解：  
* 一般按照条例10写就可以了，一定返回一个对象的时候就直接返回其对象。  

---

### 条款22：将成员变量声明为private
请记住：  
* 切记将成员变量声明为private。这可赋予客户访问数据的一致性、可细微划分访问控制、允许约束条件获得保证，并提供class作者以充分的实现弹性。  
    ```c++
    // 确保变量成员都是private, 每个变量成员需要一个setter和getter函数来设置和获取
    class AccessLevels
    {
    public:
        ...
        int getReadOnly() const { return readOnly; }
        void setReadWrite(int value) { readWrite = value; }
        int getReadWrite() const { return readWrite; }
    private:
        int readOnly;
        int readWrite;
    }
    ```
* protected并不比public更具封装性。  

理解：  
* 成员变量的封装性和“成员变量的内容改变时可能造成的代码破坏量”成反比，比如获取一个变量时想要做一些操作就可以隐藏在getter和setter函数后面，这样的升级对于用户代码来讲是无感且不侵入的，总之这是一种良好的编程习惯，遵循这种习惯。  

---

### 条款23：宁以non-member、non-friend替换member函数
请记住：  
* 宁可拿non-member non-friend函数替换member函数。这样做可以增加封装性、包裹弹性和机能扩充性。  
    ```c++
    class WebBrowser
    {
    public:
        ...
        void clearCache();
        void clearHistory();
        void removeCookies();
        // 调用clearCache、clearHistory、removeCookies
        // void clearEverything();
        ...
    }
    // 这个non member函数是对clearEverything的替换
    // 这种替换实际是提高了封装性，就像变量都尽可能是private一样减少了用户可以改变的东西
    // 如果涉及到不同功能的函数还可以将non member函数声明在不同的头文件中
    void clearEverything(WebBrowser& wb)
    {
        wb.clearCache();
        wb.clearHistory();
        wb.removeCookies();
    }
    ```

理解：  
* 感觉很多时候还是直接写到类成员函数的，对于这种不访问成员变量的函数尽可能以non member的方式实现。  

---

### 条款24：若所有参数皆需类型转换，请为此采用non-member函数
请记住：  
* 如果你需要为某个函数的所有参数（包括被this指针所值的那个隐喻参数）进行类型转换，那么这个函数必须是个non-member。  
    ```c++
    class Rational
    {
    public:
        Rational(int numerator=0, int denominator=1);
        int numerator() const;
        int denominator() const;
        const Rational operator* (const Rational& rhs) const;
    private:
        ...
    };

    Rational oneHalf(1, 2);
    result = oneHalf * 2; // non-explicit构造函数情况系正常运作， 2 做了隐式的类型转换
    result = 2 * oneHalf; // 无法正常运行

    // 要想支持这种混合运算，可行之道就是让operator*成为一个non-member函数
    // 编译器会自动搜索这个实现做隐式转换
    const Rational operator*(const Rational& lhs, const Rational& rhs)
    {
        return Rational(lhs.numerator() * rhs.numerator(), lhs.denominator() * rhs.denominator());
    }
    ```

理解：  
* 以上其实可以用friend友元函数实现，但是无论合适能避免friend函数就应该避免，因为就像真实世界一样，朋友带来的麻烦往往多余其价值。  

---

### 条款25：考虑写出一个不抛异常的swap函数
请记住：  
* 当std::swap对你的类型效率不高时，提供一个swap成员函数，并确定这个函数不抛出异常。  
* 如果你提供一个member swap，以该提供一个non-member swap用来调用前者。对与classes（而非templates），也请特化std::swap。  
* 调用swap时应对std::swap使用using声明式，然后调用swap并且不带任何“命名空间资格修饰”。  
* 为“用户定义类型”进行std templates全特化是好的，但千万不要尝试在std内加入某些对std而言全新的东西。
    ```c++
    // swap典型实现
    namespace std
    {
        template<typename T>
        void swap(T& a, T& b)
        {
            t temp(a);
            a = b;
            b = temp;
        }
    }
    // 如果存在一个对象，实际上swap只需要交换两个内部指针就可以了，那么经典的就很复杂和浪费资源
    class Widget
    {
    public:
        Widget(const Widget& rhs);
        Widget& operator=(const Widget& rhs)
        {
            ...
            *pImpl = *(rhs.pImpl);
            ...
        }
        ...
    private:
        WidgetImpl* pImpl;
    }
    // 优化版本是新增一个swao的public成员函数
    class Widget
    {
    public:
        ...
        void swap(Widget& other)
        {
            // 指定使用std::swap避免和下面特化的冲突
            using std::swap;
            swap(pImpl, other.pImple);
        }
        ...
    private:
        WidgetImpl* pImpl;
    }
    // std重载版本
    namespace std
    {
        // std::swap的特化版本
        template<>
        void swap<Widget>(Widget& a, Widget& b)
        {
            a.swap(b);
        }
    }
    // 更牛逼的重载版本，但是不能定义在std空间，支持Widget的多态
    namespace WidgetStuff
    {
        // std::swap的特化版本
        template<typename T>
        void swap(Widget<T>& a, Widget<T>& b)
        {
            a.swap(b);
        }
    }
    ```  

理解：
* 深层原理有点复杂，遇到再研究下，总之对象的swap通常多一些思考，避免资源的浪费，按照这种写法来做优化即可。  

---

### 条款26：尽可能延后变量定义式的出现时间
请记住：  
* 尽可能延后变量定义式的出现。这样做可增加程序的清晰度并改善程序效率。  
    ```c++
    // 这个实现的问题在于如果提前抛出异常了，那么就浪费了encrypted构造和析构成本
    std::string encryptPassword(const std::string& password)
    {
        using namespace std;
        string encrypted;
        if (password.length() < MinimumPasswordLength)
        {
            throw logic_error("Password is too short");
        }
        
        encrypt(encrypted);

        return encrypted;
    }

    // 优化版本
    std::string encryptPassword(const std::string& password)
    {
        using namespace std;

        if (password.length() < MinimumPasswordLength)
        {
            throw logic_error("Password is too short");
        }
        
        // 直接用构造函数赋值可以避免先声明string encrypted再赋值的毫无意义的default构造过程
        string encrypted(password);
        encrypt(encrypted);

        return encrypted;
    }

    // 对于循环版本
    // 一个构造函数 + 一个析构函数 + n个赋值操作
    Widget w;
    for(int i = 0; i < n; i++)
    {
        w = 取决于i的某个值;
    }
    // n个构造函数 + n个析构函数
    for(int i = 0; i < n; i++)
    {
        Widget w(取决于i的某个值);
    }
    // 具体使用那个版本取决于赋值和构造哪个代价更大，一般还是用第二种
    ```

理解：  
* 之前定义局部变量的时候都是随便地方定义的，看样子要在不得不用的时候再定义。  

---

### 条款27：尽量少做转型动作
请记住：  
* 如果可以，尽量避免转型，特别是在注重效率的代码中避免dynamic_casts。如果有个设计需要转型动作，试着发展无需转换的替代设计。  
    ```c++
    class window
    {
    public:
        // 声明为virtual从而使得window对象的实例调用的是其衍生类的实现
        virtual void onResize() { ... }
        ...
    };
    class SpecialWindow: public Window 
    {
    public:
        // 衍生类想要先调用父类的该实现
        virtual void onResize() 
        {
            // 这种写法是错误的，因为这个时候onResize是作用在一个副本上的
            // static_cast<Window>(*this).onResize();
            Window::onResize();
        }
    }
    ```
* 如果转型是必要的，试着将它隐藏于某个函数背后。客户随后可以调用该函数，而不需要将转型放进他们自己的代码内。  
* 宁可使用c++-style（新式），不要使用旧式转型。前者很容易辨识出来，而且也比较有着分门别类的职掌。
  
理解：  
* 实际编码中尽可能的减少类型转换，避免不需要的坑以及这是一个比较耗时的操纵。  

---

### 条款28：避免返回handles指向对象内部成分
请记住：  
* 避免返回handles（包括references、指针、迭代器）指向对象内部。遵守这个条款可增加封装性，帮助const成员函数的行为像个const，并将发生“虚吊号码牌”的可能性降至最低。  
    ```c++
    class Point
    {
    public:
        Point(int x, int y);
        ...
        void setX(int newVal);
        void setY(int newVal);
        ...
    };

    struct RectDara
    {
        Point ulhc;
        Point lrhs;
    };

    class Rectangle
    {
        ...
    private:
        std::tr1::shared_ptr<RectData> pData;
    };

    class Rectangle
    {
    public:
        ...
        // 共有函数返回了私有成员变量的引用，这将导致pData被放松了封装性，因为可以通过指针对他进行操作了
        // Point& upperLeft() const { return pData->ulhc; }
        // Point& lowerRight() const { return pData->lrhc; }

        // 优化做法加const，使得返回对象只有读取权限
        const Point& upperLeft() const { return pData->ulhc; }
        const Point& lowerRight() const { return pData->lrhc; }
        ...
    };

    // 对于上面的放松了封装的阐释
    Point coord1(0, 0);
    Point coord2(100, 100);
    const Rectangle rec(coord1, coord2);
    // 修改了其私有变量属性
    rec.upperLeft().setX(50);

    // 其次如果这个私有变量开放出去了，当其他的地方拿到了这个指针但是和Rectangle生命周期不相关
    // 那么就会导致Rectangle生命周期结束后其他的引用就变成了悬空。
    ```

理解：  
* 原则就是尽可能不要public成员函数中返回私有变量的引用或指针。  

---

### 条款29：为异常安全而努力是值得的
请记住：  
* 异常安全函数即使发生异常也不会泄露资源或允许任何数据结构败坏。这样的函数区分为三种可能的保证：基本型、强烈型、不抛异常型。  
```c++
class PrettyMenu
{
public:
    ...
    void changeBackground(std::istream& imgSrc); // 改变背景图像
    ...
private:
    Mutex mutex; // 互斥器
    Image* bgImage; // 目前的背景图像
    int imageChanges; // 背景图像被改变的次数
}；

// 这个实现很糟糕
// 1. 资源泄露，当new Image异常时，unlock的调用就绝不会执行，互斥锁就永远锁住了
// 2. 数据败坏，当new Image异常时，bgImage指向一个已删除的对象
void PrettyMenu::changeBackground(std::istream& imgSrc)
{
    lock(&mutex); // 取得互斥器
    delete bgImage; // 摆脱旧的背景图像
    ++imageChanges; // 修改图像变更次数
    bgImage = new Image(imgSrc); // 安装新的背景图像
    unlock(&mutex); // 释放互斥器
}

// 进行以下优化
class PrettyMenu
{
...
private:
    ...
    std::tr1::shared_ptr<Image> bgImage;
    ...
}；

void PrettyMenu::changeBackground(std::istream& imgSrc)
{
    // 来自条款14，获得互斥锁的同时确保了结束后一定会释放掉
    Lock ml(&muitex); 
    // 智能指针的方法，new失败了之后bgImage会保持之前的状态
    // 一个函数执行失败后也应该让资源都处于之前的状态
    bgImage.reset(new Image(imgSrc));
    // 调换了顺序，如果失败了就不会加
    ++imageChanges;
}

// 还有一种更加优化的写法是所有的操作都在copy上，成功了之后再swap
// 这样正常做到了失败后保持所有资源的原始状态
```
* “强烈保证”往往能够以copy-and-swap实现出来，但“强烈保证”并非对所有函数都可实现或具备现实意义。  
* 函数提供的“异常安全保证”通常最高只等于其所调用之各个函数的“异常安全保证”中的最弱者。  

理解：  
* 这些都是编码的良好习惯，可以避免debug的时间  

---

### 条款30：透彻了解inlining的里里外外  
请记住：  
* 将大多数inlining限制在小型、被频繁调用的函数身上。这可使日后的调试过程和二进制升级更容易，也可使潜在的代码膨胀问题最小化，使程序的速度提升机会最大化。  
* 不要只因为function templates出现头文件，就将它们声明为inline。  

理解：  
* 包含inline函数头文件的库都得重编，所以对于移植性性不是很友好，正常换个动态库不用编译就升级了才是最佳体验。  
* inline函数是不能打断点得，所以无法调试。
* 总之将inlining限制在小型、被频繁调用的函数身上，其他情况就谨慎使用。  

---

### 条款31：将文件间的编译依存关系将至最低
请记住：  
* 支持“编译依存性最小化”的一般构想是：相依与申明式，不要相依于定义式。基于此构想的两个手段是Handle classes和Interface classes。  
* 程序库头文件应该以“完全且仅有声明式”的形式存在。这种做法不论是否涉及templates都适用。
    ```c++
    // 这样做的问题再与头文件任何一个改变都会导致每一个含入Person class的文件重新编译，这种依存关系就强了
    #include <string>
    #include "data.h"
    #include "address.h"

    class Person
    {
    public:
        Person(const std::string& name, const Dare& birthday, const Address& addr);
        std::string name() const;
        std::string birthDate() const;
        std::string address() const;
        ...
    private:
        std::string theName;
        Date theBirthDate;
        Address theAddress;
    }

    // 为了解耦这种依存性我们有两种写法
    // =========== Handle classes ============
    // Person.h 头文件定义
    #include <string>
    #include <memory>
    // 前置声明
    class PersonImpl;
    class Date;
    class Address;

    class Person
    {
    public:
        Person(const std::string& name, const Dare& birthday, const Address& addr);
        std::string name() const;
        std::string birthDate() const;
        std::string address() const;
        ...
    private:
        std::tr1::shared_ptr<PersonImpl> pImpl; // 指针指向实现物
    }

    // .cpp 函数实现
    #include "Person.h"
    #include "PersonImpl.h"
    Person::Person(const std::string& name, const Dare& birthday, const Address& addr)
    : pImpl(new PersonImpl(name, birthday, addr)){}
    std::string Person::name() const
    {
        return pImpl->name();
    }

    // =========== Interface classes ============
    // 写一个Person.h纯虚基类头文件
    // 前置声明
    class Date;
    class Address;

    class Person
    {
    public:
        virtual ~Person();
        virtual std::String name() const = 0;
        virtual std::string birthDate() const = 0;
        virtual std::string address() const = 0;
        ...
        static std::tr1::shared_ptr<Person> create(const std::string& name, const Date& birthday, const Address& addr);
        ...
    }

    // 衍生类的头文件RealPerson.h,然后cpp文件实现
    #include "Person.h"
    #include "data.h"
    #include "address.h"
    class RealPerson: public Person
    {
    public:
        RealPerson(const std::string& name, const Date& birthday, const Address& addr)
        : theNmae(name), thrBirthDate(birthday), theAddress(addr){}
        virtual ~RealPerson();
        std::string name() const;
        std::string birthDate() const() const;
        std::string address() const;
    private:
        std::string theName;
        Date theBirthDate;
        Address theAddress;
    };

    // Person的cpp实现
    #include "Person.h"
    #include "RealPerson.h"
    std::tr1::shared_ptr<Person> create(const std::string& name, const Date& birthday, const Address& addr)
    {
        return std::tr1::shared_ptr<Person>(new RealPerson(name, birthday, addr));
    }

    // 客户调用方式
    #include "Person.h
    std::string name;
    Date dateOfBirth;
    Address address;
    ...
    // 创建一个对象支持Person接口
    std::tr1::shared_ptr<Person> pp(Person::create(name, dateOfBirth, address));
    ...
    std::cout << pp->name()
            << " was born on "
            << pp->birthDate()
            << " and now lives at "
            << pp->address();
    ...
    ```  

理解：  
* 以上两种方式Handle classes和Interface classes均解除了接口和实现之间的耦合关系，用户包含的头文件基本都只包含声明而没有实现，这样满足了编译依存最小化的原则。

---

### 条款32：确定你的public继承塑模出is-a关系
请记住：  
* “public继承”意味is-a。适用于base classes身上的每一件事情一定适用于derived classes身上，因为每一个derived class对象也都是一个base class对象。  

理解：  
* 没有一个“适用于所有软件”的完美设计，用继承的方式可以做出一些根据当前情况的最佳设计，例如Student继承Person，表示Student is a Person，我们的设计也必须要满足这种关系。