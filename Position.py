import math


class Position:

    def __init__(self, location: str = None):
        if location is not None:
            location = location.split(',')
            self.x = float(location[0])
            self.y = float(location[1])
            self.z = float(location[2])
        else:
            self.x = 0
            self.y = 0
            self.z = 0

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def distance(self, p1) -> float:
        return math.sqrt((self.x - p1.x) ** 2 + (self.y - p1.y) ** 2)
