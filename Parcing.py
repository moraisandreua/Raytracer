from Classes.Box import Box
from Classes.Camera import Camera
from Classes.Color3 import Color3
from Classes.Image import Image
from Classes.Light import Light
from Classes.Material import Material
from Classes.Sphere import Sphere
from Classes.Transformation import Transformation
from Classes.Triangle import Triangle
from Classes.Triangles import Triangles
from Classes.Vector3 import Vector3
import re

class Parcing():
    def __init__(self, filename):
        self.filename=filename
        self.colors=[]
        self.vectors=[]
        self.images=[]
        self.transformations=[]
        self.camera=None
        self.lights=[]
        self.materials=[]
        self.triangles=[]
        self.spheres=[]
        self.boxes=[]
    
    def parse(self):
        f=open(self.filename, "rb")
        content=f.read().decode("utf-8")

        objects=["mage", "Transformation", "Material", "Light", "Camera", "Triangles", "Box", "Sphere"]

        for prefix in objects:

            pos=[m.start() for m in re.finditer(prefix+"\r\n{", content)]
            for i in pos:
                startPos=i+len(prefix+"\r\n{")+1
                endPos=content.find("}", startPos)

                confBlock=content[startPos:endPos].replace("\t", "").strip()
                self.parseObject(prefix, confBlock)

        #print(len(self.triangles), len(self.triangles)*3)
    
    def parseObject(self, prefix, properties):
        if prefix=="mage":
            self.images.append(Image(properties.split("\r\n")[0].split(" ")[0], properties.split("\r\n")[0].split(" ")[1], Color3(properties.split("\r\n")[1].split(" ")[0], properties.split("\r\n")[1].split(" ")[1], properties.split("\r\n")[1].split(" ")[2])))
            
        if prefix=="Box":
            len(self.materials)
            len(self.transformations)
            self.boxes.append(Box(self.transformations[int(properties.split("\r\n")[0])], self.materials[int(properties.split("\r\n")[1])]))

        if prefix=="Camera":
            pass

        if prefix=="Light":
            pass

        if prefix=="Material":
            self.materials.append(Material(Color3(properties.split("\r\n")[0].split(" ")[0], properties.split("\r\n")[0].split(" ")[1], properties.split("\r\n")[0].split(" ")[2]), properties.split("\r\n")[1].split(" ")[0], properties.split("\r\n")[1].split(" ")[1], properties.split("\r\n")[1].split(" ")[2], properties.split("\r\n")[1].split(" ")[3], properties.split("\r\n")[1].split(" ")[4]))

        if prefix=="Sphere":
            pass

        if prefix=="Transformation":
            pass

        if prefix=="Triangles":
            count=0
            currentMaterial=None
            currentVectors=[]
            self.triangles.append(Triangles(properties.split("\r\n")[0], []))
            for x in properties.split("\r\n")[1:]:
                if count % 4 == 0:
                    currentVectors=[]
                    currentMaterial=self.materials[int(properties.split("\r\n")[count+1])]
                else:
                    currentVectors.append(Triangle(currentMaterial, properties.split("\r\n")[count+1].split(" ")[0], properties.split("\r\n")[count+1].split(" ")[1], properties.split("\r\n")[count+1].split(" ")[2]))
                
                if count % 4 == 3:
                    self.triangles[-1].triangles=currentVectors