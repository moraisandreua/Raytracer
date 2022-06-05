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
        v0=[self.vertexA.x, self.vertexA.y, self.vertexA.z]
        v1=[self.vertexB.x, self.vertexB.y, self.vertexB.z]
        v2=[self.vertexC.x, self.vertexC.y, self.vertexC.z]

        # compute plane's normal
        v0v1 = np.subtract(v1, v0); 
        v0v2 = np.subtract(v2, v0); 

        # no need to normalize
        N=np.cross(v0v1, v0v2)
        area = math.sqrt( math.pow(N[0],2) + math.pow(N[1],2) + math.pow(N[2],2) );  # area of the triangle = half of the length of cross product
        denom = np.dot(N, N);

        # Step 1: finding P
 
        #   check if ray and plane are parallel ?
        NdotRayDirection = np.dot(N, [ray.direction.x, ray.direction.y, ray.direction.z])

        if (abs(NdotRayDirection) < sys.float_info.epsilon):  # o segundo parametro é almost 0, porque correpsponde a epsilon
            return False;  # they are parallel so they don't intersect ! 
    
        #   compute d parameter using equation 2
        d = np.dot(N, v0); 
    
        #   compute t (equation 3)
        t = np.dot(N, [ray.origin.x, ray.origin.y, ray.origin.z]) + d # NdotRayDirection; 
        
        #   check if the triangle is in behind the ray
        if (t < 0): return False;  #the triangle is behind 
    
        #   compute the intersection point using equation 1
        
        rayOrigin=np.array([ray.origin.x, ray.origin.y, ray.origin.z])
        rayDirection=t*np.array([ray.direction.x, ray.direction.y, ray.direction.z])
        P = [rayOrigin[0] + rayDirection[0], rayOrigin[1] + rayDirection[1], rayOrigin[2] + rayDirection[2]]

        # Step 2: inside-outside test
        C = None; # vector perpendicular to triangle's plane 
    
        # edge 0
        edge0 = np.subtract(v1, v0) 
        vp0 = np.subtract(P, v0)
        C = np.cross(edge0, vp0)

        if (np.dot(N, C) < 0): return False  #P is on the right side 
    
        # edge 1
        edge1 = np.subtract(v2, v1) 
        vp1 = np.subtract(P, v1); 
        C = np.cross(edge1,vp1)
        if (np.dot(N,C) < 0):  return False;  # P is on the right side 
    
        # edge 2
        edge2 = np.subtract(v0, v2); 
        vp2 = np.subtract(P, v2); 
        C = np.cross(edge2,vp2); 
        if (np.dot(N, C) < 0): return False  #P is on the right side

        # if (np.dot([ray.direction.x, ray.direction.y, ray.direction.z], hit.normal) < (-1)*sys.float_info.epsilon): return False
        
        hit.point = Vector3(P[0], P[1], P[2])
        hit.tDistance=t

        #ObjCoordToWorldCoord(ray, hit);

        if (hit.tDistance > sys.float_info.epsilon and hit.tDistance < hit.tMin):        
            hit.tMin = hit.tDistance
            hit.found = True
            hit.material = self.material

            # hit.normal = ConvertNormalToWorld(N);
    
        return True;  # this ray hits the triangle 