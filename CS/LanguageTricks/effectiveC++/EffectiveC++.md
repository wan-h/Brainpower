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