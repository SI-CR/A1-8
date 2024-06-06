from classes.state import State

class Node:
    def __init__(self, node_id, parent, state: State, value, depth, cost, heuristic, action):
        self.node_id = node_id
        self.parent = parent
        self.state = state
        self.value = value
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

    def get_path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __str__(self):
        return f"[{self.node_id}][({self.cost[0]:.3f},{round(self.cost[1], 3):.3f}),{self.state.node_id},{self.parent.get_id() if self.parent else None},{self.action},{self.depth},{self.heuristic},{self.value:.4f}]"

    def get_id(self):
        return self.node_id

    def get_value(self):
        return self.value

    def get_state(self):
        return self.state

    def get_depth(self):
        return self.depth

    def get_cost(self):
        return self.cost