import math

class TransformHelper():
    def __init__(self):
        self.transformMatrix=[[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]
        self.inverseMatrix=[]
        self.transposeMatrix=[]

    def multiply1(self, a, b):

        for i in range(0,4):
            b[i]=0

        for i in range(0,4):
            for j in range(0,4):
                b[i] += self.transformMatrix[i][j] * a[j]

        return b

    def multiply3(self, a):
        b=[[],[],[],[]]

        for i in range(0,4):
            for j in range(0,4):
                b[i][j]=self.transformMatrix[i][j]
                self.transformMatrix[i][j]=0

        for i in range(0,4):
            for j in range(0,4):
                for k in range(0,4):
                    self.transformMatrix[i][j] += b[i][k] * a[k][j]

    # cria a matriz correspondente à transformação identidade
    def identityMatrix(self):
        for i in range(0,4):
            for j in range(0,4):
                if i==j:
                    self.transformMatrix[i][j]=1
                else:
                    self.transformMatrix[i][j]=0
    
    # cria a matriz correspondente à translação e multiplica a matriz de transformação composta pela matriz recém-criada
    def translate(self, x, y, z):
        translateMatrix = [[],[],[],[]]

        for i in range(0,4):
            for j in range(0,4):
                if i==j:
                    translateMatrix[i][j]=1
                elif j==3:
                    if i==0:
                        translateMatrix[i][j]=x
                    elif i==1:
                        translateMatrix[i][j]=y
                    elif i==2:
                        translateMatrix[i][j]=z
                    else:
                        translateMatrix[i][j]=1
                else:
                    translateMatrix[i][j]=0

        self.multiply3(translateMatrix)
                    
    def rotateX(self, a):
        rotateXMatrix = [[],[],[],[]]

        a *= math.pi / 180.0

        rotateXMatrix[0][0] = 1.0
        rotateXMatrix[0][1] = 0.0
        rotateXMatrix[0][2] = 0.0
        rotateXMatrix[0][3] = 0.0
        rotateXMatrix[1][0] = 0.0
        rotateXMatrix[1][1] = math.cos(a)
        rotateXMatrix[1][2] = -math.sin(a)
        rotateXMatrix[1][3] = 0.0
        rotateXMatrix[2][0] = 0.0
        rotateXMatrix[2][1] = math.sin(a)
        rotateXMatrix[2][2] = math.cos(a)
        rotateXMatrix[2][3] = 0.0
        rotateXMatrix[3][0] = 0.0
        rotateXMatrix[3][1] = 0.0
        rotateXMatrix[3][2] = 0.0
        rotateXMatrix[3][3] = 1.0

        self.multiply3(rotateXMatrix)

    def rotateY(self, a):
        rotateYMatrix = [[],[],[],[]]

        a *= math.pi / 180.0
        rotateYMatrix[0][0] = math.cos(a)
        rotateYMatrix[0][1] = 0.0
        rotateYMatrix[0][2] = math.sin(a)
        rotateYMatrix[0][3] = 0.0
        rotateYMatrix[1][0] = 0.0
        rotateYMatrix[1][1] = 1.0
        rotateYMatrix[1][2] = 0.0
        rotateYMatrix[1][3] = 0.0
        rotateYMatrix[2][0] = -math.sin(a)
        rotateYMatrix[2][1] = 0.0
        rotateYMatrix[2][2] = math.cos(a)
        rotateYMatrix[2][3] = 0.0
        rotateYMatrix[3][0] = 0.0
        rotateYMatrix[3][1] = 0.0
        rotateYMatrix[3][2] = 0.0
        rotateYMatrix[3][3] = 1.0

        self.multiply3(rotateYMatrix)

    def rotateZ(self, a):
        rotateZMatrix = [[],[],[],[]]

        a *= math.pi / 180.0
        rotateZMatrix[0][0] = math.cos(a)
        rotateZMatrix[0][1] = -math.sin(a)
        rotateZMatrix[0][2] = 0.0
        rotateZMatrix[0][3] = 0.0
        rotateZMatrix[1][0] = math.sin(a)
        rotateZMatrix[1][1] = math.cos(a)
        rotateZMatrix[1][2] = 0.0
        rotateZMatrix[1][3] = 0.0
        rotateZMatrix[2][0] = 0.0
        rotateZMatrix[2][1] = 0.0
        rotateZMatrix[2][2] = 1.0
        rotateZMatrix[2][3] = 0.0
        rotateZMatrix[3][0] = 0.0
        rotateZMatrix[3][1] = 0.0
        rotateZMatrix[3][2] = 0.0
        rotateZMatrix[3][3] = 1.0
        self.multiply3(rotateZMatrix)
    
    def scale(self, x, y, z):
        scaleMatrix=[[],[],[],[]]

        scaleMatrix[0][0] = x
        scaleMatrix[0][1] = 0.0
        scaleMatrix[0][2] = 0.0
        scaleMatrix[0][3] = 0.0
        scaleMatrix[1][0] = 0.0
        scaleMatrix[1][1] = y
        scaleMatrix[1][2] = 0.0
        scaleMatrix[1][3] = 0.0
        scaleMatrix[2][0] = 0.0
        scaleMatrix[2][1] = 0.0
        scaleMatrix[2][2] = z
        scaleMatrix[2][3] = 0.0
        scaleMatrix[3][0] = 0.0
        scaleMatrix[3][1] = 0.0
        scaleMatrix[3][2] = 0.0
        scaleMatrix[3][3] = 1.0
        self.multiply3(scaleMatrix)