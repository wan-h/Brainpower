"""
https://www.langchain.com.cn/modules/prompts/prompt_templates/examples/partial

"""

from langchain.prompts import PromptTemplate
####################### 使用字符串进行部分格式化 ############################
"""
假设有一个需要两个变量foo和baz的提示模板。
如果在链条的早期获取了foo值，但稍后才获取了baz值，那么等到在一个地方同时拥有两个变量才将它们传递给提示模板可能会很麻烦。
相反，可以使用foo值部分化提示模板，然后将部分化的提示模板传递下去，只需使用它即可
"""
print("=" * 100)
prompt = PromptTemplate(template="{foo}{bar}", input_variables=["foo", "bar"])
partial_prompt = prompt.partial(foo="foo")
print(partial_prompt.format(bar="baz"))

# 也可以只使用部分变量初始化Prompt
prompt = PromptTemplate(template="{foo}{bar}", input_variables=["bar"], partial_variables={"foo": "foo"})
print(prompt.format(bar="baz"))

####################### 函数部分化Partial With Functions ############################
print("=" * 100)
"""
另一个常见的用途是使用函数部分化。这种情况的用例是当总是想以一种常见的方式获取一个变量时。
这个例子最好的例子是日期或时间。假如有一个Prompt，总是要有当前日期。
不能在Prompt中硬编码它，而且将它与其他输入变量一起传递有点麻烦。
在这种情况下，使用一个总是返回当前日期的函数对Prompt进行部分化非常方便。
"""
from datetime import datetime
 
def _get_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}", 
    input_variables=["adjective", "date"]
)
partial_prompt = prompt.partial(date=_get_datetime)
print(partial_prompt.format(adjective="funny"))

# 在这种工作流中，也可以使用部分变量初始化Prompt，这通常更有意义。
prompt = PromptTemplate(
    template="Tell me a {adjective} joke about the day {date}", 
    input_variables=["adjective"],
    partial_variables={"date": _get_datetime}
)
print(prompt.format(adjective="funny"))