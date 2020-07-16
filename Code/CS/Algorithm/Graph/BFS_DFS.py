# coding: utf-8
# Author: wanhui0729@gmail.com

'''
图相关算法
'''

from collections import deque

class Graph(object):
    '''
    Graph类
    '''
    def __init__(self):
        # 已经遍历的节点存储
        self.neighbor = {}
    def add_node(self, node: tuple):
        key, val = node
        self.neighbor[key] = val
    def __len__(self):
        return len(self.neighbor)

def BFS(graph:Graph, name):
    '''
    广度优先搜索，时间复杂度O(V+E)，V为顶点数，E为边数
    '''
    # 队列先进先出
    search_queue = deque()
    search_queue += graph.neighbor[name]
    # 存储已遍历节点
    searched = []
    searched.append(name)
    while search_queue:
        node_name = search_queue.popleft()
        if node_name not in searched:
            search_queue += graph.neighbor[node_name]
            searched.append(node_name)
    return searched

def DFS(graph: Graph, name):
    '''
    深度优先搜索，时间复杂度O(V+E)，V为顶点数，E为边数
    '''
    # 栈后进先出
    stack = []
    stack += graph.neighbor[name]
    # 存储已遍历节点
    searched = []
    searched.append(name)
    while stack:
        node_name = stack.pop()
        if node_name not in searched:
            stack += graph.neighbor[node_name]
            searched.append(node_name)
    return searched


if __name__ == '__main__':
    graph = Graph()
    graph.add_node(('A', ['B', 'C']))
    graph.add_node(('B', ['E']))
    graph.add_node(('C', ['B', 'D', 'E']))
    graph.add_node(('D', ['F']))
    graph.add_node(('E', ['F']))
    graph.add_node(('F', []))
    search_path = BFS(graph, 'A')
    assert search_path == ['A', 'B', 'C', 'E', 'D', 'F']
    search_path = DFS(graph, 'A')
    assert search_path == ['A', 'C', 'E', 'F', 'D', 'B']