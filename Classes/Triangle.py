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


        """v0=np.array([self.vertexA.x, self.vertexA.y, self.vertexA.z])
        v1=np.array([self.vertexB.x, self.vertexB.y, self.vertexB.z])
        v2=np.array([self.vertexC.x, self.vertexC.y, self.vertexC.z])

        # compute plane's normal
        v0v1 = np.subtract(v1, v0); 
        v0v2 = np.subtract(v2, v0); 

        # no need to normalize
        N=np.cross(v0v1, v0v2)
        #area = math.sqrt( math.pow(N[0],2) + math.pow(N[1],2) + math.pow(N[2],2) );  # area of the triangle = half of the length of cross product
        denom = np.dot(N, N);

        # Step 1: finding P
 
        #   check if ray and plane are parallel ?
        NdotRayDirection = np.dot(N, np.array([ray.direction.x, ray.direction.y, ray.direction.z]))

        if (abs(NdotRayDirection) < sys.float_info.epsilon):  # o segundo parametro é almost 0, porque correpsponde a epsilon
            return False;  # they are parallel so they don't intersect ! 
    
        #   compute d parameter using equation 2
        d = np.dot(N, v0); 
    
        #   compute t (equation 3)
        t = (np.dot(N, np.array([ray.origin.x, ray.origin.y, ray.origin.z])) + d) / NdotRayDirection; 
        
        #   check if the triangle is in behind the ray
        if (t < 0): return False;  #the triangle is behind 
    
        #   compute the intersection point using equation 1
        
        rayOrigin = np.array([ray.origin.x, ray.origin.y, ray.origin.z])
        rayDirection = t * np.array([ray.direction.x, ray.direction.y, ray.direction.z])
        P = np.array([rayOrigin[0] + rayDirection[0], rayOrigin[1] + rayDirection[1], rayOrigin[2] + rayDirection[2]])

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

        # set the hit
        hit.point = Vector3(P[0], P[1], P[2])
        hit.tDistance=t

        if (hit.tDistance > sys.float_info.epsilon and hit.tDistance < hit.tMin):        
            hit.tMin = hit.tDistance
            hit.found = True
            hit.material = self.material
    
        return True;  # this ray hits the triangle """