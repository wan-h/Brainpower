#include<iostream>
using namespace std;

class Shape {
    protected:
        int width, height;
    public:
        Shape( int a = 0, int b = 0){
            width = a;
            height = b;
        }
        virtual int area(){
            cout << "Parent class area" << endl;
            return 0;
        }
        // 纯虚函数， 派生类必须实现
        virtual int perimeter() = 0;
};

class Rectangle: public Shape {
    public:
        // 子构造函数调用父构造函数
        Rectangle( int a = 0, int b = 0): Shape(a, b) { }
        int area(){
            cout << "Rectangle class area" << endl;
            return (width * height);
        }
        int perimeter(){
            return 0;
        }
};

class Triangle: public Shape{
    public:
        Triangle( int a = 0, int b = 0): Shape(a, b) { }
        int area() {
            cout << "Triangle class area" << endl;
            return (width * height / 2);
        }
        int perimeter(){
            return 0;
        }
};

int main(){
    Shape* shape;
    Rectangle rec(10, 7);
    Triangle tri(10, 5);

    // 存储矩形的地址
    shape = &rec;
    shape -> area();

    shape = &tri;
    shape -> area();

    return 0;
}