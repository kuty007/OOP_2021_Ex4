class Position:

    def __init__(self, location: tuple, **kwargs):
        self.x = location[0]
        self.y = location[1]
        self.z = location[2]

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z
