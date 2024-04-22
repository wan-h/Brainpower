"""
https://www.langchain.com.cn/modules/prompts/output_parsers/getting_started

"""

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
        return "Why did the chicken cross the road?To get to the other side!"


llm = CustomLLM()

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
print(parser.get_format_instructions())
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
print(prompt.format(query="Why did the chicken cross the road?"))