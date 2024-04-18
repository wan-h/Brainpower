from langchain.prompts.example_selector.base import BaseExampleSelector
from typing import List, Dict
import numpy as np

class CustomExampleSelector(BaseExampleSelector):
    def __init__(self, examples: List[Dict[str, str]], **kwargs):
        self.examples = examples
    
    def add_example(self, example: Dict[str, str]) -> None:
        """Add new example to store for a key."""
        self.examples.append(example)
    
    def select_examples(self, input_variables: Dict[str, str]) -> List[Dict]:
        """Select which examples to use based on the inputs."""
        return np.random.choice(self.examples, size=2, replace=False)

examples = [
    {"foo": "1"},
    {"foo": "2"},
    {"foo": "3"}
]

# Initialize example selector.
example_selector = CustomExampleSelector(examples)

# Select examples
print("============> Select examples")
print(example_selector.examples)
print(example_selector.select_examples({"foo": "foo"}))

# Add new example to the set of examples
example_selector.add_example({"foo": "4"})
print("============> Add examples")
print(example_selector.examples)
print(example_selector.select_examples({"foo": "foo"}))