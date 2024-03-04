"""
安装 pip install tokenizers
"""

from transformers import AutoTokenizer

# 这里会去hub下载
# tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")

# 测试下载到本地(这里将模型中关于Tokenizer几个必要的文件下载下来就可以了)
tokenizer = AutoTokenizer.from_pretrained("c:\\Users\\willw\\Downloads")
input = "Hello, y'all! How are you 😁 ?"
print("============input============")
print(input)
print("============output============")
output = tokenizer(input)
print(output)
print("============subwords============")
print(tokenizer.convert_ids_to_tokens(output.input_ids))
print("============encode============")
print(tokenizer.encode(input))
print("============decode============")
print(tokenizer.decode(output.input_ids))
