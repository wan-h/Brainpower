# coding: utf-8
# Author: wanhui0729@gmail.com

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get('/')
async def get():
    return HTMLResponse(html)

# 创建一个websocket
# ws://localhost:8000/ws
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 握手链接
    await websocket.accept()
    while True:
        # 长连接通信
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# 如果启动出现警告WARNING:  Unsupported upgrade request.
# 重装uvicorn
# pip uninstall uvicorn
# pip install uvicorn[standard]
if __name__ == '__main__':
    uvicorn.run(app)