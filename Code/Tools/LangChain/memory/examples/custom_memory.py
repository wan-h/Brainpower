"""
https://www.langchain.com.cn/modules/memory/examples/custom_memory

# !pip install spacy
# !python -m spacy download en_core_web_lg
 
"""

from langchain import OpenAI, ConversationChain
from langchain.schema import BaseMemory
from pydantic import BaseModel
from typing import List, Dict, Any

# 将编写一个自定义内存类，该类使用spacy提取实体并将有关它们的信息保存在简单的哈希表中。
# 然后，在对话期间，我们将查看输入文本，提取任何实体，并将有关它们的任何信息放入上下文中

import spacy
nlp = spacy.load('en_core_web_lg')

class SpacyEntityMemory(BaseMemory, BaseModel):
    """Memory class for storing information about entities."""
 
    # Define dictionary to store information about entities.
    entities: dict = {}
    # Define key to pass information about entities into prompt.
    memory_key: str = "entities"
 
    def clear(self):
        self.entities = {}
 
    @property
    def memory_variables(self) -> List[str]:
        """Define the variables we are providing to the prompt."""
        return [self.memory_key]
 
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Load the memory variables, in this case the entity key."""
        # Get the input text and run through spacy
        doc = nlp(inputs[list(inputs.keys())[0]])
        # Extract known information about entities, if they exist.
        entities = [self.entities[str(ent)] for ent in doc.ents if str(ent) in self.entities]
        # Return combined information about entities to put into context.
        return {self.memory_key: "\n".join(entities)}
 
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        # Get the input text and run through spacy
        text = inputs[list(inputs.keys())[0]]
        doc = nlp(text)
        # For each entity that was mentioned, save this information to the dictionary.
        for ent in doc.ents:
            ent_str = str(ent)
            if ent_str in self.entities:
                self.entities[ent_str] += f"\n{text}"
            else:
                self.entities[ent_str] = text

# 定义一个提示，以输入有关实体的信息以及用户输入
from langchain.prompts.prompt import PromptTemplate
 
template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. You are provided with information about entities the Human mentions, if relevant.
 
Relevant entity information:
{entities}
 
Conversation:
Human: {input}
AI:"""
prompt = PromptTemplate(
    input_variables=["entities", "input"], template=template
)

llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, prompt=prompt, verbose=True, memory=SpacyEntityMemory())

conversation.predict(input="Harrison likes machine learning")

"""
> Entering new ConversationChain chain...
Prompt after formatting:
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know. You are provided with information about entities the Human mentions, if relevant.
 
Relevant entity information:
 
Conversation:
Human: Harrison likes machine learning
AI:
 
> Finished ConversationChain chain.

"""