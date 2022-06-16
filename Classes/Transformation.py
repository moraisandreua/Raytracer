import math

import numpy as np
from Classes.Vector3 import Vector3
from Classes.Ray import Ray


class Transformation():
    def __init__(self):
        self.transformMatrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.inverseMatrix = np.array([[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]])
        self.transposeMatrix = np.array([[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]])

        # matriz resultante da transformação original com a camara
        self.transformedWithCameraMatrix = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

    def multiply1(self, a, b):

        for i in range(0, 4):
            b[i] = 0
            for j in range(0, 4):
                b[i] += self.transformedWithCameraMatrix[i][j] * a[j]

        return b

    def multiply2(self, pointA, pointB):

        for i in range(0, 4):
            pointB[i] = 0
            for j in range(0, 4):
                pointB[i] += self.inverseMatrix[i][j] * pointA[j]
                
        return pointB

    def multiply3(self, a):
        b = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

        for i in range(0, 4):
            for j in range(0, 4):
                b[i][j] = self.transformMatrix[i][j]
                self.transformMatrix[i][j] = 0

        for i in range(0, 4):
            for j in range(0, 4):
                for k in range(0, 4):
                    self.transformMatrix[i][j] += b[i][k] * a[k][j]

    def multiply4(self, pointA, pointB):

        for i in range(0, 4):
            pointB[i] = 0
            for j in range(0, 4):
                pointB[i] += self.transposeMatrix[i][j] * pointA[j]

        return pointB

    def MultiplyTransform(self, matrix):
        # função usada para juntar a transformação da matrix com a transformação do objeto
        if self.transformedWithCameraMatrix != [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]:
            return None

        matrixB = np.copy(self.transformMatrix)
        self.transformedWithCameraMatrix = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

        for i in range(0, 4):
            for j in range(0, 4):
                for k in range(0, 4):
                    self.transformedWithCameraMatrix[i][j] += matrix[i][k] * matrixB[k][j]

    # cria a matriz correspondente à transformação identidade
    def identityMatrix(self):
        for i in range(0, 4):
            for j in range(0, 4):
                if i == j:
                    self.transformMatrix[i][j] = 1
                else:
                    self.transformMatrix[i][j] = 0

    # cria a matriz correspondente à translação e multiplica a matriz de transformação composta pela matriz recém-criada
    def translate(self, x, y, z):
        translateMatrix = [[None, None, None, None], [None, None, None, None], [
            None, None, None, None], [None, None, None, None]]

        for i in range(0, 4):
            for j in range(0, 4):
                if i == j:
                    translateMatrix[i][j] = 1
                elif j == 3:
                    if i == 0:
                        translateMatrix[i][j] = x
                    elif i == 1:
                        translateMatrix[i][j] = y
                    elif i == 2:
                        translateMatrix[i][j] = z
                    else:
                        translateMatrix[i][j] = 1
                else:
                    translateMatrix[i][j] = 0

        self.multiply3(translateMatrix)

    def Minor(self, matrix, row, column):
        npMatrix = np.array(matrix)

        return npMatrix[np.array(list(range(row))+list(range(row+1,npMatrix.shape[0])))[:,np.newaxis],
               np.array(list(range(column))+list(range(column+1,npMatrix.shape[1])))]

    def Determinant(self, matrix):
        return np.linalg.det(matrix)

    def InverseMatrix(self):
        if (self.inverseMatrix != [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]).any():
            return None

        self.inverseMatrix = np.linalg.inv(self.transformedWithCameraMatrix) 

    def TransposeMatrix(self):
        if (self.transposeMatrix != [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]).any():
            return None

        # cria uma matriz transposta com numpy
        npMatrix = np.array(self.inverseMatrix)

        self.transposeMatrix=npMatrix.transpose()

    def rotateX(self, a):
        rotateXMatrix = [[None, None, None, None] for i in range(0, 4)]

        # converter para modelo 360º
        a *= math.pi / 180

        rotateXMatrix=[ 
            [1, 0, 0, 0], 
            [0, math.cos(a), -math.sin(a), 0], 
            [0, math.sin(a), math.cos(a), 0], 
            [0, 0, 0, 1]]

        self.multiply3(rotateXMatrix)

    def rotateY(self, a):
        rotateYMatrix = [[None, None, None, None] for i in range(0, 4)]

        # converter para modelo 360º
        a *= math.pi / 180

        rotateYMatrix = [
            [math.cos(a), 0, math.sin(a), 0], 
            [0, 1, 0, 0], 
            [-math.sin(a), 0, math.cos(a), 0], 
            [0, 0, 0, 1]]
        
        self.multiply3(rotateYMatrix)

    def rotateZ(self, a):
        rotateZMatrix = [[None, None, None, None] for i in range(0, 4)]

        # converter para modelo 360º
        a *= math.pi / 180

        rotateZMatrix = [
            [ math.cos(a), -math.sin(a), 0, 0],
            [math.sin(a), math.cos(a), 0, 0],
            [0, 0, 1 ,0],
            [0, 0, 0, 1]]

        self.multiply3(rotateZMatrix)

    def scale(self, x, y, z):
        scaleMatrix = [[None, None, None, None] for i in range(0, 4)]

        scaleMatrix=[[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]

        self.multiply3(scaleMatrix)

    def transform(self, point):
        pointA = [point.x, point.y, point.z, 1] # como é um ponto, w=1
        pointB = self.multiply1(pointA, [None, None, None, None])

        retorno = Vector3(pointB[0] / pointB[3], pointB[1] / pointB[3], pointB[2] / pointB[3])

        return retorno

    def inverse(self, ray):
        pointA = [ray.origin.x, ray.origin.y, ray.origin.z, 1] # w=1 porque a origem é um ponto
        originInverse = self.multiply2(pointA, [None, None, None, None])

        originConverted = Vector3( originInverse[0] / originInverse[3], originInverse[1] / originInverse[3], originInverse[2] / originInverse[3])

        arrA = [ray.direction.x, ray.direction.y, ray.direction.z, 0] # w=0 porque a direção é um vetor
        directionInverse = self.multiply2(arrA, [None, None, None, None])

        directionConverted = Vector3(directionInverse[0], directionInverse[1], directionInverse[2]).normal()

        return Ray(originConverted, directionConverted)

    def transpose(self, vector):
        pointA = [vector.x, vector.y, vector.z, 0] # como é um vetor, w=0
        vectorInverted = self.multiply4(pointA, [None, None, None, None])

        transposeVector = Vector3(vectorInverted[0], vectorInverted[1], vectorInverted[2])

        return transposeVector.normal()
