"""
https://www.langchain.com.cn/modules/memory/examples/adding_memory

"""

from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate

# 重要的步骤是正确设置提示。在下面的提示中，我们有两个输入键：一个用于实际输入，另一个用于来自Memory类的输入。
# 重要的是，确保PromptTemplate和ConversationBufferMemory中的键匹配(chat_history)。

template = """You are a chatbot having a conversation with a human.
 
{chat_history}
Human: {human_input}
Chatbot:"""
 
prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], 
    template=template
)

# 这里指定的key和prompt中的input_variables的key是一致的，这样就会将memory插入到每次的对话中
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=OpenAI(), 
    prompt=prompt, 
    verbose=True, 
    memory=memory,
)

llm_chain.predict(human_input="Hi there my friend")

"""
> Entering new LLMChain chain...
Prompt after formatting:
You are a chatbot having a conversation with a human.
 
Human: Hi there my friend
Chatbot:
 
> Finished LLMChain chain.
"""