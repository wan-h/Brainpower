# coding: utf-8
# Author: wanhui0729@gmail.com

"""
https://github.com/facebookresearch/faiss/wiki/Home

cpu安装：
pip install faiss-cpu

gpu安装：
pip install faiss-gpu
"""
import faiss
import numpy as np

# 基本参数设置
d = 64  # 向量维度
nb = 100000  # index向量库的数据量
nq = 10000  # 待检索query的数目
index_type = 'Flat'                              # index 类型
metric_type = faiss.METRIC_INNER_PRODUCT         # 度量(相似度/距离)类型

# 一，准备向量库向量
print('============================== 1,base vector ==============================')
np.random.seed(1234)  # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
faiss.normalize_L2(xb)
print('xb.shape = ',xb.shape,'\n')

# 二，准备查询向量
print('============================== 2,query vector ==============================')
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.
faiss.normalize_L2(xq)
print('xq.shape = ',xq.shape,'\n')

# 三，构建向量库索引
print('============================== 3,create&train ==============================')
index = faiss.index_factory(d,index_type,metric_type)    #等价于 faiss.IndexFlatIP(d)     
print(index.is_trained) # 输出为True，代表该类index不需要训练，只需要add向量进去即可
index.train(xb)
index.add(xb)                                      # 将向量库中的向量加入到index中
print('index.ntotal=',index.ntotal,'\n')           # 输出index中包含的向量总数，为100000 

# 四，相似向量查询
print('============================== 4, search ==============================')
k = 4                       # topK的K值
D, I = index.search(xq, k)  # xq为待检索向量，返回的I为每个待检索query最相似TopK的索引list，D为其对应的距离

print(f'D Shape: {D.shape}, I Shape: {I.shape}') # 这里的维度和xq是对应的，就是每一个q都去查询
print('nearest vector ids:\n',I[:5],'\n')
print('metric(distances/scores) to query:\n',D[-5:],'\n')

# 五，增删索引向量
print('============================== 5, add&remove ==============================')
xa = np.random.random((10000, d)).astype('float32')
xa[:, 0] += np.arange(len(xa)) / 1000.                
faiss.normalize_L2(xa)
index.add(xa)
print('after add, index.ntotal=',index.ntotal) 
index.remove_ids(np.arange(1000,1111))
print('after remove, index.ntotal=',index.ntotal,'\n') 

# 六，保存加载索引
print('============================== 6, write&read ==============================')
faiss.write_index(index, "large.index")
index_loaded = faiss.read_index('large.index')
print('index_loaded.ntotal=', index_loaded.ntotal)