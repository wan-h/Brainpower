// 将'click' 事件监听器添加到每个按钮元素上。 每个事件监听处理器都会调用到相关的 window.darkmode API 方法
// darkMode是在preload中声明的
document.getElementById('toggle-dark-mode').addEventListener('click', async () => {
    const isDarkMode = await window.darkMode.toggle()
    document.getElementById('theme-source').innerHTML = isDarkMode ? 'Dark' : 'Light'
})
  
  document.getElementById('reset-to-system').addEventListener('click', async () => {
    await window.darkMode.system()
    document.getElementById('theme-source').innerHTML = 'System'
})
  