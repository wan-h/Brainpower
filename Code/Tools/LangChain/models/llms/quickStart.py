"""
https://www.langchain.com.cn/modules/models/llms/getting_started

"""

from langchain.llms import OpenAI
 
llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)

llm("Tell me a joke")
"""
'  Why did the chicken cross the road?  To get to the other side.'
"""


# generate：更广泛地说，您可以使用输入列表调用它，获取比仅文本更完整的响应
llm_result = llm.generate(["Tell me a joke", "Tell me a poem"]*15)
# len(llm_result.generations) = 30
llm_result.generations[0]
"""
[Generation(text='  Why did the chicken cross the road?  To get to the other side!'),
 Generation(text='  Why did the chicken cross the road?  To get to the other side.')]
"""

# 还可以访问返回的特定于提供程序的信息
llm_result.llm_output
"""
{'token_usage': {'completion_tokens': 3903,
  'total_tokens': 4023,
  'prompt_tokens': 120}}
 
"""

# 还可以估计模型中一段文本将有多少个标记。这很有用，因为模型具有上下文长度（并且对于更多标记的成本更高)，这意味着您需要注意传递的文本的长度
llm.get_num_tokens("what a joke")
"""
3
"""