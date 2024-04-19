"""
https://www.langchain.com.cn/modules/prompts/chat_prompt_template
"""

from langchain.prompts import (
    ChatPromptTemplate, 
    PromptTemplate, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    AIMessagePromptTemplate,
    ChatMessagePromptTemplate,
    MessagesPlaceholder
)

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Template本质上就是一个字符串模板，包含了预设信息，保留占位信息，供后续填充。
system_template = "You are a helpful assistant that translates {input_language} to {output_language}"
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

print("=" * 100)
prompt = PromptTemplate(
    template="You are a helpful assistant that translates {input_language} to {output_language}",
    input_variables=["input_language", "output_language"],
)
system_message_prompt_2 = SystemMessagePromptTemplate(prompt=prompt)

# 这两个对象是等价的，这里的 == 使用 dict()来判断的
assert system_message_prompt == system_message_prompt_2
print("system_message_prompt =>")
print(system_message_prompt)

print("=" * 100)

# 这里的 ChatPromptTemplate 更像是把多个PromptTemplate组合在一起，可以理解为一个容器
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
# get a chat completion from the formatted messages
output = chat_prompt.format_prompt(
    input_language="English", 
    output_language="French",
    text="I love programming"
)
print("chat_prompt to_messages =>")
print(output.to_messages())

print("=" * 100)
# 输出的格式 Format output
output_1 = chat_prompt.format(
    input_language="English", 
    output_language="French",
    text="I love programming"
)
print("chat_prompt format =>")
print(output_1)

# 等价实现
output_2 = chat_prompt.format_prompt(
    input_language="English", 
    output_language="French",
    text="I love programming"
).to_string()
assert output_1 == output_2


print("=" * 100)
# 消息模板最常用的是 AIMessagePromptTemplate、SystemMessagePromptTemplate 和 HumanMessagePromptTemplate，分别用于创建 AI 消息、系统消息和人类消息
# 在聊天模型支持使用任意角色发送聊天消息的情况下,可以使用 ChatMessagePromptTemplate，允许用户指定角色名称
prompt = "May the {subject} be with you"
chat_message_prompt = ChatMessagePromptTemplate.from_template(template=prompt, role="Jedi")
chat_message_prompt.format(subject="force")
print("ChatMessagePromptTemplate =>")
print(chat_message_prompt)


print("=" * 100)
# 该占位符可以在格式化期间完全控制要呈现的消息。不确定应该使用哪个消息提示模板的角色或者希望在格式化期间插入消息列表时，使用该占位符
human_prompt = "Summarize our conversation so far in {word_count} words."
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)
chat_prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name="conversation"), human_message_template])
human_message = HumanMessage(content="What is the best way to learn programming?")
ai_message = AIMessage(content="""\
1. Choose a programming language: Decide on a programming language that you want to learn. 
 
2. Start with the basics: Familiarize yourself with the basic programming concepts such as variables, data types and control structures.
 
3. Practice, practice, practice: The best way to learn programming is through hands-on experience\
""")
result = chat_prompt.format_prompt(conversation=[human_message, ai_message], word_count="10").to_messages()
print("MessagesPlaceholder =>")
print(result)