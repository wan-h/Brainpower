"""
https://www.langchain.com.cn/modules/memory/examples/agent_with_memory

"""

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper
 
search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )
]

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"
 
{chat_history}
Question: {input}
{agent_scratchpad}"""
 
prompt = ZeroShotAgent.create_prompt(
    tools, 
    prefix=prefix, 
    suffix=suffix, 
    input_variables=["input", "chat_history", "agent_scratchpad"]
)

# 这里和LLMChain使用的方式是一致的，本质就是替换agent提示中的chat_history占位符
memory = ConversationBufferMemory(memory_key="chat_history")


llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

agent_chain.run(input="How many people live in canada?")

"""
> Entering new AgentExecutor chain...
Thought: I need to find out the population of Canada
Action: Search
Action Input: Population of Canada
Observation: The current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data. · Canada ... Additional information related to Canadian population trends can be found on Statistics Canada's Population and Demography Portal. Population of Canada (real- ... Index to the latest information from the Census of Population. This survey conducted by Statistics Canada provides a statistical portrait of Canada and its ... 14 records ... Estimated number of persons by quarter of a year and by year, Canada, provinces and territories. The 2021 Canadian census counted a total population of 36,991,981, an increase of around 5.2 percent over the 2016 figure. ... Between 1990 and 2008, the ... ( 2 ) Census reports and other statistical publications from national statistical offices, ( 3 ) Eurostat: Demographic Statistics, ( 4 ) United Nations ... Canada is a country in North America. Its ten provinces and three territories extend from ... Population. • Q4 2022 estimate. 39,292,355 (37th). Information is available for the total Indigenous population and each of the three ... The term 'Aboriginal' or 'Indigenous' used on the Statistics Canada ... Jun 14, 2022 ... Determinants of health are the broad range of personal, social, economic and environmental factors that determine individual and population ... COVID-19 vaccination coverage across Canada by demographics and key populations. Updated every Friday at 12:00 PM Eastern Time.
Thought: I now know the final answer
Final Answer: The current population of Canada is 38,566,192 as of Saturday, December 31, 2022, based on Worldometer elaboration of the latest United Nations data.
> Finished AgentExecutor chain.
"""