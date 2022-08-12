import pygame as pg
from matrixfunctions import *
from numba import njit

@njit(fastmath = True)
def anyfunc(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Object3D:
    def __init__(self, render):
    #def __init__(self, render, vertices, faces):
        self.render = render
        self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])
        #self.vertices = np.array([np.array(v) for v in vertices])
        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])
        #self.faces = np.array([np.array(face) for face in faces])
        self.font = pg.font.SysFont("Gotham", 25, bold = True)
        self.colorfaces = [(pg.Color("yellow"), face) for face in self.faces]
        self.movementflag = True
        self.drawvertices = True # drawvertices turned off to improve framerate
        self.label = ""

    def draw(self):
        self.screenprojection()
        self.movement()

    def movement(self):
        if self.movementflag:
            self.rotatey(pg.time.get_ticks() % 0.005)
    
    def screenprojection(self):
        vertices = self.vertices @ self.render.camera.cameramatrix()
        vertices = vertices @ self.render.projection.projectionmatrix
        vertices /= vertices[ :, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.toscreenmatrix
        vertices = vertices[ :, :2]

        for index, colorfaces in enumerate(self.colorfaces):
            color, face = colorfaces
            polygon = vertices[face]
            #if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
            if not anyfunc(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, 2) # Int = line size
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color("purple"))
                    self.render.screen.blit(text, polygon[-1])

        if self.drawvertices:
            for vertex in vertices:
                #if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                if not anyfunc(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color("orange"), vertex, 4) # Int = vertex dot size

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)
    
    def scale(self, scaleto):
        self.vertices = self.vertices @ scale(scaleto)
    
    def rotatex(self, angle):
        self.vertices = self.vertices @ rotatex(angle)
    
    def rotatey(self, angle):
        self.vertices = self.vertices @ rotatey(angle)

    def rotatez(self, angle):
        self.vertices = self.vertices @ rotatez(angle)
    
class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color("red"), pg.Color("green"), pg.Color("blue")]
        self.colorfaces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.drawvertices = False
        self.label = "XYZ"
