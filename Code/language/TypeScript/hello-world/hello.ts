alert('hello world in TypeScript!');

// 通过类型批注提供静态类型以在编译时启动类型检查
// 基础类型批注：number, bool, string，没有类型给出时TS编译器使用类型推断．没有类型可以推断时默认为any类型
function Add(left: number, right: number): number {
    return left + right;
}

// 实例
function area1(shape: string, width: number, height: number) {
    var area = width * height;
    return "I'm a " + shape + " with an area of " + area + " cm squared.";
}

document.body.innerHTML = area1("rectangle", 30, 15);

// 接口
interface Shape1 {
    name: string;
    width: number;
    height: number;
    // 保留
    color?: string;
}

function area2(shape: Shape1) {
    var area = shape.width * shape.height;
    return "I'm a " + shape.name + " with an area of " + area + " cm squared.";
}

console.log(area2({name: "rectangle", width: 30, height: 15}));
console.log(area2({name: "square", width: 30, height: 30, color: "blue"}))

// 箭头函数表达式
// lambda表达式 ()=>{something}或()=>something 相当于js中的函数,它的好处是可以自动将函数中的this附加到上下文中
var shape = {
    name: "rectangle",
    popup: function() {
        console.log('This inside popup(): ' + this.name);

        setTimeout( () => {
            console.log('This inside setTimeout(): ' + this.name);
            console.log("I'm a " + this.name + "!");
        }, 3000)
    }
};
shape.popup();

// 类
class Shape2 {
    name: string;
    area: number;
    // 私有成员，只有类函数可以访问
    private color: string;
    // 构造函数
    constructor (name: string, width: number, height: number) {
        this.name = name;
        this.area = width * height;
        this.color = "pink";
    };

    shoutout() {
        return "I'm " + this.color + " " + this.name +  " with an area of " + this.area + " cm squared.";
    }
}

var square = new Shape2("square", 30, 30);
console.log(square.shoutout());
console.log( 'Area of Shape: ' + square.area );
console.log( 'Name of Shape: ' + square.name );
// 私有不可访问，此操作有编译器限制，在编译后的js上没有任何体现
// console.log( 'Color of Shape: ' + square.color );

// 继承
class Shape3D extends Shape2 {
    volume: number;
    constructor ( public name: string, width: number, height: number, length: number ) {
        super( name, width, height );
        this.volume = length * this.area;
    };
    
    shoutout() {
        return "I'm " + this.name +  " with a volume of " + this.volume + " cm cube.";
    }

    superShout() {
        return super.shoutout();
    }
}

var cube = new Shape3D("cube", 30, 30, 30);
console.log( cube.shoutout() );
console.log( cube.superShout() );


// ts编译执行：
// tsc hello.ts
// 编译后为hello.js