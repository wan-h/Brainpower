import React from 'react';
import ReactDOM from 'react-dom';

function formatName(user) {
    return user.firstName + ' ' + user.lastName;
}

const user = {
    firstName: 'Harper',
    lastName: 'Perez'
};

// 元素渲染，条件渲染
function getGreeting(user) {
    if (user) {
        return <h1>Hello, {formatName(user)}</h1>;
    }
    return <h1>Hello, Stranger.</h1>;
}

// 组合组件
function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
}

// State & 生命周期

// 使用类替换上面function的写法,在组件内部实现了定时器
class Clock2 extends React.Component {
    constructor(props) {
        super(props);
        this.state = {date: new Date()};
    }
    // 生命周期：第一次被渲染时
    componentDidMount() {
        // 设置定时器，1000ms刷新一次页面
        this.timerID = setInterval(
            () => this.tick(),
            1000
        )
    }
    // 生命周期：组件删除时
    componentWillUnmount() {
        // 清除计时器
        clearInterval(this.timerID);
    }

    tick() {
        // this.state.date = new Date(); 此代码不会重新渲染组件，使用this.setState才会重新渲染组件
        this.setState({
            date: new Date()
        });
    }

    render() {
        return (
            <div>
                <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
            </div>
        );
    }
}

function WarningBanner(props) {
    // 组件不做任何渲染
    if (!props.warn) {
        return null;
    }

    return (
        <div className="warning">
            Warning!
        </div>
    );
}

// 事件处理
class Toggle extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isToggleOn: true,
            showWarning: true
        };

        // 为了在回调中使用 `this`，这个绑定是必不可少的
        this.handleClick1 = this.handleClick1.bind(this);
    }

    handleClick1() {
        this.setState({
            isToggleOn: !this.state.isToggleOn
        });
    }
    handleClick2() {
        this.setState({
            showWarning: !this.state.showWarning
        });
    }

    render() {
        return (
            <div>
                <button onClick={this.handleClick1}>
                    {this.state.isToggleOn ? 'ON': 'OFF'}
                </button>
                <WarningBanner warn={this.state.showWarning} />
                {/* 不用在构造函数中绑定this的写法 */}
                <button onClick={() => this.handleClick2()}>
                    {this.state.showWarning ? 'Hide' : 'Show'}
                </button>
            </div>
        )
    }
}

// 列表 & Key
function NumberList(props) {
    const numbers = props.numbers;
    const listItems = numbers.map((number) => 
        // 一个元素的 key 最好是这个元素在列表中拥有的一个独一无二的字符串
        // key={index} 在没有唯一标志时可以用index
        <li key={number.toString()}>
            {number}
        </li>
    );
    return (
        <ul>{listItems}</ul>
    );
}

// 表单
class NameForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: 'grapefruit'};
    
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    handleChange(event) {
        this.setState({value: event.target.value});
    }
    
    handleSubmit(event) {
        alert('提交的名字: ' + this.state.value);
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    名字:
                    {/* <input value={this.state.value} onChange={this.handleChange} /> */}
                    {/* 下拉列表 */}
                    <select value={this.state.value} onChange={this.handleChange}>
                        <option value="grapefruit">葡萄柚</option>
                        <option value="lime">酸橙</option>
                        <option value="coconut">椰子</option>
                        <option value="mango">芒果</option>
                    </select>
                </label>
                <input type="submit" value="提交" />
            </form>
        );
    }
}

// 状态提升
const scaleNames = {
    c: 'Celsius',
    f: 'Fahrenheit'
};
function BoilingVerdict(props) {
    if (props.celsius >= 100) {
      return <p>The water would boil.</p>;
    }
    return <p>The water would not boil.</p>;
}
function toCelsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}
function toFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}
function tryConvert(temperature, convert) {
    const input = parseFloat(temperature);
    if (Number.isNaN(input)) {
      return '';
    }
    const output = convert(input);
    const rounded = Math.round(output * 1000) / 1000;
    return rounded.toString();
}

class TemperatureInput extends React.Component {
    constructor(props) {
      super(props);
      this.handleChange = this.handleChange.bind(this);
    }
  
    handleChange(e) {
      this.props.onTemperatureChange(e.target.value);
    }
  
    render() {
      const temperature = this.props.temperature;
      const scale = this.props.scale;
      return (
        <fieldset>
          <legend>Enter temperature in {scaleNames[scale]}:</legend>
          <input value={temperature}
                 onChange={this.handleChange} />
        </fieldset>
      );
    }
}
class Calculator extends React.Component {
    constructor(props) {
      super(props);
      this.handleCelsiusChange = this.handleCelsiusChange.bind(this);
      this.handleFahrenheitChange = this.handleFahrenheitChange.bind(this);
      this.state = {temperature: '', scale: 'c'};
    }
  
    handleCelsiusChange(temperature) {
      this.setState({scale: 'c', temperature});
    }
  
    handleFahrenheitChange(temperature) {
      this.setState({scale: 'f', temperature});
    }
  
    render() {
      const scale = this.state.scale;
      const temperature = this.state.temperature;
      const celsius = scale === 'f' ? tryConvert(temperature, toCelsius) : temperature;
      const fahrenheit = scale === 'c' ? tryConvert(temperature, toFahrenheit) : temperature;
  
      return (
        <div>
          <TemperatureInput
            scale="c"
            temperature={celsius}
            onTemperatureChange={this.handleCelsiusChange} />
          <TemperatureInput
            scale="f"
            temperature={fahrenheit}
            onTemperatureChange={this.handleFahrenheitChange} />
          <BoilingVerdict
            celsius={parseFloat(celsius)} />
        </div>
      );
    }
  }

function App() {
    return (
        <div>
            {getGreeting(user)}
            {getGreeting()}
            {/* && 运算符，前面为true才显示后面的expression,可以作为判断的快速写法 */}
            {false && getGreeting()}
            <Welcome name="Sara" />
            <Welcome name="Cahal" />
            <Welcome name="Edite" />
            <Clock2 />
            <Toggle />
            <NumberList numbers={[1, 2, 3, 4, 5]} />
            <NameForm />
            <Calculator />
        </div>
    )
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);


// 初始化项目
// npx create-react-app quick-start