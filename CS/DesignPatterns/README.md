## Design Patterns
设计模式的六大原则：  
* 开闭原则（Open Close Principle）
对扩展开放，对修改关闭。在程序需要进行拓展的时候，不能去修改原有的代码，实现一个热插拔的效果。
简言之，是为了使程序的扩展性好，易于维护和升级。想要达到这样的效果，我们需要使用接口和抽象类。
* 里氏代换原则（Liskov Substitution Principle）
任何基类可以出现的地方，子类一定可以出现。LSP 是继承复用的基石，只有当派生类可以替换掉基类，
且软件单位的功能不受到影响时，基类才能真正被复用，而派生类也能够在基类的基础上增加新的行为。
里氏代换原则是对开闭原则的补充。实现开闭原则的关键步骤就是抽象化，而基类与子类的继承关系就是
抽象化的具体实现，所以里氏代换原则是对实现抽象化的具体步骤的规范。
* 依赖倒转原则（Dependence Inversion Principle）
这个原则是开闭原则的基础，具体内容是针对接口编程，依赖于抽象而不依赖于具体。
* 接口隔离原则（Interface Segregation Principle）
使用多个隔离的接口，比使用单个接口要好。它还有另外一个意思是降低类之间的耦合度。
由此可见，其实设计模式就是从大型软件架构出发、便于升级和维护的软件设计思想，
它强调降低依赖，降低耦合。
* 迪米特法则，又称最少知道原则（Demeter Principle）
一个实体应当尽量少地与其他实体之间发生相互作用，使得系统功能模块相对独立。
* 合成复用原则（Composite Reuse Principle）
尽量使用合成/聚合的方式，而不是使用继承。
### 创建型模式
这些设计模式提供了一种在创建对象的同时隐藏创建逻辑的方式，而不是使用 new 运算符直接实例化对象。
这使得程序在判断针对某个给定实例需要创建哪些对象时更加灵活。  
其模式包含：  
[Abstract Factory Pattern](AbstractFactoryPattern/README.md)  
[Builder Pattern](BuilderPattern/README.md)  
[Prototype Pattern](PrototypePattern/README.md)  
[Simple Factory Pattern](SimpleFactoryPattern/README.md)  
[Singleton Pattern](SingletonPattern/README.md)
### 结构型模式
这些设计模式关注类和对象的组合。继承的概念被用来组合接口和定义组合对象获得新功能的方式。  
其模式包含：  
[Adapter Pattern](AdapterPattern/README.md)  
[Bridge Pattern](BridgePattern/README.md)  
[Composite Pattern](CompositePattern/README.md)  
[Decorator Pattern](DecoratorPattern/README.md)  
[Facade Pattern](FacadePattern/README.md)  
[Filter Pattern](FilterPattern/README.md)  
[Flyweight Pattern](FlyweightPattern/README.md)  
[Proxy Pattern](ProxyPattern/README.md)
### 行为型模式
这些设计模式特别关注对象之间的通信。  
其模式包含：  
[Command Pattern](CommandPattern/README.md)  
[Chain Of Responsibility Pattern](ChainOfResponsibilityPattern/README.md)  
[Interpreter Pattern](InterpreterPattern/README.md)  
[Iterator Pattern](IteratorPattern/README.md)  
[Mediator Pattern](MediatorPattern/README.md)  
[Memento Pattern](MementoPattern/README.md)  
[Null Object Pattern](NullObjectPattern/README.md)  
[Observer Pattern](ObserverPattern/README.md)  
[State Pattern](StatePattern/README.md)  
[Strategy Pattern](StrategyPattern/README.md)  
[Template Pattern](TemplatePattern/README.md)
### J2EE模式
这些设计模式特别关注表示层。这些模式是由 Sun Java Center 鉴定的。  
[Model View Controller Pattern](MVCPattern/README.md)