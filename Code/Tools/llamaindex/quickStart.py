from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 配置模型
print("Loading model...")
import openai
openai.api_key = "sk-XXX"
Settings.llm = OpenAI(temperature=0.2, model="gpt-4")
# 加载数据
print("Loading data...")
documents = SimpleDirectoryReader("data").load_data(show_progress=True)
# 构建搜索引擎
print("Building search engine...")
index = VectorStoreIndex.from_documents(documents, show_progress=True)
query_engine = index.as_query_engine()
# 搜索
print("Searching...")
response = query_engine.query(
    "投资的原则是什么？",
)
print(response)