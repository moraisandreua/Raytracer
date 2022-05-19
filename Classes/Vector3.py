import math

class Vector3():
    def __init__(self, x, y, z):
        self.x=float(x)
        self.y=float(y)
        self.z=float(z)

    def sum(self, x, y, z):
        self.x+=x
        self.y+=y
        self.z+=z

    def sub(self, x, y, z):
        self.x-=x
        self.y-=y
        self.z-=z
    
    def escalar(self, scale):
        self.x*=scale
        self.y*=scale
        self.z*=scale

    def size(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    def normal(self):
        return Vector3(self.x/self.size(), self.y/self.size(), self.z/self.size())