from classes.state import State

class Problem:
    def __init__(self, filename: str, initial_state: State):
        self.filename = filename
        self.initial_state = initial_state

    def is_goal(self, current_state: State, destination_state: State) -> bool:
        return current_state.get_y() == destination_state.get_y() and current_state.get_x() == destination_state.get_x()

    def get_filename(self) -> str:
        return self.filename

    def get_initial_state(self) -> State:
        return self.initial_state