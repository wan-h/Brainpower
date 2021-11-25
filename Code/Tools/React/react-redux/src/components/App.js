import React from 'react'
import Footer from './Footer'
import AddTodo from '../containers/AddTodo'
import VisibleTodoList from '../containers/VisibleTodoList'

// UI 组件，只负责 UI 的呈现，不带有任何业务逻辑
// 容器组件，负责管理数据和业务逻辑，不负责 UI 的呈现

// APP下都是容器组件，容器组件中定义了UI和容器之间的关系

const App = () => (
  <div>
    <AddTodo />
    <VisibleTodoList />
    <Footer />
  </div>
)

export default App