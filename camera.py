from re import L
import pygame as pg
from matrixfunctions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.hfov = math.pi/3
        self.vfov = self.hfov * (render.HEIGHT / render.WIDTH)
        self.nearplane = 0.1
        self.farplane = 100
        self.movingspeed = 0.04
        self.rotationspeed = 0.02
    
    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.movingspeed
        if key[pg.K_d]:
            self.position += self.right * self.movingspeed
        if key[pg.K_w]:
            self.position += self.forward * self.movingspeed
        if key[pg.K_s]:
            self.position -= self.forward * self.movingspeed
        if key[pg.K_q]:
            self.position += self.up * self.movingspeed
        if key[pg.K_e]:
            self.position -= self.up * self.movingspeed

        if key[pg.K_LEFT]:
            self.camerayaw(-self.rotationspeed)
        
        if key[pg.K_RIGHT]:
            self.camerayaw(self.rotationspeed)
        
        if key[pg.K_UP]:
            self.camerapitch(-self.rotationspeed)
        
        if key[pg.K_DOWN]:
            self.camerapitch(self.rotationspeed)

    def camerayaw(self, angle):
        rotate = rotatey(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camerapitch(self, angle):
        rotate = rotatex(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translatematrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotatematrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def cameramatrix(self):
        return self.translatematrix() @ self.rotatematrix()


