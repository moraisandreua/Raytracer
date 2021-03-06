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
import time
import math


class Parcing():
    def __init__(self, filename):
        self.filename = filename
        self.colors = []
        self.vectors = []
        self.images = []
        self.transformations = []
        self.camera = None
        self.lights = []
        self.materials = []
        self.triangles = []
        self.spheres = []
        self.boxes = []

    def parse(self):
        f = open(self.filename, "rb")
        content = f.read().decode("utf-8")

        objects = ["mage", "Transformation", "Material",
                   "Light", "Camera", "Triangles", "Box", "Sphere"]

        for prefix in objects:

            pos = [m.start() for m in re.finditer(prefix+"\r\n{", content)]
            for i in pos:
                startPos = i+len(prefix+"\r\n{")+1
                endPos = content.find("}", startPos)

                confBlock = content[startPos:endPos].replace("\t", "").strip()
                self.parseObject(prefix, confBlock)

        # multiplicar transformações pela da camara
        for t in self.transformations:
            
            if t!=self.camera.tranformation:
                t.MultiplyTransform(self.camera.tranformation.transformMatrix)
                t.InverseMatrix()
                t.TransposeMatrix()


    def parseObject(self, prefix, properties):
        if prefix == "mage":
            self.images.append(Image(float(properties.split("\r\n")[0].split(" ")[0]), float(properties.split("\r\n")[0].split(" ")[1]), Color3(
                properties.split("\r\n")[1].split(" ")[0], properties.split("\r\n")[1].split(" ")[1], properties.split("\r\n")[1].split(" ")[2])))

        if prefix == "Box":
            self.boxes.append(Box(self.transformations[int(properties.split("\r\n")[
                              0])], self.materials[int(properties.split("\r\n")[1])]))

        if prefix == "Camera":
            self.camera = Camera(self.transformations[int(properties.split(
                "\r\n")[0])], float(properties.split("\r\n")[1]), float(properties.split("\r\n")[2]))

        if prefix == "Light":
            self.lights.append(Light(self.transformations[int(properties.split("\r\n")[0])], Color3(properties.split("\r\n")[
                               1].split(" ")[0], properties.split("\r\n")[1].split(" ")[1], properties.split("\r\n")[1].split(" ")[2])))

        if prefix == "Material":
            self.materials.append(Material(Color3(properties.split("\r\n")[0].split(" ")[0], properties.split("\r\n")[0].split(" ")[1], properties.split("\r\n")[0].split(" ")[2]), properties.split("\r\n")[
                                  1].split(" ")[0], properties.split("\r\n")[1].split(" ")[1], properties.split("\r\n")[1].split(" ")[2], properties.split("\r\n")[1].split(" ")[3], properties.split("\r\n")[1].split(" ")[4]))

        if prefix == "Sphere":
            self.spheres.append(Sphere(self.transformations[int(properties.split(
                "\r\n")[0])], self.materials[int(properties.split("\r\n")[1])]))

        if prefix == "Transformation":
            tempTransform=Transformation()
            linhas = properties.split("\r\n")
            for l in linhas:
                a = l.split(" ")
                if a[0] == "T":
                    tempTransform.translate(float(a[1]), float(a[2]), float(a[3]))

                if a[0] == "S":
                    tempTransform.scale(float(a[1]), float(a[2]), float(a[3]))

                if a[0] == "Rx":
                    tempTransform.rotateX(float(a[1]))

                if a[0] == "Ry":
                    tempTransform.rotateY(float(a[1]))

                if a[0] == "Rz":
                    tempTransform.rotateZ(float(a[1]))

            self.transformations.append(tempTransform)

        if prefix == "Triangles":
            count = 0
            currentMaterial = None
            currentVectors = []
            self.triangles.append(
                Triangles(self.transformations[int(properties.split("\r\n")[0])], []))

            for x in properties.split("\r\n")[1:]:
                if count % 4 == 0:
                    currentVectors = []
                    currentMaterial = self.materials[int(
                        properties.split("\r\n")[count+1])]
                else:
                    currentVectors.append(Vector3(properties.split("\r\n")[count+1].split(" ")[0], properties.split(
                        "\r\n")[count+1].split(" ")[1], properties.split("\r\n")[count+1].split(" ")[2]))

                if count % 4 == 3:
                    self.triangles[-1].triangles += [Triangle(
                        currentMaterial, currentVectors[0], currentVectors[1], currentVectors[2], self.triangles[-1])]

                count += 1