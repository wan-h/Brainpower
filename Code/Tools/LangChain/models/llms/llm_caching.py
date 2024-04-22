"""
https://www.langchain.com.cn/modules/models/llms/examples/llm_caching

类似Python函数lru_cache的缓存机制
"""

from langchain.llms import OpenAI
import langchain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()

# To make the caching really obvious, lets use a slower model.
llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)

# The first time, it is not yet in cache, so it should take longer
llm("Tell me a joke")
 
"""
CPU times: user 26.1 ms, sys: 21.5 ms, total: 47.6 ms
Wall time: 1.68 s
"""

# The second time it is, so it goes faster
llm("Tell me a joke")
"""
CPU times: user 238 µs, sys: 143 µs, total: 381 µs
Wall time: 1.76 ms
"""
 