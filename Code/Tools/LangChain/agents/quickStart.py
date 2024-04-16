import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

"""
pip install google-search-results
pip install numexpr
"""

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "44a6af98d6f5ec973d737767979193de4cf9c564d006aca6911d5ef39a021195"

# 加载语言模型
llm = OpenAI(temperature=0)

# 加载工具
tools = load_tools(["llm-math"], llm=llm)

# 初始化agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 测试一下
agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

"""
> Entering new AgentExecutor chain...
 I need to find out who Leo DiCaprio's girlfriend is and then calculate her age raised to the 0.43 power.
Action: Search
Action Input: "Leo DiCaprio girlfriend"
Observation: Camila Morrone
Thought: I need to find out Camila Morrone's age
Action: Search
Action Input: "Camila Morrone age"
Observation: 25 years
Thought: I need to calculate 25 raised to the 0.43 power
Action: Calculator
Action Input: 25^0.43
Observation: Answer: 3.991298452658078
 
Thought: I now know the final answer
Final Answer: Camila Morrone is Leo DiCaprio's girlfriend and her current age raised to the 0.43 power is 3.991298452658078.
 
> Finished chain.
"""