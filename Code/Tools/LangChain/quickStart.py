# -*- coding: utf-8 -*-
# @Author  : wanhui

"""
https://python.langchain.com/docs/get_started/quickstart#prompt-templates

pip install langchain
pip install openai
"""

"""
LLM / Chat Model
"""
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

llm = OpenAI()
chat_model = ChatOpenAI()

from langchain.schema import HumanMessage

text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]

# print(llm.invoke(text))
# print(chat_model.invoke(messages))

"""
Prompt templates
"""
# 提示词模板
from langchain.prompts import PromptTemplate
prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
# print(prompt.format(product="colorful socks"))

# 聊天提示词模板
from langchain.prompts.chat import ChatPromptTemplate
template = "You are a helpful assistant that translates {input_language} to {output_language}."
human_template = "{text}"
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])
# print(chat_prompt.format_prompt(input_language="English", output_language="French", text="I love programming."))

"""
Output parsers
"""
from langchain.schema import BaseOutputParser
class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""
    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")
# print(CommaSeparatedListOutputParser().parse("hi, bye"))

"""
Composing with LCEL
"""
template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more."""
human_template = "{text}"
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])
chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()
# print(chain.invoke({"text": "colors"}))