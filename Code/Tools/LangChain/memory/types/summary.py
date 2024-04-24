"""
https://www.langchain.com.cn/modules/memory/types/summary

对话摘要记忆

这种记忆类型可以创建关于对话的摘要，有助于从对话中概括信息
这种应该也是解决上下文限制的问题，可以将历史对话做归纳来降低token数量
"""

from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.memory import ConversationSummaryMemory

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
memory = ConversationSummaryMemory(llm=llm)
memory.save_context({"input": "say hi to sam"}, {"ouput": "who is sam"})
memory.save_context({"input": "sam is a friend"}, {"ouput": "okay"})

print(memory.load_memory_variables({"input": 'who is sam'}))