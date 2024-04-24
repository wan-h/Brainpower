"""
https://www.langchain.com.cn/modules/memory/examples/multiple_memory

多重内存

在同一链中使用多个内存类。要组合多个内存类，我们可以初始化CombinedMemory类，然后使用它
"""

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, CombinedMemory, ConversationSummaryMemory
 
conv_memory = ConversationBufferMemory(
    memory_key="chat_history_lines",
    input_key="input"
)
 
summary_memory = ConversationSummaryMemory(llm=OpenAI(), memory_key="history", input_key="input")
# Combined
memory = CombinedMemory(memories=[conv_memory, summary_memory])
_DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
 
Summary of conversation:
{history}
Current conversation:
{chat_history_lines}
Human: {input}
AI:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"], template=_DEFAULT_TEMPLATE
)
llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=memory,
    prompt=PROMPT
)

conversation.run("Hi!")
conversation.run("Can you tell me a joke?")

"""
> Entering new ConversationChain chain...
Prompt after formatting:
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
 
Summary of conversation:
 
The human greets the AI and the AI responds, asking how it can help.
Current conversation:
 
Human: Hi!
AI: Hi there! How can I help you?
Human: Can you tell me a joke?
AI:
 
> Finished chain.
 
"""