"""
用于测试的虚假LLM类。这使您可以模拟对LLM的调用，并模拟LLM以特定方式响应时会发生什么
"""

from langchain.llms.fake import FakeListLLM
from langchain.agents import load_tools, initialize_agent, AgentType, create_react_agent
from langchain.agents import Tool
from langchain_community.utilities import PythonREPL

python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="一个Python shell。使用它来执行python命令。输入应该是一个有效的python命令。如果你想看到一个值的输出，你应该用`print(...)`打印出来。",
    func=python_repl.run,
)

tools = [repl_tool]

responses = [
    "Action: python_repl\nAction Input: print(2 + 2)",
    "Final Answer: 4"
]
llm = FakeListLLM(responses=responses)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("whats 2 + 2")