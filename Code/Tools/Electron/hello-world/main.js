// 控制应用生命周期和创建原生浏览器窗口的模组
// app控制应用程序生命周期
// BrowserWindow创建和管理应用程序窗口
const { app, BrowserWindow } = require('electron')
const path = require('path')

function createWindow () {
    // 创建浏览器窗口
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    // 加载index.html
    mainWindow.loadFile('index.html')
}

// Electron结束初始化和创建浏览器窗口时候调用
// 部分API在ready事件触发之后才能使用
app.whenReady().then(() => {
    createWindow()

    app.on('activate', function(){
        // 通常macOS上，当点击dock中的应用程序图标时，如果没有其他打开的窗口，那么程序会创建一个窗口
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

// 除了macOS外，其他操作系统当所有的窗口都被关闭的时候退出程序
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
})



// 打包程应用程序
// 1. 将 Electron Forge 添加到您应用的开发依赖中
// npm install --save-dev @electron-forge/cli
// npx electron-forge import
// 2. 使用 Forge 的 make 命令来创建可分发的应用程序
// npm run make