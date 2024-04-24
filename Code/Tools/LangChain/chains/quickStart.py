"""
https://www.langchain.com.cn/modules/chains/getting_started

"""

################# 快速开始: 使用LLMChain #################
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
 
llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
 
# Run the chain only specifying the input variable.
print(chain.run("colorful socks"))

################# 类创建自定义链Chain类 #################
"""
LangChain 提供了很多现成的链接，但是有时候您可能想要为您的特定用例创建一个自定义链接。对于此示例，我们将创建一个自定义链，用于连接2个 LLMChains 的输出。
为了创建自定义链:
1. 首先从 Chain 类的子类化开始,
2. 填写 input_key 和 output_key 属性,
3. 添加显示如何执行链的 _call 方法。
"""
from langchain.chains import LLMChain
from langchain.chains.base import Chain
 
from typing import Dict, List
 
 
class ConcatenateChain(Chain):
    chain_1: LLMChain
    chain_2: LLMChain
 
    @property
    def input_keys(self) -> List[str]:
        # Union of the input keys of the two chains.
        all_input_vars = set(self.chain_1.input_keys).union(set(self.chain_2.input_keys))
        return list(all_input_vars)
 
    @property
    def output_keys(self) -> List[str]:
        return ['concat_output']
 
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        output_1 = self.chain_1.run(inputs)
        output_2 = self.chain_2.run(inputs)
        return {'concat_output': output_1 + output_2}

prompt_1 = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)
chain_1 = LLMChain(llm=llm, prompt=prompt_1)
 
prompt_2 = PromptTemplate(
    input_variables=["product"],
    template="What is a good slogan for a company that makes {product}?",
)
chain_2 = LLMChain(llm=llm, prompt=prompt_2)
 
concat_chain = ConcatenateChain(chain_1=chain_1, chain_2=chain_2)
concat_output = concat_chain.run("colorful socks")
print(f"Concatenated output:\n{concat_output}")

"""
Concatenated output:



Socktastic Colors.
 
"Put Some Color in Your Step!"

"""