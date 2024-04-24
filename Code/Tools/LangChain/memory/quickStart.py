"""
https://www.langchain.com.cn/modules/memory/getting_started

内存涉及在用户与语言模型的交互过程中始终保持状态的概念。
用户与语言模型的交互被捕获在聊天消息的概念中，所以这归结为从一系列聊天消息中摄取、捕获、转换和提取知识。有许多不同的方法可以实现这一点，每种方法都作为自己的内存类型存在。
一般来说，对于每种类型的记忆，有两种方法来理解使用记忆。这些是从消息序列中提取信息的独立函数，还有一种方法可以在链中使用这种类型的内存。
内存可以返回多条信息(例如，最近的 N 条消息和所有以前消息的摘要)。返回的信息可以是字符串，也可以是消息列表。
"""

############################## 聊天记录 ##############################
print("=" * 100)
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message("hi!")
history.add_ai_message("whats up?")
print(history.messages)

############################## 缓存记忆 ##############################
# ConversationBufferMemory 只是 ChatMessageHistory 的一个包装器，用于提取变量中的消息
print("=" * 100)
from langchain.memory import ConversationBufferMemory
 
memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("hi!")
memory.chat_memory.add_ai_message("whats up?")
print(memory.load_memory_variables({}))

# 获取作为消息列表的历史记录
memory = ConversationBufferMemory(return_messages=True)
memory.chat_memory.add_user_message("hi!")
memory.chat_memory.add_ai_message("whats up?")
print(memory.load_memory_variables({}))


############################## chain中的使用 ##############################
print("=" * 100)
from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chains import ConversationChain

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
conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory(), verbose=True)
conversation.predict(input="Hi there!")
conversation.predict(input="I'm doing well! Just having a conversation with an AI.")
conversation.predict(input="Tell me about yourself.")
# 历史信息都记录到了memory中
print(conversation.memory.load_memory_variables({}))

############################## 保存邮件历史记录 ##############################
print("=" * 100)
# 如果经常需要保存消息，然后加载它们再次使用。通过首先将消息转换为普通的 python 字典，保存它们(作为 json 或其他形式) ，然后加载它们，可以很容易地做到这一点
import json
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
 
history = ChatMessageHistory()
history.add_user_message("hi!")
history.add_ai_message("whats up?")

dicts = messages_to_dict(history.messages)
print(dicts)

new_messages = messages_from_dict(dicts)
print(new_messages)