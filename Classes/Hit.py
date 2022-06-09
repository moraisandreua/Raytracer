from re import T
import sys

class Hit():
    def __init__(self, t):
        self.found=False
        self.material=None
        self.point=None # ponto de interceção
        self.normal=None
        self.tDistance=t
        self.tMin=sys.float_info.max

    def getT(self):
        return self.tDistance

    def setT(self):
        pass

    def setAttr(self, found, material, point, normal, tDistance, tMin):
        self.found=found
        self.material=material
        self.point=point
        self.normal=normal
        self.tDistance=tDistance
        self.tMin=tMin

    

