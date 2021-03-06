from array import array
from logging import NullHandler
import sys
from Classes.Color3 import Color3
from Classes.Vector3 import Vector3
from Classes.Ray import Ray
from Classes.Hit import Hit
from Parcing import Parcing
import random

import math
from tracemalloc import start
import numpy as np
from OpenGL import GL
import OpenGL.GLU as GLU

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtOpenGL import QOpenGLWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel, QFileDialog, QProgressBar
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6 import QtGui


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.recursionLevel=1
        self.parser=None

        self.setWindowTitle("COSIG Ray Tracer")
        self.setFixedSize(QSize(800, 700))

        self.imageHeight=0
        self.imageWidth=0
        self.pixelScale=0
        self.pixels=[]
        self.itt=0 # contagem de iterações no traceray
        
        layoutVertical = QVBoxLayout()
        self.opengl_window = GLWidget()
        
        
        layoutHorizontal = QHBoxLayout()
        loadButton = QPushButton("Load")
        loadButton.clicked.connect(self.loadFile)
        startButton = QPushButton("Start")
        startButton.clicked.connect(self.startRaytracing)
        self.labelSliderValue = QLabel("Recursion level: 1")

        sliderLabelLayoutHorizontal = QHBoxLayout()
        self.slider = QSlider(orientation=Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.sliderValueChanged)
        
        sliderLabelLayoutHorizontal.addWidget(self.labelSliderValue)
        sliderLabelLayoutHorizontal.addWidget(self.slider)

        layoutHorizontal.addWidget(loadButton)
        layoutHorizontal.addWidget(startButton)
        layoutHorizontal.addLayout(sliderLabelLayoutHorizontal)

        self.prog_bar = QProgressBar(self)
        self.prog_bar.setValue(0)
        
        layoutVertical.addWidget(self.opengl_window)
        layoutVertical.addLayout(layoutHorizontal)
        layoutVertical.addWidget(self.prog_bar)

        # Set the central widget of the Window.
        widget = QWidget()
        widget.setLayout(layoutVertical)
        self.setCentralWidget(widget)

        

    def sliderValueChanged(self):
        value = math.floor(self.slider.value()/20)+1 # limita entre 1 e 5
        self.recursionLevel=value
        self.labelSliderValue.setText("Recursion level: " + str(value))

    def loadFile(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'Text Files (*.txt)')

        if path != ('', ''):
            self.parse(path[0])

    def startRaytracing(self):
        print("start button clicked")
        self.showFinalImage()

    def parse(self, filename):
        self.parser=Parcing(filename)
        self.parser.parse()

        self.imageHeight = 2 * self.parser.camera.distance * math.tan(self.parser.camera.fov() / 2)
        self.imageWidth = self.imageHeight * self.parser.images[0].width / self.parser.images[0].height
        self.pixelScale = self.imageHeight / self.parser.images[0].height

        # criar matriz de pixeis
        # para poder adicionar o objecto Color3 a uma dada posição da matrix
        # matrix deve ter o comprimento e a altura da imagem
        self.generatePixelMatrix()

        # self explanatory
        self.traceRays()

    def generatePixelMatrix(self):
        for y in range(0, int(self.parser.images[0].height)):
            newRow=[]
            for x in range(0, int(self.parser.images[0].width)):
                newRow.append(0)
            self.pixels.append(newRow)


    def showPercentage(self, i,j):
        self.itt+=1
        percentage = round(self.itt/40000 * 100, 0)
        self.prog_bar.setValue(percentage)

    def traceRays(self):
        origin=Vector3(0,0,self.parser.camera.distance)
        intersecoes=[]

        # percorre as linhas (y)
        for j in range(0, int(self.parser.images[0].height)):
            # percorre as colunas (x)
            for i in range(0, int(self.parser.images[0].width)):
                # calcular as coordenadas P.x, P.y e P.z do centro do píxel[i][j]
                pX = (i + 0.5) * self.pixelScale - self.imageWidth / 2
                pY = -(j + 0.5) * self.pixelScale + self.imageHeight / 2
                pZ = 0

                # calcular a direção do vetor que define a direção do raio
                direction = Vector3(pX-0, pY-0, pZ-self.parser.camera.distance); # ou seja, direction = new Vector3(P.x, P.y, -distance);
                directionNormalized=direction.normal()

                # criar ray
                ray = Ray(origin, directionNormalized)
                rec=2 # recursividade
                inter = self.traceRay(ray, rec)
                inter[0].checkRange() #ajustar a cor
                inter.append(i)
                inter.append(j)
                intersecoes.append(inter) # adicionar a uma lista de interseções para mais tarde ordena-los

                #mostrar percentagem atual
                self.showPercentage(i,j)

        print("começa a ordenação de interseções")
        intersecoes = sorted(intersecoes, key=lambda x:x[1], reverse=True)

        for inter in intersecoes:
            # converter para 32bit
            i=inter[2]
            j=inter[3]
            color=inter[0]
            self.pixels[i][j] = Color3(int(255.0 * color.r), int(255.0 * color.g), int(255.0 * color.b))

        print("end tracing")


    def traceRay(self, ray, rec):
        hit=Hit(0)

        temp=[ y for x in self.parser.triangles for y in x.triangles ]
        temp.extend(self.parser.spheres)
        temp.extend(self.parser.boxes)

        for object in temp:
            # trasformação de um objeto. tem de ser feito .super porque no caso dos triangulos, o donut é uma classe Triangles com vários triangulos lá dentro
            tempTransform = object.super.transformation
            
            
            # ray transformado com base no transform aplicado ao object + transform aplicada à camara
            transformedRay = tempTransform.inverse(ray)

            object.intersect(transformedRay, hit)

            # se for encontrado um ponto de interseção
            if hit.found and tempTransform!=None:
                newPoint = tempTransform.transform(hit.point)
                hit.point = newPoint
                hit.tDistance = ray.distance(newPoint)
                hit.normal = tempTransform.transpose(hit.normal)

        
            if hit.found:
                color = Color3(0,0,0)
                for l in self.parser.lights:
                    color.r = color.r + (l.color.r * hit.material.color.r * hit.material.ambient)
                    color.g = color.g + (l.color.g * hit.material.color.g * hit.material.ambient)
                    color.b = color.b + (l.color.b * hit.material.color.b * hit.material.ambient)

                    posLight=[ x[3] for x in l.transformation.transformedWithCameraMatrix ]

                    vectorI = Vector3( posLight[0]-hit.point.x, posLight[1]-hit.point.y, posLight[2]-hit.point.z ).normal()
                    cosTheta = np.dot([hit.normal.x, hit.normal.y, hit.normal.z],[vectorI.x, vectorI.y, vectorI.z])

                    if cosTheta > 0:
                        color.r = color.r + (l.color.r * hit.material.color.r * hit.material.difuse * cosTheta)
                        color.g = color.g + (l.color.g * hit.material.color.g * hit.material.difuse * cosTheta)
                        color.b = color.b + (l.color.b * hit.material.color.b * hit.material.difuse * cosTheta)

                return [color, hit.tDistance]
        
        return [Color3(0.2,0.2,0.2), sys.float_info.max]

    def showFinalImage(self):
        arrayOfArrays=[ [int(x.r), int(x.g), int(x.b)] for y in self.pixels for x in y ]
        matrixDecomposition = [item for sublist in arrayOfArrays for item in sublist]
        print("will now paint the pixels")
        self.opengl_window.imageWidth=int(self.parser.images[0].width)
        self.opengl_window.imageHeight=int(self.parser.images[0].height)
        self.opengl_window.imageData=matrixDecomposition
        self.opengl_window.paintGL()


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QOpenGLWidget.__init__(self, parent)
        self.imageWidth=0
        self.imageHeight=0
        self.imageData=[]

    def initializeGL(self):
        #self.qglClearColor(QtGui.QColor(0, 0, 255))    # initialize the screen to blue
        GL.glClearColor(0, 0, 255, 0.5) # azul com transparencia
        GL.glEnable(GL.GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glDrawPixels(self.imageWidth, self.imageHeight, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, (GL.GLubyte * len(self.imageData))(*self.imageData))
        self.update()