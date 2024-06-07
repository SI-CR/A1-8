from math import sqrt
from classes.map import Map

class State:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x
        self.id = "(" + str(y) + "," + str(x) + ")"

    def __str__(self) -> str:
        return f"({self.y},{self.x})"

    def validate(self, action: tuple[str, tuple, tuple], slope: int, map_obj: Map) -> bool:
        yd, xd = action[1]
        if (
            yd <= map_obj.up_left[0]
            and yd >= map_obj.down_right[0]
            and xd >= map_obj.up_left[1]
            and xd <= map_obj.down_right[1]
            and map_obj.umt_yx(yd, xd) != map_obj.no_data_value
            and action[2][1] < slope
        ):  return True
        return False

    def successor(self, factor: int, slope: int, map_obj: Map) -> list[tuple[str, tuple, tuple]]:
        successors = []
        actions = []
        length = factor * map_obj.cell_size
        actions.append(("N", (self.y + length, self.x), (float(length), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y + length, self.x)))))
        # actions.append(("NE", (self.y + length, self.x + length), (float(length * sqrt(2)), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y + length, self.x + length)))))
        actions.append(("E", (self.y, self.x + length), (float(length), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y, self.x + length)))))
        # actions.append(("SE", (self.y - length, self.x + length), (float(length * sqrt(2)), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y - length, self.x + length)))))
        actions.append(("S", (self.y - length, self.x), (float(length), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y - length, self.x)))))
        # actions.append(("SW", (self.y - length, self.x - length), (float(length * sqrt(2)), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y - length, self.x - length)))))
        actions.append(("W", (self.y, self.x - length), (float(length), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y, self.x - length)))))
        # O / W
        # actions.append(("NW", (self.y + length, self.x - length), (float(length * sqrt(2)), abs(map_obj.umt_yx(self.y, self.x) - map_obj.umt_yx(self.y + length, self.x - length)))))
        for action in actions:
            if self.validate(action, slope, map_obj):
                successors.append(action)
        return successors

    def get_y(self) -> int:
        return self.y
    
    def get_x(self) -> int:
        return self.x
    
    def get_id(self) -> str:
        return self.id