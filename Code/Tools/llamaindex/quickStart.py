import os
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.embeddings import resolve_embed_model

# 使用测试模式
os.environ["IS_TESTING"] = "True"

# Load data and build an index
documents = SimpleDirectoryReader('C:\\code\\wanhui\\Brainpower\\Code\\Tools\\LlamaIndex\\data').load_data()
index = VectorStoreIndex.from_documents(
    documents,
)

# Query your data
query_engine = index.as_query_engine()
response = query_engine.query("投资理念是什么?")
print(response)