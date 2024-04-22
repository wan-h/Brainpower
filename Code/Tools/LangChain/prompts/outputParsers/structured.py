"""
https://www.langchain.com.cn/modules/prompts/output_parsers/examples/structured

json格式的解析
"""

import json
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

print("=================== output_parser instructions =======================")
response_schemas = [
    ResponseSchema(name="answer", description="answer to the user's question"),
    ResponseSchema(name="source", description="source used to answer the user's question, should be a website.")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
print(output_parser.get_format_instructions())

print("=================== prompt =======================")
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="answer the users question as best as possible.\n{format_instructions}\n{question}",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions}
)
print(prompt.format(question="What is the capital of France?"))


print("=================== output =======================")
output = {'answer': 'Paris', 'source': 'https://en.wikipedia.org/wiki/Paris'}
print(output_parser.parse(json.dumps(output)))