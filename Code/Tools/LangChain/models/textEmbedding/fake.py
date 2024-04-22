"""
https://www.langchain.com.cn/modules/models/text_embedding/examples/fake

作为一些实验验证使用
"""

from langchain.embeddings import FakeEmbeddings
 
embeddings = FakeEmbeddings(size=1352)
 

query_result = embeddings.embed_query("foo")
print(len(query_result))
doc_results = embeddings.embed_documents(["foo"])
print(len(doc_results), len(doc_results[0]))