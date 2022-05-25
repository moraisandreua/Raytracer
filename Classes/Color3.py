class Color3():
    def __init__(self, r, g, b):
        self.r=r
        self.g=g
        self.b=b

    def checkRange(self):
        if self.r<0:
            self.r=0

        if self.g<0:
            self.g=0

        if self.b<0:
            self.b=0