class Color3():
    def __init__(self, r, g, b):
        self.r=r
        self.g=g
        self.b=b

    def checkRange(self):
        # check less then 0
        if self.r<0:
            self.r=0

        if self.g<0:
            self.g=0

        if self.b<0:
            self.b=0

        # check more than 1
        if self.r>1:
            self.r=1

        if self.g>1:
            self.g=1

        if self.b>1:
            self.b=1