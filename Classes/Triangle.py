from Classes.Vector3 import Vector3
import math

class Triangle():
    def __init__(self, material, vertexA, vertexB, vertexC):
        self.material=material
        self.vertexA=vertexA
        self.vertexB=vertexB
        self.vertexC=vertexC

    def normal(self):
        A=self.vertexB
        B=self.vertexC
        A.sub(self.vertexA.x, self.vertexA.y, self.vertexA.z)
        B.sub(self.vertexA.x, self.vertexA.y, self.vertexA.z)

        newX=((A.y * B.z) - (A.z * B.y))
        newY=((A.z * B.x) - (A.x * B.z))
        newZ=((A.x * B.y) - (A.y * B.x))
        size=math.sqrt(math.pow(newX, 2) + math.pow(newY, 2) + math.pow(newZ, 2))
        return Vector3(newX/size, newY/size, newZ/size)