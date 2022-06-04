import numpy as np
import math
import sys
from Classes.Vector3 import Vector3
from Classes.Hit import Hit

class Sphere():
    def __init__(self, transformation, material):
        self.transformation=transformation
        self.material=material

    def intersect(self, ray):
        t0, t1=None  # solutions for t if the ray intersects 
        
        #if 0 
        # geometric solution
        L = np.subtract([0,0,0], [ray.origin.x, ray.origin.y, ray.origin.z])

        tca = np.dot(L, [ray.direction.x, ray.direction.y, ray.direction.z]); 
        
        d2 = np.dot(L, L) - tca * tca; 

        if (d2 > 1): return False; 
        
        thc = math.sqrt(1 - d2); # thc: por favor enrola esse

        t0 = tca - thc

        t1 = tca + thc
 
        if(t0 > t1): t0,t1=[t1, t0]
        

        if(t0 < sys.float_info.epsilon):
            t0 = t1

            if (t0 < sys.float_info.epsilon): 
                return False
        
        t = t0; 

        if (t < sys.float_info.epsilon):
            return False
        
        # ponto de internção
        L = Vector3(ray.origin.X + ray.direction.X * t, ray.origin.Y + ray.direction.Y * t, ray.origin.Z + ray.direction.Z * t)

        hit = Hit(t)
        hit.point=L
        if (hit.tDistance > sys.float_info.epsilon and hit.tDistance < hit.tMin):        
            hit.tMin = hit.tDistance
            hit.found = True
            hit.material = self.material


        return True