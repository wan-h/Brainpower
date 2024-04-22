"""
https://www.langchain.com.cn/modules/prompts/output_parsers/examples/comma_separated

逗号分隔列表输出解析器
"""

from langchain.output_parsers import CommaSeparatedListOutputParser

model_output = "apple, banana, cherry"
output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
print(format_instructions)

# 相当于将逗号分隔的字符串输出为列表
output = output_parser.parse(model_output)
print(output)