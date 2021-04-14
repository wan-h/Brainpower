#include <iostream>

using namespace std;

class Box {
    public:
        double length; // 长度
        double breadth; // 宽度
        double height; // 高度
};

class Shape {
    public:
        void setWidth(int w) {
            width = w;
        }

        void setHeight(int h) {
            height = h;
        }
    // protected成员可以被派生类对象访问，不能被用户代码（类外）访问。
    protected:
        int width;
        int height;
};

// 派生类
// 公有继承（public）：当一个类派生自公有基类时，基类的公有成员也是派生类的公有成员，基类的保护成员也是派生类的保护成员，基类的私有成员不能直接被派生类访问，但是可以通过调用基类的公有和保护成员来访问。
// 保护继承（protected）： 当一个类派生自保护基类时，基类的公有和保护成员将成为派生类的保护成员。
// 私有继承（private）：当一个类派生自私有基类时，基类的公有和保护成员将成为派生类的私有成员
class Rectangle: public Shape {
    public:
        int getArea() {
            return (width * height);
        }
};

int main() {
    Box Box1; // 声明 Box1，类型为 Box
    Box Box2; // 声明 Box2，类型为 Box
    double volume = 0.0; // 用于存储体积
    
    // box1详述
    Box1.height = 5.0;
    Box1.length = 6.0;
    Box1.breadth = 7.0;

    // box2详述
    Box2.height = 10.0;
    Box2.length = 12.0;
    Box2.breadth = 13.0;

    // box1体积
    volume = Box1.height * Box1.length * Box1.breadth;
    cout << "Box1 的体积: " << volume << endl;

    // box2体积
    volume = Box2.height * Box2.length * Box2.breadth;
    cout << "Box2 的体积: " << volume << endl;


    Rectangle Rect;

    Rect.setWidth(5);
    Rect.setHeight(7);

    // 输出对象面积
    cout << "Total area: " << Rect.getArea() << endl;

    return 0;
}