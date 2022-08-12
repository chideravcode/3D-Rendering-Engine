from object3d import * # Import object to be rendered
from camera import *
from projection import *
import pygame as pg

class Engine: # Template for application.
    def __init__ (self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 800, 450 # Window resolution
        self.H_WIDTH = self.WIDTH // 2 # Surface for drawing
        self.H_HEIGHT = self.HEIGHT // 2 # Surface for drawing
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.createobject()
    
    def createobject(self):
        #self.camera = Camera(self, [-10, 10, -100])
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        #self.object = self.getobjectfromfile("Objects/demo_hand.obj")

        # Variables for hard-coded object
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])
        self.worldaxes = Axes(self)
        self.worldaxes.movementflag = False
        self.worldaxes.scale(2.5)
        self.worldaxes.translate([0.0001, 0.0001, 0.0001])
    
    def getobjectfromfile(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith("v "):
                    vertex.append([float(i) for i in line.split()[1: ]] + [1])
                elif line.startswith("f"):
                    facesholder = line.split()[1: ]
                    faces.append([int(facesholder.split("/")[0])- 1 for facesholder in facesholder])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color("white")) # Color of background

        self.worldaxes.draw()
        self.axes.draw()
        self.object.draw()
    
    def run(self): # Main program loop
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT] # Exit application
            pg.display.set_caption(str(self.clock.get_fps())) #Display FPS in application header
            pg.display.flip() # Update rendering surface
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = Engine() # Create instance of engine
    app.run() # Run instance of engine

