const { app, BrowserWindow, Menu, MenuItem, globalShortcut } = require('electron')

function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600
    })

    win.loadFile('index.html')
    // 拦截主进程事件，调度页面中的keydown和keyup事件之前，会发出before-input-event事件
    // 拦截后渲染将无法接收到事件
    win.webContents.on('before-input-event', (event, input) => {
        if (input.control && input.key.toLowerCase() === 'i') {
            console.log('Pressed Control + I')
            // 阻止事件关联默认动作
            event.preventDefault()
        }
    })
}

const menu = new Menu()
menu.append(new MenuItem({
    label: 'Electron',
    submenu: [{
        role: 'help',
        // 添加本地快捷键
        accelerator: process.platform === 'darwin' ? 'Alt+Cmd+I' : 'Alt+Shift+I',
        click: () => {console.log('Electron rocks!')}
    }]
}))

Menu.setApplicationMenu(menu)

app.whenReady().then(() => {
    // 全局快捷键，监听键盘输入(只要键盘有此输入)
    globalShortcut.register('Alt+CommandOrControl+J', () => {
        console.log('Electron loves global shortcuts!')
    })
}).then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})