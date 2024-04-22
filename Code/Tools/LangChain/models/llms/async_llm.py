"""
https://www.langchain.com.cn/modules/models/llms/examples/async_llm

使用agenerate方法异步调用OpenAI LLM
"""

import time
import asyncio
 
from langchain.llms import OpenAI
 
def generate_serially():
    llm = OpenAI(temperature=0.9)
    for _ in range(10):
        resp = llm.generate(["Hello, how are you?"])
        print(resp.generations[0][0].text)
 
async def async_generate(llm):
    resp = await llm.agenerate(["Hello, how are you?"])
    print(resp.generations[0][0].text)
 
async def generate_concurrently():
    llm = OpenAI(temperature=0.9)
    tasks = [async_generate(llm) for _ in range(10)]
    await asyncio.gather(*tasks)
 
s = time.perf_counter()
# If running this outside of Jupyter, use asyncio.run(generate_concurrently())
asyncio.run(generate_concurrently())
elapsed = time.perf_counter() - s
print('\033[1m' + f"Concurrent executed in {elapsed:0.2f} seconds." + '\033[0m')
 
s = time.perf_counter()
generate_serially()
elapsed = time.perf_counter() - s
print('\033[1m' + f"Serial executed in {elapsed:0.2f} seconds." + '\033[0m')


"""
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, how about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about yourself?
 
I'm doing well, thank you! How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you! How about you?
 
I'm doing well, thank you. How about you?
Concurrent executed in 1.39 seconds.
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about yourself?
 
I'm doing well, thanks for asking. How about you?
 
I'm doing well, thanks! How about you?
 
I'm doing well, thank you. How about you?
 
I'm doing well, thank you. How about yourself?
 
I'm doing well, thanks for asking. How about you?
Serial executed in 5.77 seconds.
 
"""