from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain_community import OpenAI, SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re

import os
os.environ["SERPAPI_API_KEY"] = "44a6af98d6f5ec973d737767979193de4cf9c564d006aca6911d5ef39a021195"
os.environ["OPENAI_API_KEY"] = "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"
 
## ============================ 设置工具 =============================
# 创建一个合适的工具（搜索)和99个不相关的工具

# Define which tools the agent can use to answer user queries
# search = SerpAPIWrapper()
# search_tool = Tool(
#         name = "Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events"
#     )
def fake_func(inp: str) -> str:
    return "foo"
fake_tools = [
    Tool(
        name=f"foo-{i}", 
        func=fake_func, 
        description=f"a silly function that you can use to get more information about the number {i}"
    ) 
    for i in range(99)
]
ALL_TOOLS = fake_tools


## ============================ 工具检索器(tool-retriever) ============================
# 我们将使用向量存储来为每个工具描述创建嵌入。
# 然后，对于传入的查询，我们可以为该查询创建嵌入，并进行相关工具的相似性搜索。 
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
 
docs = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(ALL_TOOLS)]
vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
retriever = vector_store.as_retriever()
 
def get_tools(query):
    docs = retriever.get_relevant_documents(query)
    return [ALL_TOOLS[d.metadata["index"]] for d in docs]

# 可以测试这个检索器，看看它是否有效。
get_tools("whats the weather?")

## ============================ 提示模板 ============================
# Set up the base template
template = """Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:
 
{tools}
 
Use the following format:
 
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
 
Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s
 
Question: {input}
{agent_scratchpad}"""
 
# 自定义提示模板
from typing import Callable
# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    ############## NEW ######################
    # The list of tools available
    tools_getter: Callable
 
    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        ############## NEW ######################
        tools = self.tools_getter(kwargs["input"])
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
        return self.template.format(**kwargs)
prompt = CustomPromptTemplate(
    template=template,
    tools_getter=get_tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps"]
)

## ============================ 输出解析器 (Output Parser) ============================
class CustomOutputParser(AgentOutputParser):
 
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
output_parser = CustomOutputParser()

## ============================ 设置LLM，停止序列和代理 ============================
llm = OpenAI(temperature=0)
# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)
tools = get_tools("whats the weather?")
tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)

## ============================ 使用代理（Use the Agent）============================
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
agent_executor.run("What's the weather in SF?")
