import math

class Camera():
    def __init__(self, tranformation, distance, fieldOfView):
        self.tranformation=tranformation
        self.distance=distance
        self.fieldOfView=fieldOfView

    def fov(self):
        return self.fieldOfView * math.pi / 180
