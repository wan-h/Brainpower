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

def dijkstra(graph: Graph, start_node_name, end_node_name):
    '''
    狄克斯特拉算法
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

    def find_lowest_cost_node(costs, processed):
        '''
        找到开销最小的节点
        '''
        lowest_cost = float("inf")
        lowest_cost_node = None
        for node in costs:
            if costs[node] < lowest_cost and node not in processed:
                lowest_cost = costs[node]
                lowest_cost_node = node
        return lowest_cost_node

    # 遍历图构建开销表、父节点表
    def build_costs_parents_table(graph: Graph, start_node_name):
        costs = {}
        parents = {}
        nodes = graph.neighbor[start_node_name]
        for node_name, node_value in nodes.items():
            costs[node_name] = node_value
            parents[node_name] = start_node_name
        return costs, parents

    # 已经处理的节点
    processed = [start_node_name]
    costs, parents = build_costs_parents_table(graph, start_node_name)
    node = find_lowest_cost_node(costs, processed)
    # 遍历未处理的最小开销节点
    while node:
        cost = costs[node]
        neighbors = graph.neighbor[node]
        for n in neighbors.keys():
            # 遍历图时完善cost表
            if n not in costs.keys(): costs[n] = float('inf')
            new_cost = cost + neighbors[n]
            if new_cost < costs[n]:
                costs[n] = new_cost
                parents[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs, processed)
    shortest_path = find_shortest_path(parents, start_node_name, end_node_name)
    return shortest_path


if __name__ == '__main__':
    graph = Graph()
    graph.add_node(('start', {'a': 6, 'b': 2}))
    graph.add_node(('a', {'c': 1}))
    graph.add_node(('c', {'end': 1}))
    graph.add_node(('b', {'a': 3, 'end': 8}))
    graph.add_node(('end', {}))
    assert dijkstra(graph, 'start', 'end') == ['start', 'b', 'a', 'c', 'end']