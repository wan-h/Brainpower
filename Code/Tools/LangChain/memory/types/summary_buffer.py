"""
https://www.langchain.com.cn/modules/memory/types/summary_buffer

对话摘要缓存内存

本质上是summay + token buffer的结合
它将最近的交互记录缓存在内存中，但不仅仅是完全清除旧的交互，而是将它们编译成一份摘要并同时使用。不过，与之前的实现不同，它使用令牌长度而不是交互数量来确定何时清除交互。
"""

from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.memory import ConversationSummaryBufferMemory

class CustomLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("CustomLLM does not support stop arguments.")
        return "Hello"


llm = CustomLLM()
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=10)
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})

print(memory.load_memory_variables({"input": 'who is sam'}))

"""
{'history': 'System: \nThe human says "hi", and the AI responds with "whats up".\nHuman: not much you\nAI: not much'}
"""

# 可以直接利用predict_new_summary方法
messages = memory.chat_memory.messages
previous_summary = ""
memory.predict_new_summary(messages, previous_summary)

"""
'\nThe human and AI state that they are not doing much.'
"""