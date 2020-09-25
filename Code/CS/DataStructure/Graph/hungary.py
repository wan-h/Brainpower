# coding: utf-8
# Author: wanhui0729@gmail.com

'''

图相关算法

graph:

   E  F  G  H

A  1  0  1  0

B  0  1  0  1

C  1  0  0  1

D  0  0  1  0


'''

class DFS_hungary(object):
    def __init__(self, graph):
        self.g = graph  # 无向图的矩阵表示
        self.Nx = len(graph)  # 顶点集A的个数
        self.Ny = len(graph[0])  # 顶点集B的个数
        self.cx = [-1] * self.Nx  # 初始匹配
        self.cy = [-1] * self.Ny  # 初始匹配
        self.visited = [0] * self.Ny
        self.M = []
        self.res = 0

    # 遍历顶点A集合，得到最大匹配
    def max_match(self):
        for i in range(self.Nx):
            if self.cx[i] == -1:  # 未匹配
                for j in range(self.Ny):
                    self.visited[j] = 0
                self.res += self.path(i)
                print('i', i, 'M', self.M)
        return self.res

    # 增广路置换获得更大的匹配
    def path(self, u):
        for v in range(self.Ny):
            if self.g[u][v] and (not self.visited[v]):  # 如果可连且未被访问过
                self.visited[v] = 1  # 访问该顶点
                if self.cy[v] == -1:  # 如果未匹配， 则建立匹配
                    self.cx[u], self.cy[v] = v, u
                    self.M.append((u, v))
                    return 1
                else:
                    self.M.remove((self.cy[v], v))  # 如果匹配则删除之前的匹配
                    if self.path(self.cy[v]):  # 递归调用
                        self.cx[u], self.cy[v] = v, u
                        self.M.append((u, v))
                        return 1
                print('v', v, 'M', self.M)
        return 0


class BFS_hungary(object):
    def __init__(self, graph):
        self.g = graph  # 无向图的矩阵表示
        self.Nx = len(graph)  # 顶点集A的个数
        self.Ny = len(graph[0])  # 顶点集B的个数
        self.Mx = [-1] * self.Nx  # 初始匹配
        self.My = [-1] * self.Ny  # 初始匹配
        self.chk = [-1] * max(self.Nx, self.Ny)  # 是否匹配
        self.Q = []

    def max_match(self):
        res = 0  # 最大匹配数
        self.Q = [0 for _ in range(self.Nx * self.Ny)]
        prev = [0] * max(self.Nx, self.Ny)  # 是否访问
        for i in range(self.Nx):
            if self.Mx[i] == -1:  # A中顶点未匹配
                qs = qe = 0
                self.Q[qe] = i
                qe += 1
                prev[i] = -1
                flag = 0
                while (qs < qe and not flag):
                    u = self.Q[qs]
                    for v in range(self.Ny):
                        if flag: continue
                        if self.g[u][v] and self.chk[v] != i:
                            self.chk[v] = i
                            self.Q[qe] = self.My[v]
                            qe += 1
                            if self.My[v] >= 0:
                                prev[self.My[v]] = u
                            else:
                                flag = 1
                                d, e = u, v
                                while d != -1:  # 将原匹配的边去掉加入原来不在匹配中的边
                                    t = self.Mx[d]
                                    self.Mx[d] = e
                                    self.My[e] = d
                                    d = prev[d]
                                    e = t
                qs += 1
            if self.Mx[i] != -1:  # 如果已经匹配
                res += 1
        return res

if __name__ == '__main__':
    g = [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1], [0, 0, 1, 0]]
    bh = BFS_hungary(g)
    assert bh.max_match() == 4

    dh = DFS_hungary(g)
    assert dh.max_match() == 4

'''
DFS 的优点是思路清晰、代码量少，但是性能不如 BFS。测试了两种算法的性能。
对于稀疏图，BFS 版本明显快于 DFS 版本；而对于稠密图两者则不相上下。
'''