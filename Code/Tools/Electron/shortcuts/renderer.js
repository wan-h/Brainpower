// 渲染器进程监听键盘按键事件
function handleKeyPress(event){
    document.getElementById("last-keypress").innerText = event.key
    console.log(`You Pressed ${event.key}`)
}

window.addEventListener('keyup', handleKeyPress, true)