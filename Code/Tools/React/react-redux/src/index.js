import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore } from 'redux'
import todoApp from './reducers'
import App from './components/App'

let store = createStore(todoApp)

// subscribe() 返回一个函数用来注销监听器
// 每次 state 更新时，打印日志
const unsubscribe = store.subscribe(() =>
  console.log(store.getState())
)

// Provider在根组件外面包了一层，这样一来，App的所有子组件就默认都可以拿到store中的state了(容器组件中用到了store中的state)
// react components通过context可以获取到store
// const { store } = this.context;
render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
)

// 停止监听 state 更新
// unsubscribe()