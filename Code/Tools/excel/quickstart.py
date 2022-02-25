# coding: utf-8
# Author: wanhui0729@gmail.com

"""
# pandas处理excel依赖xlrd,openpyxl库
pip install xlrd
pip install openpyxl
"""
import pandas as pd

# 读取表格，默认读第一个表，可以使用sheet_name来指定读取哪个表
df = pd.read_excel("example.xlsx")
print("获取到的数据：\n", df)

# 存储数据为表格
data_dict = {
    "id": [100, 200],
    "data": ["100-data", "200-data"]
}
df = pd.DataFrame(data_dict)
# index=True将行索引作为第一列
df.to_excel('output.xlsx', index=False)