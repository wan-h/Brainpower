"""
https://www.langchain.com.cn/modules/memory/types/entity_summary_memory

实体记忆
"""

from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.memory import ConversationEntityMemory

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

memory = ConversationEntityMemory(llm=llm)
_input = {"input": "Deven & Sam are working on a hackathon project"}
memory.load_memory_variables(_input)
# 这里相当于就用大模型取解析了 entities 是什么以及他的描述
memory.save_context(
    _input,
    {"ouput": " That sounds like a great project! What kind of project are they working on?"}
)
print(memory.load_memory_variables({"input": 'who is Sam'}))

 