# coding: utf-8
# Author: wanhui0729@gmail.com

"""
https://github.com/facebookresearch/faiss/wiki/Home
"""
import faiss
import numpy as np

# Getting some data
d = 64  # dimension
nb = 100000  # database size
nq = 10000  # nb of queries
np.random.seed(1234)  # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.

# Building an index and adding the vectors to it
index = faiss.IndexFlatL2(d)  # build the index
print(index.is_trained)
index.add(xb)  # add vectors to the index
print(index.ntotal)

# Searching
k = 4  # we want to see 4 nearest neighbors
D, I = index.search(xb[:5], k)  # sanity check
print(I)
print(D)
D, I = index.search(xq, k)  # actual search
print(I[:5])  # neighbors of the 5 first queries
print(I[-5:])  # neighbors of the 5 last queries

# Faster search
print("#" * 21)
nlist = 100
k = 4
quantizer = faiss.IndexFlatL2(d)  # the other index
index = faiss.IndexIVFFlat(quantizer, d, nlist)
assert not index.is_trained
index.train(xb)
assert index.is_trained

index.add(xb)  # add may be a bit slower as well
D, I = index.search(xq, k)  # actual search
print(I[-5:])  # neighbors of the 5 last queries
index.nprobe = 10  # default nprobe is 1, try a few more
D, I = index.search(xq, k)
print(I[-5:])
