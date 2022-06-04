from Classes.Vector3 import Vector3
import numpy as np

class Ray():
    def __init__(self, origin, direction):
        self.origin=origin
        self.direction=direction
        self.invdir = Vector3(1/self.direction.x, 1/self.direction.y, 1/self.direction.z)
        self.sign = [self.invdir.x < 0, self.invdir.y < 0, self.invdir.z < 0]

    def intersection(self, distancia):
        return np.add([self.origin.x, self.origin.y, self.origin.z], np.array([self.direction.x, self.direction.y, self.direction.z]) * distancia)