import _ from 'loadsh';
import printMe from './print.js';
import './style.css';
import Icon from './icon.png';
import Data from './data.xml';
import Notes from './data.csv';
import yaml from './data.yaml'

console.log(yaml.title)

function component() {
    const element = document.createElement('div');
    const btn = document.createElement('button');
    // lodash 在当前 script 中使用 import 引入
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
    element.classList.add('hello');
    
    btn.innerHTML = 'Click me and check the console!';
    btn.onclick = printMe;
    element.appendChild(btn);

    // 将图片添加到我们已经存在的div中
    const myIcon = new Image();
    myIcon.src = Icon;
    element.appendChild(myIcon);

    console.log(Data);
    console.log(Notes);

    return element;

}

document.body.appendChild(component());