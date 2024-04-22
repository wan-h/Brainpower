"""
https://www.langchain.com.cn/modules/prompts/output_parsers/getting_started

"""

import json
from pydantic import BaseModel, Field, validator
from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.callbacks.manager import CallbackManagerForLLMRun

class CustomLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        data = {  
            "setup": "Why did the chicken cross the playground?",  
            "punchline": "To get to the other slide!"  
        }
        return json.dumps(data)


model = CustomLLM()

# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")
 
    # You can add custom validation logic easily with Pydantic.
    @validator('setup')
    def question_ends_with_question_mark(cls, info):
        if info[-1] != '?':
            raise ValueError("Badly formed question!")
        return info

# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Joke)

print("======================= parser =============================")
print(parser.get_format_instructions())
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
print("======================= prompt =============================")
# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."
_input = prompt.format_prompt(query=joke_query)
print(_input.to_string())

print("======================= model output =============================")
# 这里就相当于直接解析成了Joke格式
output = model(_input.to_string())
output = parser.parse(output)
print(output)