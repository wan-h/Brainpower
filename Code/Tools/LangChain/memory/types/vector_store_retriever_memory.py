"""
https://www.langchain.com.cn/modules/memory/types/vectorstore_retriever_memory

基于向量存储的记忆

VectorStoreRetrieverMemory将记忆存储在VectorDB中，并在每次调用时查询最重要的K个文档。
与大多数其他记忆类不同的是，它不明确跟踪交互的顺序。
在这种情况下，“文档”是先前的对话片段。这可以用来提到AI在对话中早期被告知的相关信息
"""


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory
 
 
############################ 初始化 VectorStore ############################
import faiss
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
 
embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
index = faiss.IndexFlatL2(embedding_size)
embedding_fn = OpenAIEmbeddings().embed_query
vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})

############################ 创建 VectorStoreRetrieverMemory ############################

# In actual usage, you would set `k` to be a higher value, but we use k=1 to show that
# the vector lookup still returns the semantically relevant information
retriever = vectorstore.as_retriever(search_kwargs=dict(k=1))
memory = VectorStoreRetrieverMemory(retriever=retriever)
 
# When added to an agent, the memory object can save pertinent information from conversations or used tools
memory.save_context({"input": "My favorite food is pizza"}, {"output": "thats good to know"})
memory.save_context({"input": "My favorite sport is soccer"}, {"output": "..."})
memory.save_context({"input": "I don't the Celtics"}, {"output": "ok"}) # 
 
# Notice the first result returned is the memory pertaining to tax help, which the language model deems more semantically relevant
# to a 1099 than the other documents, despite them both containing numbers.
print(memory.load_memory_variables({"prompt": "what sport should i watch?"})["history"])
 
"""
input: My favorite sport is soccer
output: ...
"""