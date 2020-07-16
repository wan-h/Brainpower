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

def bellman_fold(graph: Graph, start_node_name, end_node_name):
    '''
    贝尔曼-福德算法
    '''
    def find_shortest_path(parents, start_node_name, end_node_name):
        '''
        找到最短路径
        '''
        node = end_node_name
        shortest_path = [end_node_name]
        while parents[node] != start_node_name:
            shortest_path.append(parents[node])
            node = parents[node]
        shortest_path.append(start_node_name)
        shortest_path.reverse()
        return shortest_path
    distance = {start_node_name: 0}
    parents = {}
    for i in range(len(graph) - 1):
        for u in graph.neighbor.keys():
            for v in graph.neighbor[u]:
                if v not in distance:
                    distance[v] = float('inf')
                if distance[v] > graph.neighbor[u][v] + distance[u]:
                    distance[v] = graph.neighbor[u][v] + distance[u]
                    parents[v] = u
    for u in graph.neighbor.keys():
        for v in graph.neighbor[u]:
            if distance[v] > graph.neighbor[u][v] + distance[u]:
                return None, None
    shortest_path = find_shortest_path(parents, start_node_name, end_node_name)
    return shortest_path

if __name__ == '__main__':
    graph = Graph()
    graph.add_node(('start', {'a': 1, 'b': 2}))
    graph.add_node(('a', {'c': 1}))
    graph.add_node(('c', {'end': 1}))
    graph.add_node(('b', {'a': -2, 'end': 5}))
    graph.add_node(('end', {}))
    assert bellman_fold(graph, 'start', 'end') == ['start', 'b', 'a', 'c', 'end']