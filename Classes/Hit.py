from re import T
import sys

class Hit():
    def __init__(self, t):
        found=False
        material=None
        point=None # ponto de interceção
        normal=None
        tDistance=t
        tMin=sys.float_info.max

    def getT(self):
        return self.tDistance

    def setAttr(self, found, material, point, normal, tDistance, tMin):
        self.found=found
        self.material=material
        self.point=point
        self.normal=normal
        self.tDistance=tDistance
        self.tMin=tMin
    

