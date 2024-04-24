"""
https://www.langchain.com.cn/modules/memory/types/buffer_window

对话缓存窗口内存
"""

from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory( k=1)
memory.save_context({"input": "hi"}, {"ouput": "whats up"})
memory.save_context({"input": "not much you"}, {"ouput": "not much"})

# k=1 所有只会保存最后一条对话的上下文
print(memory.load_memory_variables({}))