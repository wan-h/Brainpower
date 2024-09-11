"""
参考:https://github.com/ysymyth/ReAct/blob/master/hotpotqa.ipynb
"""


# ================================ 模型调用 ==================================
"""
API说明:
https://platform.moonshot.cn/docs/api-reference#%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF

计费标准:
https://platform.moonshot.cn/docs/pricing#%E4%BB%B7%E6%A0%BC%E8%AF%B4%E6%98%8E
"""

from openai import OpenAI
client = OpenAI(
    api_key = "sk-96479af5c4934e3b901404fac3dd29c6",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def llm(prompt, query, stop=["\n"]):
    completion = client.chat.completions.create(
        model = "qwen-max-0428",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
        temperature = 0.3,
        stop=stop
    )
    return completion.choices[0].message.content

# ================================ 环境反馈 ==================================
import random
# 这里使用mock的数据
def search_step(entity):
    answers = [
        "OpenAI，是一家开放人工智能研究和部署公司，其使命是确保通用人工智能造福全人类。",
        "OpenAI创立于2015年12月，总部位于美国旧金山。现由营利性公司OpenAI LP及非营利性母公司OpenAI Inc组成。\
        OpenAI最早为非营利组织，于2015年底由包括萨姆·奥尔特曼（Sam Altman）、彼得·泰尔（Peter Thiel）、里德·霍夫曼（Reid Hoffman）和埃隆·马斯克（Elon Musk）等创办。"
    ]
    return random.choice(answers)

# 根据action执行工具，并返回observation和done
def step(action):
    done = False
    obs = ""
    if action.startswith("search[") and action.endswith("]"):
        entity = action[len("search["):-1]
        obs = search_step(entity)
    elif action.startswith("finish[") and action.endswith("]"):
        answer = action[len("finish["):-1]
        obs = answer
        done = True
    else:
        print("Invalid action: {}".format(action))

    return obs, done

# ================================ Agent策略 ==================================

webthink_examples = """
Question: Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?
Thought 1: I need to search Adam Clayton Powell and The Saimaa Gesture, and find which documentary is about Finnish rock groups.
Action 1: Search[Adam Clayton Powell]
Observation 1: Could not find [Adam Clayton Powell]. Similar: ['Adam Clayton Powell III', 'Seventh Avenue (Manhattan)', 'Adam Clayton Powell Jr. State Office Building', 'Isabel Washington Powell', 'Adam Powell', 'Adam Clayton Powell (film)', 'Giancarlo Esposito'].
Thought 2: To find the documentary, I can search Adam Clayton Powell (film).
Action 2: Search[Adam Clayton Powell (film)]
Observation 2: Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg.The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience.
Thought 3: Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture.
Action 3: Finish[The Saimaa Gesture]

Question: What profession does Nicholas Ray and Elia Kazan have in common?
Thought 1: I need to search Nicholas Ray and Elia Kazan, find their professions, then find the profession they have in common.
Action 1: Search[Nicholas Ray]
Observation 1: Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 \u2013 June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause.
Thought 2: Professions of Nicholas Ray are director, screenwriter, and actor. I need to search Elia Kazan next and find his professions.
Action 2: Search[Elia Kazan]
Observation 2: Elia Kazan was an American film and theatre director, producer, screenwriter and actor.
Thought 3: Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor.
Action 3: Finish[director, screenwriter, actor]
"""

instruction = """Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types: 
(1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.
(2) Finish[answer], which returns the answer and finishes the task.
Here are some examples.
"""

webthink_prompt = instruction + webthink_examples

def react(prompt):
    query = "Question: OpenAI是哪一年创立的?\n"
    for i in range(1, 8):
        print(f"=================== round {i} ===================")
        query += f"Thought {i}:"
        print(query)
        thought_action = llm(prompt, query, stop=[f"\nObservation {i}:"])
        print(thought_action)
        try:
            thought, action = thought_action.strip().split(f"\nAction {i}: ")
        except:
            # 这里是一个容错处理,如果输出没有 Action 的字符串,那么就显示的再让 llm 接龙 Action 后面的内容
            print('ohh...', thought_action)
            thought = thought_action.strip().split('\n')[0]
            query += f" {thought}\nAction {i}:"
            action = llm(prompt, query, stop=[f"\n"]).strip()
        # action[0].lower() 应该一个trick的兼容, 防止返回的首字母大小写不一致问题
        obs, done = step(action[0].lower() + action[1:])
        if done:
            break
        # 如果本次action不是结束,那么观察结果后作为下一轮的输入
        obs = obs.replace('\\n', '')
        query += f" {thought}\nAction {i}: {action}\nObservation {i}: {obs}\n"
        

# ================================ Agent策略 ==================================

if __name__ == '__main__':
    react(webthink_prompt)



"""
=================== round 1 ===================
Question: OpenAI是哪一年创立的?
Thought 1:
我需要搜索OpenAI的创立年份。
Action 1: Search[OpenAI]
=================== round 2 ===================
Question: OpenAI是哪一年创立的?
Thought 1: 我需要搜索OpenAI的创立年份。
Action 1: Search[OpenAI]
Observation 1: OpenAI，是一家开放人工智能研究和部署公司，其使命是确保通用人工智能造福全人类。
Thought 2:
这段信息没有直接提供创立年份，我需要更具体地搜索OpenAI的创立时间。
Action 2: Search[OpenAI 创立年份]
=================== round 3 ===================
Question: OpenAI是哪一年创立的?
Thought 1: 我需要搜索OpenAI的创立年份。
Action 1: Search[OpenAI]
Observation 1: OpenAI，是一家开放人工智能研究和部署公司，其使命是确保通用人工智能造福全人类。
Thought 2: 这段信息没有直接提供创立年份，我需要更具体地搜索OpenAI的创立时间。
Action 2: Search[OpenAI 创立年份]
Observation 2: OpenAI创立于2015年12月，总部位于美国旧金山。现由营利性公司OpenAI LP及非营利性母公司OpenAI Inc组成。        OpenAI最早为非营利组织，于2015年底由包括萨姆·奥尔特曼（Sam Altman）、彼得·泰尔（Peter Thiel）、里德·霍夫曼（Reid Hoffman）和埃隆·马斯克（Elon Musk）等创办。
Thought 3:
现在我知道了OpenAI创立于2015年。
Action 3: Finish[2015年]
"""