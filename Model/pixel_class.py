class Pixel():
    def __init__(self, x, value):
        self.x = x
        self.value = value

    def __repr__(self):
        return repr((self.value, self.x))
