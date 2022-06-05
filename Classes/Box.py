from Classes.Vector3 import Vector3
from Classes.Hit import Hit
import numpy as np
import math
import sys 

class Box():
    def __init__(self, transformation, material):
        self.transformation=transformation
        self.material=material
        self.bounds=[Vector3(-0.5, -0.5, -0.5), Vector3(0.5,0.5,0.5)]

    def intersect(self, ray, hit):

        txmin = (self.bounds[ray.sign[0]].x - ray.origin.x) * ray.invdir.x; 
        txmax = (self.bounds[1-ray.sign[0]].x - ray.origin.x) * ray.invdir.x; 
        tymin = (self.bounds[ray.sign[1]].y - ray.origin.y) * ray.invdir.y; 
        tymax = (self.bounds[1-ray.sign[1]].y - ray.origin.y) * ray.invdir.y; 
    
        if ((txmin > tymax) or (tymin > txmax)) :
            return False 
    
        if (tymin > txmin): txmin = tymin

        if (tymax < txmax): txmax = tymax; 
    
        tzmin = (self.bounds[ray.sign[2]].z - ray.origin.z) * ray.invdir.z; 
        tzmax = (self.bounds[1-ray.sign[2]].z - ray.origin.z) * ray.invdir.z; 
    
        if ((txmin > tzmax) or (tzmin > txmax)): return False; 
    
        if (tzmin > txmin): txmin = tzmin

        if (tzmax < txmax): txmax = tzmax

        intersectionPoint = Vector3(txmin, tymin, tzmin)
        vectorOriginPoint = [txmin - ray.origin.x, tymin - ray.origin.y, tzmin - ray.origin.z]
        distancia = math.sqrt( math.pow(vectorOriginPoint[0], 2)+math.pow(vectorOriginPoint[1], 2)+math.pow(vectorOriginPoint[2], 2) )
    
        hit.point=intersectionPoint
        hit.tDistance=distancia

        if (hit.tDistance > sys.float_info.epsilon and hit.tDistance < hit.tMin):        
            hit.tMin = hit.tDistance
            hit.found = True
            hit.material = self.material

        return True
        