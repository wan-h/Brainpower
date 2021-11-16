const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron')
const path = require('path')

// 将应用注册为“electron-fiddle://”协议的处理器
if (process.defaultApp) {
    if (process.argv.length > 2) {
        app.setAsDefaultProtocolClient('electron-fiddle', process.execPath, [path.resolve(process.argv[1])])
    }
} else {
    app.setAsDefaultProtocolClient('electron-fiddle')
}

const createWindow = () => {
    // 创建浏览器窗口
    mainWindow = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        preload: path.join(__dirname, 'preload.js')
      }
    })
  
    mainWindow.loadFile('index.html')
}

// Windows 中需要特别处理在同一个 Electron 实例中打开的协议的内容
if (process.platform === 'win') {
    const gotTheLock = app.requestSingleInstanceLock()
    if (!gotTheLock) {
        app.quit()
    } else {
        app.on('second-instance', (event, commandLine, workingDirectory) => {
            // 用户正在尝试运行第二个实例，我们需要让焦点指向我们的窗口
            if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore()
            mainWindow.focus()
            }
        })
    }
}

// Create mainWindow, load the rest of the app, etc...
app.whenReady().then(() => {
    createWindow()
})

// 处理协议，在本例中，我们选择显示一个错误提示对话框。
app.on('open-url', (event, url) => {
    dialog.showErrorBox('欢迎回来', `导向自: ${url}`)
})

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit()
  })
  
// Handle window controls via IPC
ipcMain.on('shell:open', () => {
    const pageDirectory = __dirname.replace('app.asar', 'app.asar.unpacked')
    const pagePath = path.join('file://', pageDirectory, 'index.html')
    // 使用系统默认程序(浏览器)打开链接
    shell.openExternal(pagePath)
})

// 打包程应用程序
// 1. 将 Electron Forge 添加到您应用的开发依赖中
// npm install --save-dev @electron-forge/cli
// npx electron-forge import
// 2. 使用 Forge 的 make 命令来创建可分发的应用程序
// npm run make