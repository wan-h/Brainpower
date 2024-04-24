"""
https://www.langchain.com.cn/modules/memory/types/kg

对话知识图谱记忆

这种类型的记忆使用知识图谱来重建记忆
"""

from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.memory import ConversationKGMemory

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
memory = ConversationKGMemory(llm=llm)
memory.save_context({"input": "say hi to sam"}, {"ouput": "who is sam"})
memory.save_context({"input": "sam is a friend"}, {"ouput": "okay"})

print(memory.load_memory_variables({"input": 'who is sam'}))