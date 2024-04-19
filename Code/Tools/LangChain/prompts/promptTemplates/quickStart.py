"""
https://www.langchain.com.cn/modules/prompts/prompt_templates/getting_started
提示模板是生成提示的可重复方法。它包含一个文本字符串（“模板”)，该字符串可以从最终用户那里接收一组参数并生成提示。
提示模板可能包含：
* 对语言模型的指导
* 一组少量示例，以帮助语言模型生成更好的响应
* 对语言模型的提问
"""

########################################## 什么是提示模板 ##########################################
print("=" * 100)
from langchain.prompts import PromptTemplate
 
template = """
I want you to act as a naming consultant for new companies.
What is a good name for a company that makes {product}?
"""
 
prompt = PromptTemplate(
    input_variables=["product"],
    template=template,
)
print(prompt.format(product="colorful socks"))
# -> I want you to act as a naming consultant for new companies.
# -> What is a good name for a company that makes colorful socks?

########################################## 创建提示模板 ##########################################
print("=" * 100)
 
# An example prompt with no input variables
no_input_prompt = PromptTemplate(input_variables=[], template="Tell me a joke.")
print(no_input_prompt.format())
# -> "Tell me a joke."
 
# An example prompt with one input variable
one_input_prompt = PromptTemplate(input_variables=["adjective"], template="Tell me a {adjective} joke.")
print(one_input_prompt.format(adjective="funny"))
# -> "Tell me a funny joke."
 
# An example prompt with multiple input variables
multiple_input_prompt = PromptTemplate(
    input_variables=["adjective", "content"], 
    template="Tell me a {adjective} joke about {content}."
)
print(multiple_input_prompt.format(adjective="funny", content="chickens"))
# -> "Tell me a funny joke about chickens."

# 如果您不想手动指定input_variables，您也可以使用from_template类方法创建PromptTemplate。 langchain将根据传递的template自动推断input_variables
template = "Tell me a {adjective} joke about {content}."
 
prompt_template = PromptTemplate.from_template(template)
prompt_template.input_variables
# -> ['adjective', 'content']
print(prompt_template.format(adjective="funny", content="chickens"))
# -> Tell me a funny joke about chickens.
 
########################################## 序列化提示模板 ##########################################
print("=" * 100)
# langchain会自动通过文件扩展名推断文件格式。当前，langchain支持将模板保存为YAML和JSON文件
prompt_template.save("awesome_prompt.json") # Save to JSON filem，这里存储的是序列化的信息
from langchain.prompts import load_prompt
loaded_prompt = load_prompt("awesome_prompt.json")
 
assert prompt_template == loaded_prompt
print(prompt_template.format(adjective="funny", content="chickens"))

########################################## 将少量示例传递给提示模板 ##########################################
"""
few shot examples 是一组示例，可用于帮助语言模型生成更好的响应。
要使用 few shot examples 生成提示，可以使用 FewShotPromptTemplate。
这个类接受一个 PromptTemplate 和一个 few shot examples 列表。然后，它将用 few shot examples 格式化提示模板。
"""
print("=" * 100)
from langchain.prompts import FewShotPromptTemplate
# First, create the list of few shot examples.
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
]
# Next, we specify the template to format the examples we have provided.
# We use the `PromptTemplate` class for this.
example_formatter_template = """\
Word: {word}
Antonym: {antonym}
"""
example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template=example_formatter_template,
)

# Finally, we create the `FewShotPromptTemplate` object.
few_shot_prompt = FewShotPromptTemplate(
    # These are the examples we want to insert into the prompt.
    examples=examples,
    # This is how we want to format the examples when we insert them into the prompt.
    example_prompt=example_prompt,
    # The prefix is some text that goes before the examples in the prompt.
    # Usually, this consists of intructions.
    prefix="Give the antonym of every input",
    # The suffix is some text that goes after the examples in the prompt.
    # Usually, this is where the user input will go
    suffix="Word: {input}\nAntonym:",
    # The input variables are the variables that the overall prompt expects.
    input_variables=["input"],
    # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
    example_separator="\n",
)
 
# We can now generate a prompt using the `format` method.
print(few_shot_prompt.format(input="big"))


########################################## 选择提示模板的示例 ##########################################
"""
如果有大量的示例，可以使用 ExampleSelector 来选择一组最具信息量的示例，以帮助语言模型生成更好的响应。这将帮助生成更可能生成良好响应的提示。

下面的示例中使用基于输入长度选择示例的 LengthBasedExampleSelector。当你担心构建的提示会超过上下文窗口的长度时，这很有用。
对于较长的输入，它将选择较少的示例进行包含，而对于较短的输入，它将选择更多的示例
"""
print("=" * 100)
from langchain.prompts.example_selector import LengthBasedExampleSelector
 
# These are a lot of examples of a pretend task of creating antonyms.
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
    {"word": "energetic", "antonym": "lethargic"},
    {"word": "sunny", "antonym": "gloomy"},
    {"word": "windy", "antonym": "calm"},
]
 
# We'll use the `LengthBasedExampleSelector` to select the examples.
example_selector = LengthBasedExampleSelector(
    # These are the examples is has available to choose from.
    examples=examples, 
    # This is the PromptTemplate being used to format the examples.
    example_prompt=example_prompt, 
    # This is the maximum length that the formatted examples should be.
    # Length is measured by the get_text_length function below.
    max_length=25,
)
 
# We can now use the `example_selector` to create a `FewShotPromptTemplate`.
dynamic_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Word: {input}\nAntonym:",
    input_variables=["input"],
    example_separator="\n",
)
 
# We can now generate a prompt using the `format` method.
print(dynamic_prompt.format(input="big"))

