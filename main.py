from classes.map import Map
from classes.state import State
from classes.node import Node
from classes.frontier import Frontier
from classes.problem import Problem
from math import sqrt

def test_umt_values(filename, map_obj: Map):
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        y, x, expected_value = map(float, line.strip().split('\t'))
        if round(map_obj.umt_yx(y, x), 3) != expected_value:
            print(f"Fail: The real value ({round(map_obj.umt_yx(y, x))}) does not match with the expected value ({expected_value}) for the coordinates Y={y}, X={x}")
           
def test_successors(filename, map_obj: Map):
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            y, x = eval(parts[0])
            expected_successors = [eval(s) for s in parts[1:]]
            state = State(y, x)
            actual_successors = [(action, (y, x), (round(length, 3), round(slope, 3))) for action, (y, x), (length, slope) in state.successor(1, 10000, map_obj)]
            if str(actual_successors) != str(expected_successors):
                print(f"For {y, x}\nexpected\t{expected_successors}\nbut got\t\t{actual_successors}")



def is_not_visited(visited_nodes, actual_node: Node):
    for visited_node in visited_nodes:
        if visited_node == actual_node.get_state().get_id():
            return False
    return True

def algorithm(problem: Problem, strategy, max_depth, destination: State):
    actual_node = Node(None, None, None, None, None, None, None, None)
    map_obj = Map(problem.get_filename())
    initial_state = problem.get_initial_state()
    frontier = Frontier()
    global GLOBAL_ID
    GLOBAL_ID = 0
    initial_node = Node(GLOBAL_ID, None, initial_state, 0, 0, (0, 0), calc_heuristic(
        initial_state, strategy, destination), None)
    initial_node.value = calc_value(initial_node, strategy, destination)
    frontier.add_node(initial_node)
    visited_nodes = []
    is_solution = False

    while not frontier.is_empty() and not is_solution:
        actual_node = frontier.remove_node()
        if problem.is_goal(actual_node.get_state(), destination):
            is_solution = True
        if actual_node.get_depth() <= max_depth:
            correct_depth = True
        else:
            correct_depth = False

        if not is_solution and is_not_visited(visited_nodes, actual_node) and correct_depth:
            visited_nodes.append(actual_node.get_state().get_id())
            childs = expand(actual_node, map_obj, strategy, destination)
            for child in childs:
                frontier.add_node(child)

    return actual_node.get_path()
        
def expand(node: Node, map_obj, strategy, destination: State):
    global GLOBAL_ID
    childs = []
    successors = node.get_state().successor(1, 100, map_obj)
    for successor in successors:
        GLOBAL_ID += 1
        successor_state = State(successor[1][0], successor[1][1])
        successor_node = Node(GLOBAL_ID, node, successor_state, 0, node.get_depth()+1, 
            (node.get_cost()[0]+successor[2][0], max(node.get_cost()[1], successor[2][1])), 
            calc_heuristic(successor_state, strategy, destination), successor[0])
        successor_node.value = calc_value(successor_node, strategy, destination)
        childs.append(successor_node)

    return childs

def calc_value(node: Node, strategy, destination: State):
    if "DFS" in strategy:
        return 1/(1+node.get_depth())
    elif "BFS" in strategy:
        return node.get_depth()
    elif "UCS" in strategy:
        return node.get_cost()[0]
    elif "A*" in strategy:
        return calc_heuristic(node.get_state(), strategy, destination) + node.get_cost()[0]
    elif "GREEDY" in strategy:
        return calc_heuristic(node.get_state(), strategy, destination)

def calc_heuristic(state: State, strategy, destination: State):
    if "Euclidea" in strategy:
        return sqrt((destination.get_x() - state.get_x())**2 + (destination.get_y() - state.get_y())**2)
    elif "Manhattan" in strategy:
        return abs(destination.get_x() - state.get_x()) + abs(destination.get_y() - state.get_y())
    else:
        return 0.0



if __name__ == "__main__":

    # # ------- Test the map class -------
    # map_obj = Map("data/LaGomera.hdf5")
    # def calculate_mean(cells):
    #     new_values = cells[cells != map_obj.no_data_value]
    #     if len(new_values) == 0:
    #         return map_obj.no_data_value
    #     return new_values.mean()
    # def calculate_max(cells):
    #     new_values = cells[cells != map_obj.no_data_value]
    #     if len(new_values) == 0:
    #         return map_obj.no_data_value
    #     return new_values.max()
    # new_map_mean = map_obj.resize(300, calculate_mean, "data/LaGomera_300_mean")
    # new_map_max = map_obj.resize(400, calculate_max, "data/LaGomera_400_max")
    # new_map_mean = Map("data/LaGomera_300_mean.hdf5")
    # new_map_max = Map("data/LaGomera_400_max.hdf5")
    # test_umt_values("data/test_map_300_mean.txt", new_map_mean)
    # test_umt_values("data/test_map_400_max.txt", new_map_max)

    # # ------- Test the state class -------
    # test_successors('data/sucesores_300_mean.txt', new_map_mean)
    # test_successors('data/sucesores_400_max.txt', new_map_max)
    # print("Tests passed")

    # ------- Test the algorithm -------
    problem = Problem("data/LaGomera_300_mean.hdf5", State(3117601, 273733))
    solution = algorithm(problem, "BFS", 500000, State(3107401, 287533))
    for node in solution:
        print(node)    