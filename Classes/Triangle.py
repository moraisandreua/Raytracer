from Classes.Vector3 import Vector3
from Classes.Hit import Hit
import numpy as np
import sys
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
        A.sub(self.vertexA.x, self.vertexA.y, self.vertexA.z) # 
        B.sub(self.vertexA.x, self.vertexA.y, self.vertexA.z)

        newX=((A.y * B.z) - (A.z * B.y))
        newY=((A.z * B.x) - (A.x * B.z))
        newZ=((A.x * B.y) - (A.y * B.x))
        size=math.sqrt(math.pow(newX, 2) + math.pow(newY, 2) + math.pow(newZ, 2))
        return Vector3(newX/size, newY/size, newZ/size)

    def intersect(self, ray, hit):
        rayOrigin=[ray.origin.x, ray.origin.y, ray.origin.z]
        rayDirection=[ray.direction.x, ray.direction.y, ray.direction.z]

        v0=np.array([self.vertexA.x, self.vertexA.y, self.vertexA.z])
        v1=np.array([self.vertexB.x, self.vertexB.y, self.vertexB.z])
        v2=np.array([self.vertexC.x, self.vertexC.y, self.vertexC.z])

        v0v1 = np.subtract(v1, v0); 
        v0v2 = np.subtract(v2, v0); 

        P = np.cross(rayDirection, v0v2)
        det=np.dot(v0v1, P)
        epsilon=sys.float_info.epsilon

        if(abs(det) < epsilon): return False

        invertedDet = 1 / det

        T = np.subtract(rayOrigin, v0)
        u = np.dot(T, P) * invertedDet

        if(u < 0 or u > 1): return False

        Q = np.cross(T, v0v1)
        v=np.dot(rayDirection, Q) * invertedDet

        if(v < 0 or (u+v) > 1): return False

        distance = np.dot(v0v2, Q) * invertedDet

        if(distance > epsilon):
            hit.point=[rayOrigin[0] + rayDirection[0]*distance, rayOrigin[1] + rayDirection[1]*distance, rayOrigin[2] + rayDirection[2]*distance]
            hit.tDistance=distance
            hit.tMin = hit.tDistance
            hit.found = True
            hit.material = self.material

        return False