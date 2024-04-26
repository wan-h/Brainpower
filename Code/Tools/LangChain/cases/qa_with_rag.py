from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms.fake import FakeListLLM
from langchain.embeddings.fake import FakeEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate

############################# fake llm & fake embedding #############################

responses = [
    "Hello, Hah!"
]
llm = FakeListLLM(responses=responses)
embeddings = FakeEmbeddings(size=512)


############################# 加载数据 #############################
print("=" * 100)
loader = TextLoader('C:\\code\\wanhui\\Brainpower\\Code\\Tools\\LlamaIndex\\data\\财富自由之路3.txt', encoding='utf8')
docs = loader.load()
print("page_content: \n", len(docs[0].page_content))

############################# 切分数据 #############################
print("=" * 100)
# 这里相当于将chunk_size设置为每100个字符切分一次，其中切分的判断标志就是"\n"
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=100, chunk_overlap=20)
# 这里将docs拆分成了多个chunks
splits = text_splitter.split_documents(docs)
print("chunks size: \n", len(splits))
print("content size: \n", len(splits[0].page_content))
print("page metadatas: \n", splits[-1].metadata)
# print("splits: \n", splits)

############################# 构造向量检索器 #############################
print("=" * 100)
"""
这里的内部流程是：
1. 将每个chunk的内容向量化(embedding)
2. 将这些向量化后的数据存储到vector database (or vector store)
3. 需要检索的时候将search query同样向量化后从数据存储中匹配similarity最相近的向量表达
"""
# 这里的vector database使用Chroma
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
print(vectorstore)

############################# 检索 #############################
print("=" * 100)
# 这里就是构造了一个相似度检索器，返回top-k = 3
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
retrieved_docs = retriever.invoke("财务状况有哪三个阶段？")
print("retrieved_docs size: \n", len(retrieved_docs))
print("retrieved_docs content: \n", retrieved_docs[0].page_content)

############################# 构造rag chain #############################
print("=" * 100)
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
"""

prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=template,
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 管道操作符
# 上一个输出就是下一个的输入
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print(rag_chain.invoke("What is Task Decomposition?"))

# cleanup
vectorstore.delete_collection()