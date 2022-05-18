import sys

import math
import numpy as np
from OpenGL import GL
import OpenGL.GLU as GLU

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtOpenGL import QOpenGLWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6 import QtGui


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.recursionLevel=1

        self.setWindowTitle("COSIG Ray Tracer")
        self.setFixedSize(QSize(800, 700))
        
        layoutVertical = QVBoxLayout()
        opengl_window = GLWidget()
        
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
        
        layoutVertical.addWidget(opengl_window)
        layoutVertical.addLayout(layoutHorizontal)

        # Set the central widget of the Window.
        widget = QWidget()
        widget.setLayout(layoutVertical)
        self.setCentralWidget(widget)

    def sliderValueChanged(self):
        value = math.floor(self.slider.value()/20)+1 # limita entre 1 e 5
        self.recursionLevel=value
        self.labelSliderValue.setText("Recursion level: " + str(value))

    def loadFile(self):
        print("load button clicked")

    def startRaytracing(self):
        print("start button clicked")

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QOpenGLWidget.__init__(self, parent)

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