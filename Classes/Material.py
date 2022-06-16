class Material():
    def __init__(self, color, ambient, difuse, especular, refraction, refraction_index):
        self.color=color
        # coeficientes \/
        self.ambient=float(ambient) # reflexão ambiente
        self.difuse=difuse
        self.especular=especular
        self.refraction=refraction
        self.refraction_index=refraction_index
