class Transformation():
    def __init__(self, tx, ty, tz, rx, ry, rz, sx, sy, sz):
        self.tx=tx
        self.ty=ty
        self.tz=tz
        self.rx=rx
        self.ry=ry
        self.rz=rz
        self.sx=sx
        self.sy=sy
        self.sz=sz

    """def matrix(self):
        retorno={"translation":[], "rotation":[], "scale":[]}

        translation=[
            [self.tx, 0, 0, 0],
            [0, self.ty, 0, 0],
            [0,0,self.tz,0],
            [0,0,0,1]]

        rotation=[
            [self.rx, 0, 0, 0],
            [0, self.ry, 0, 0],
            [0,0,self.rz,0],
            [0,0,0,1]]
        scale=[
            [self.sx, 0, 0, 0],
            [0, self.sy, 0, 0],
            [0,0,self.sz,0],
            [0,0,0,1]]

        retorno["translation"]=translation
        retorno["rotation"]=rotation
        retorno["scale"]=scale

        return retorno"""