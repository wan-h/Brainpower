"""
https://www.langchain.com.cn/modules/prompts/example_selectors/examples/mmr
最大边际相关性示例选择器
MaxMarginalRelevanceExampleSelector根据示例与输入之间的相似性以及多样性进行选择。
它通过找到与输入具有最大余弦相似度的嵌入示例，并在迭代中添加它们，同时对已选择示例的接近程度进行惩罚来实现这一目标。
"""

from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector, SemanticSimilarityExampleSelector
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
 
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)
 
# These are a lot of examples of a pretend task of creating antonyms.
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]
 

example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples, 
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(), 
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    FAISS, 
    # This is the number of examples to produce.
    k=2
)
mmr_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective}\nOutput:", 
    input_variables=["adjective"],
)
 
# Input is a feeling, so should select the happy/sad example as the first one
print("=" * 100)
print("MaxMarginalRelevanceExampleSelector =>")
print(mmr_prompt.format(adjective="worried"))


# 仅基于相似性的情况进行比较
example_selector = SemanticSimilarityExampleSelector.from_examples(
    # 可供选择的示例列表。
    examples,
    # 用于生成嵌入并用于测量语义相似性的嵌入类。
    OpenAIEmbeddings(),
    # 用于存储嵌入并进行相似性搜索的VectorStore类。
    FAISS,
    # 要生成的示例数量。
    k=2,
)
similar_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective}\nOutput:", 
    input_variables=["adjective"],
)
similar_prompt.example_selector.k = 2
print("=" * 100)
print("SemanticSimilarityExampleSelector =>")
print(similar_prompt.format(adjective="worried"))
 