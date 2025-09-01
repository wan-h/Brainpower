import json
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters, types
from mcp.types import ListToolsResult
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.shared.context import RequestContext

from openai.types.chat.chat_completion import ChatCompletion
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

# 处理服务端发送的sampling请求，用于server和client交互（比如大模型的请求）
async def handle_sampling_message(
    context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
) -> types.CreateMessageResult:
    print(f"Sampling request: {params.messages}")
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )

# 处理服务端发送的elicitation请求，用于server和client交互（比如需要用户确认或则提供额外信息的操作）
async def handle_elicitation_message(
    context: RequestContext[ClientSession, None], params: types.ElicitRequestParams
) -> types.ElicitResult:
    print(f"Elicitation request: {params.model_dump()}")
    return types.ElicitResult(
        action="accept",
        content={
            "checkAlternative": True
        }
    )

# 用服务端获取roots权限的请求（限制服务端操作范围）
async def handle_list_roots_message(
    context: RequestContext[ClientSession, None]
) -> types.ListRootsResult:
    return types.ListRootsResult(
        roots=[
            types.Root(
                uri="file:///Users/willw/Desktop/test1.png"
            ),
            types.Root(
                uri="file:///Users/willw/Desktop/test2.png"
            )
        ]
    )

# 处理服务发送的日志信息
async def handle_logging_message(params: types.LoggingMessageNotificationParams):
    print(f"Logging message: {params.model_dump()}")

# async def handle_message(message: types.ServerNotification):
#     print(f"Received message: {message.model_dump()}")

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai = AsyncOpenAI(
            base_url='http://litellm.prod.zyaidc.local/v1',
            api_key='sk-AGhIknipIS6-mYjKQoQttQ'
        )
    
    # async def connect_to_file_server(self):
    #     server_params = StdioServerParameters(
    #         command="npx",
    #         args=[
    #             "-y",
    #             "@modelcontextprotocol/server-filesystem",
    #             "/Users/willw/WORKSPACE/CODE/LIT/mcp-for-beginners/practice"
    #         ],
    #         env=None
    #     )
        
    #     stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
    #     self.stdio, self.write = stdio_transport
    #     self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
    #     await self.session.initialize()
        
    #     # List available tools
    #     response = await self.session.list_tools()
    #     tools = response.tools
    #     print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(
            self.stdio, 
            self.write,
            sampling_callback=handle_sampling_message,
            list_roots_callback=handle_list_roots_message,
            elicitation_callback=handle_elicitation_message,
            logging_callback=handle_logging_message,
            # message_handler=handle_message,
        ))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("=" * 20)
        print("\nConnected to server with tools:", [tool.name for tool in tools])
        print("\nConnected to server with resources:")
        print(await self.session.list_resource_templates())
        print(await self.session.read_resource("file://documents/hello"))
        print(await self.session.list_resources())
        print(await self.session.read_resource("config://settings"))
        print("=" * 20)

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        system_prompt = await self.session.get_prompt(name='assistant', arguments={"name": "will"})
        system_prompt = system_prompt.messages[0].content.text

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]
        resp: ListToolsResult = await self.session.list_tools()
        available_tools = [{ 
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        } for tool in resp.tools]

        while True:
            # Initial API call
            response: ChatCompletion = await self.openai.chat.completions.create(
                model='Qwen3-30B-A3B-Thinking-2507',
                messages=messages,
                stream=False,
                tools=available_tools
            )
            # Process response and handle tool calls
            message = response.choices[0].message
            tool_use = False
            if message.content:
                messages.append({
                    "role": "assistant",
                    "content": message.content
                })
            if message.tool_calls:
                tool_use = True
                tool_name = message.tool_calls[0].function.name
                tool_args = json.loads(message.tool_calls[0].function.arguments)
                async def progress_callback(progress: float, total: float | None, message: str | None):
                    print("progress_callback: progress: {}, total: {}, message: {}".format(progress, total, message))
                result = await self.session.call_tool(tool_name, tool_args, progress_callback=progress_callback)
                print(f"Called tool {tool_name} with args {tool_args}, result: {result}")
                messages.extend([
                    {
                        "role": "assistant", 
                        "content": f"Calling tool {tool_name} with args {tool_args}"
                    },
                    {
                        "role": "tool", 
                        "content": result.content
                    }
                ])

            if not tool_use:
                return "\n".join([str(message['content']) for message in messages])

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())