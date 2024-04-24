"""
https://www.langchain.com.cn/modules/memory/types/token_buffer

token缓冲区

在内存中保留最近的对话内容，并使用token长度而不是对话数量来决定何时刷新对话
"""

from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.memory import ConversationTokenBufferMemory

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
memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=10)
memory.save_context({"input": "hi"}, {"ouput": "whats up"})
memory.save_context({"input": "not much you"}, {"ouput": "not much"})

print(memory.load_memory_variables({}))
# 这里由于长度限制就只取了最后一次的内容
"""
{'history': 'Human: not much you\nAI: not much'}
"""