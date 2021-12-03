import React, { useState, useEffect } from "react"
import ReactDOM from 'react-dom';

function App() {
    // 声明一个叫 “count” 的 state 变量，初始值为0
    // useState 会返回一对值：当前状态和一个让你更新它的函数
    const [count, setCount] = useState(0);

    // 相当于 componentDidMount 和 componentDidUpdate
    useEffect (() => {
        // 使用浏览器的 API 更新页面标题
        document.title = `You clicked ${count} times`;
    })

    return (
        <div>
            <p>You clicked {count} times</p>
            <button onClick={() => setCount(count + 1)}>
                Click me
            </button>
        </div>
    )
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);