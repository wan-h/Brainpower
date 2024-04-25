from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


############################# fake llm & fake embedding #############################



# 加载数据
loader = TextLoader('C:\\code\\wanhui\\Brainpower\\Code\\Tools\\LlamaIndex\\data\\财富自由之路1.txt', encoding='utf8')
docs = loader.load()
text_splitter = CharacterTextSplitter(separator="\n", is_separator_regex=True, chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(splits)