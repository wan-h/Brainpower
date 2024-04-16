from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re

import os
os.environ["SERPAPI_API_KEY"] = "44a6af98d6f5ec973d737767979193de4cf9c564d006aca6911d5ef39a021195"
os.environ["OPENAI_API_KEY"] = "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"
 
## 设置工具
# 创建一个合适的工具（搜索)和99个不相关的工具

# Define which tools the agent can use to answer user queries
search = SerpAPIWrapper()
search_tool = Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )
def fake_func(inp: str) -> str:
    return "foo"
fake_tools = [
    Tool(
        name=f"foo-{i}", 
        func=fake_func, 
        description=f"a silly function that you can use to get more information about the number {i}"
    ) 
    for i in range(99)
]
ALL_TOOLS = [search_tool] + fake_tools


## 工具检索器(tool-retriever)
# 我们将使用向量存储来为每个工具描述创建嵌入。
# 然后，对于传入的查询，我们可以为该查询创建嵌入，并进行相关工具的相似性搜索。 
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
 
docs = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(ALL_TOOLS)]
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
retriever = vector_store.as_retriever()
 
def get_tools(query):
    docs = retriever.get_relevant_documents(query)
    return [ALL_TOOLS[d.metadata["index"]] for d in docs]

# 可以测试这个检索器，看看它是否有效。
get_tools("whats the weather?")