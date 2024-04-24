"""
https://www.langchain.com.cn/modules/agents/tools/custom_tools

"""

from langchain.tools import BaseTool

from typing import Type
 
class CustomSearchTool(BaseTool):
    name = "搜索"
    description = "当你需要回答有关当前事件的问题时有用"
 
    def _run(self, query: str) -> str:
        """使用工具。"""
        return "query result"
    
    async def _arun(self, query: str) -> str:
        """异步使用工具。"""
        raise NotImplementedError("BingSearchRun不支持异步")