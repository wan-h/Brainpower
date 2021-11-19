import { connect } from 'react-redux'
import { setVisibilityFilter } from '../actions'
import Link from '../components/Link'

// Footer中的filter属性在ownProps中，根据该属性更新state,将state映射到 Link UI 组件的参数（props）
// mapStateToProps会订阅 Store，每当state更新的时候，就会自动执行，重新计算 UI 组件的参数，从而触发 UI 组件的重新渲染
// mapStateToProps的第一个参数总是state对象，还可以使用第二个参数，代表容器组件的props对象
const mapStateToProps = (state, ownProps) => {
  return {
    active: ownProps.filter === state.visibilityFilter
  }
}

// onclick传到Footer中，绑定click后触发setVisibilityFilter action
// mapDispatchToProps是connect函数的第二个参数，用来建立 UI 组件的参数到store.dispatch方法的映射。也就是说，它定义了哪些用户的操作应该当作 Action，传给 Store
const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    onClick: () => {
      dispatch(setVisibilityFilter(ownProps.filter))
    }
  }
}

// 从UI组件生成容器组件
// mapStateToProps　输入逻辑：外部的数据（即state对象）如何转换为 UI 组件的参数
// mapDispatchToProps　输出逻辑：用户发出的动作如何变为 Action 对象，从 UI 组件传出去
const FilterLink = connect(
  mapStateToProps,
  mapDispatchToProps
)(Link)

export default FilterLink