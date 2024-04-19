"""
https://www.langchain.com.cn/modules/prompts/prompt_templates/examples/connecting_to_a_feature_store

这里链接到特征存储，如果希望将 LLM 与特定用户的最新信息相结合
特征存储可以是获取最新数据的方式
基本思路是从提示模板内部调用特征存储以检索值，然后将其格式化到提示中
"""

from feast import FeatureStore
from langchain.prompts import PromptTemplate, StringPromptTemplate

feast_repo_path = "./feature_repo/"
store = FeatureStore(repo_path=feast_repo_path)

template = """Given the driver's up to date stats, write them note relaying those stats to them.
If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better
 
Here are the drivers stats:
Conversation rate: {conv_rate}
Acceptance rate: {acc_rate}
Average Daily Trips: {avg_daily_trips}
 
Your response:"""
prompt = PromptTemplate.from_template(template)

# 在这里，我们将设置一个自定义的FeastPromptTemplate。这个提示模板将接受一个驱动程序ID，查找他们的统计数据，并将这些统计数据格式化为提示。
# 请注意，这个提示模板的输入只是driver_id，因为这是唯一的用户定义部分（所有其他变量都在提示模板内查找)。
class FeastPromptTemplate(StringPromptTemplate):
    def format(self, **kwargs) -> str:
        driver_id = kwargs.pop("driver_id")
        feature_vector = store.get_online_features(
            features=[
                'driver_hourly_stats:conv_rate',
                'driver_hourly_stats:acc_rate',
                'driver_hourly_stats:avg_daily_trips'
            ],
            entity_rows=[{"driver_id": driver_id}]
        ).to_dict()
        kwargs["conv_rate"] = feature_vector["conv_rate"][0]
        kwargs["acc_rate"] = feature_vector["acc_rate"][0]
        kwargs["avg_daily_trips"] = feature_vector["avg_daily_trips"][0]
        return prompt.format(**kwargs)

prompt_template = FeastPromptTemplate(input_variables=["driver_id"])
print(prompt_template.format(driver_id=1001))

"""
Given the driver's up to date stats, write them note relaying those stats to them.
If they have a conversation rate above .5, give them a compliment. Otherwise, make a silly joke about chickens at the end to make them feel better
 
Here are the drivers stats:
Conversation rate: 0.4745151400566101
Acceptance rate: 0.055561766028404236
Average Daily Trips: 936
 
Your response:
"""