"""
https://www.langchain.com.cn/modules/prompts/output_parsers/examples/retry

retry和output_fixing区别在于 
* output_fixing时已经输出了正确的结果但是格式不对，只使用大模型修正输出格式
* retry的输出就不完整，相当于加上额外信息后在做一次之前的大模型推理
"""

import json
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManagerForLLMRun
from pydantic import BaseModel, Field, validator
from typing import Any, List, Mapping, Optional
from langchain.output_parsers import RetryWithErrorOutputParser, PydanticOutputParser
 
 
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
            "action": "search",  
            "action_input": "who is leo di caprios gf?"
        }
        return json.dumps(data)


class Action(BaseModel):
    action: str = Field(description="action to take")
    action_input: str = Field(description="input to the action")

parser = PydanticOutputParser(pydantic_object=Action)
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=CustomLLM())
bad_response = '{"action": "search"}'
prompt_value = prompt.format_prompt(query="who is leo di caprios gf?")
print(retry_parser.get_format_instructions())
retry_parser.parse_with_prompt(bad_response, prompt_value)
  