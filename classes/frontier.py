import heapq
from classes.node import Node

class Frontier:
    def __init__(self):
        self.nodes = []

    def is_empty(self):
        return not self.nodes

    def add_node(self, node):
        heapq.heappush(self.nodes, (node.get_value(), node.get_id(), node))

    def remove_node(self) -> Node:
        return heapq.heappop(self.nodes)[2]

    def __str__(self):
        return str(self.nodes)