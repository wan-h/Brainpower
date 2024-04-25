from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms.fake import FakeListLLM
from langchain.embeddings.fake import FakeEmbeddings

############################# fake llm & fake embedding #############################

responses = [
    "Action: python_repl\nAction Input: print(2 + 2)",
    "Final Answer: 4"
]
llm = FakeListLLM(responses=responses)
embeddings = FakeEmbeddings(size=512)


############################# 加载数据 #############################
print("=" * 100)
print("loading data...")
loader = TextLoader('C:\\code\\wanhui\\Brainpower\\Code\\Tools\\LlamaIndex\\data\\财富自由之路1.txt', encoding='utf8')
docs = loader.load()
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(splits)