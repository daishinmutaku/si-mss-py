class Pixel():
    def __init__(self, x, y, value):
        self.x: int = x
        self.y: int = y
        self.value: float = value

    def __repr__(self):
        return repr((self.value, self.x, self.y))
