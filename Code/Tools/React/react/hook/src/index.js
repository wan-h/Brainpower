import React, { useState, useEffect, useContext, useReducer, useRef } from "react"
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from "react-router-dom"

function Home() {
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

// useContext
const themes = {
    light: {
      foreground: "#000000",
      background: "#eeeeee"
    },
    dark: {
      foreground: "#ffffff",
      background: "#222222"
    }
};
const ThemeContext = React.createContext(themes.light);
function ThemedButton() {
    // 当组件上层最近的 <MyContext.Provider> 更新时，该 Hook 会触发重渲染，并使用最新传递给 MyContext provider 的 context value 值
    const theme = useContext(ThemeContext);
    return (
        <button style={{ background: theme.background, color: theme.foreground }}>
            I am styled by theme context!
        </button>
    )
}
function Toolbar(props) {
    return (
        <div>
            <ThemedButton />
        </div>
    )
}

// useReducer
const initialState = {count: 0};
function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return {count: state.count + 1};
        case 'decrement':
            return {count: state.count - 1};
        default:
            throw new Error();
    }
}
function Counter() {
    // 更新state重点的数值
    const [state, dispatch] = useReducer(reducer, initialState);
    return (
        <div>
          Count: {state.count}
          <button onClick={() => dispatch({type: 'decrement'})}>-</button>
          <button onClick={() => dispatch({type: 'increment'})}>+</button>
        </div>
      );
}


// useRef
// https://zh-hans.reactjs.org/docs/refs-and-the-dom.html
function TextInputWithFocusButton() {
    const inputE1 = useRef(null);
    const onButtonClick = () => {
        // `current` 指向已挂载到 DOM 上的文本输入元素
        inputE1.current.focus();
    };
    return (
        <div>
            <input ref={inputE1} type="text" />
            <button onClick={onButtonClick}>Focus the input</button>
        </div>
    )
}



// Router
function App() {
    return (
        <div className="App">
          <h1>React Hook Example!</h1>
          <Routes>
            {/* useState useEffect */}
            <Route path="/" element={<Home />} />
            {/* useContext */}
            <Route path="toolbar" element={
                <ThemeContext.Provider value={themes.dark}>
                    <Toolbar />
                </ThemeContext.Provider>
            } />
            {/* usePreducer */}
            <Route path="counter" element={<Counter />} />
            {/* useRef */}
            <Route path="textInputWithFocusButton" element={<TextInputWithFocusButton />} />
          </Routes>
        </div>
    );
}

ReactDOM.render(
    <BrowserRouter>
        <App />
    </BrowserRouter>,
    document.getElementById('root')
);