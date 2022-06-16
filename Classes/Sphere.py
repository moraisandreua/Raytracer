import numpy as np
import math
import sys
from Classes.Vector3 import Vector3
from Classes.Hit import Hit

class Sphere():
    def __init__(self, transformation, material):
        self.super=self # é necessário para normalizar o objeto com os triangulos

        self.transformation=transformation
        self.material=material

    def intersect(self, ray, hit):
        # solutions for t if the ray intersects 
        t0=None  
        t1=None

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
        
        # ponto de interseção
        rayOrigin=[ray.origin.x, ray.origin.y, ray.origin.z]
        rayDirection=[ray.direction.x, ray.direction.y, ray.direction.z]
        L = Vector3(rayOrigin[0] + rayDirection[0] * t, rayOrigin[1] + rayDirection[1] * t, rayOrigin[2] + rayDirection[2] * t)

        hit.point=L
        hit.tDistance=t

        if (hit.tDistance > sys.float_info.epsilon and hit.tDistance < hit.tMin):        
            hit.tMin = hit.tDistance
            hit.found = True
            hit.material = self.material
            hit.normal=L.normal()


        return True