"""
https://www.langchain.com.cn/modules/indexes/getting_started

pip install chromadb

通过文件回答问题包括四个步骤:
1. 创建索引
2. 从该索引创建检索器
3. 创建一个问题回答链
4. 问问题！
"""

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
loader = TextLoader('../state_of_the_union.txt', encoding='utf8')

############################# 创建一行索引 #############################
from langchain.indexes import VectorstoreIndexCreator
# 从 VectorstoreIndexCreator 返回的是 VectorStoreIndexWrapper，它提供了这些优秀的查询和 query_with_source 功能
index = VectorstoreIndexCreator().from_loaders([loader])
"""
Running Chroma using direct local API.
Using DuckDB in-memory for database. Data will be transient.
"""
query = "What did the president say about Ketanji Brown Jackson"
index.query(query)
"""
" The president said that Ketanji Brown Jackson is one of the nation's top legal minds, a former top litigator in private practice, a former federal public defender, and from a family of public school educators and police officers. He also said that she is a consensus builder and has received a broad range of support from the Fraternal Order of Police to former judges appointed by Democrats and Republicans."
"""
query = "What did the president say about Ketanji Brown Jackson"
index.query_with_sources(query)
"""
{'question': 'What did the president say about Ketanji Brown Jackson',
 'answer': " The president said that he nominated Circuit Court of Appeals Judge Ketanji Brown Jackson, one of the nation's top legal minds, to continue Justice Breyer's legacy of excellence, and that she has received a broad range of support from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.\n",
 'sources': '../state_of_the_union.txt'}
"""
############################# 演练 #############################
# VectorstoreIndexCreator内部做了哪些事情从而实现问题索引
"""
加载文件后有三个主要步骤:
1. 将文档分割成块
2. 为每个文档创建嵌入
3. 在向量库中存储文档和嵌入
"""
# 加载文档
documents = loader.load()
# 分割文档
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
# 创建嵌入
from langchain.vectorstores import Chroma
db = Chroma.from_documents(texts, embeddings)
"""
Running Chroma using direct local API.
Using DuckDB in-memory for database. Data will be transient.
"""
# 在一个检索接口中公开这个索引
retriever = db.as_retriever()
# 创建一个链，并使用它来回答问题
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
query = "What did the president say about Ketanji Brown Jackson"
qa.run(query)

"""
VectorstoreIndexCreator 只是所有这些逻辑的包装器。它可以在它使用的文本分割器、它使用的嵌入以及它使用的向量存储中进行配置
index_creator = VectorstoreIndexCreator(
    vectorstore_cls=Chroma, 
    embedding=OpenAIEmbeddings(),
    text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
)
"""