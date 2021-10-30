import OpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from  OpenGL.GLUT import *
from OpenGL.GLU import *
import pywavefront
import numpy as np
import math

# We first read the object file points.
scene = pywavefront.Wavefront('scene.obj', collect_faces=True)

# https://stackoverflow.com/questions/59923419/pyopengl-how-do-i-import-an-obj-file
scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

print(scene_box)

scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)

print(max_scene_size)


# We make a grid of cubicles of a certain size.
size = 100
cube_width = max_scene_size / size

cubes = np.zeros((size + 1, size + 1, size + 1))
# Go through all vertices
# Calculate which cubicle it would be contained in
for vertex in scene.vertices:
    x,y,z = vertex
    x = math.floor((x - scene_box[0][0]) / cube_width)
    y = math.floor((y - scene_box[0][1]) / cube_width)
    z = math.floor((z - scene_box[0][2]) / cube_width)
    cubes[x, y, z] = 1

# Now that we have cubes, we want to make a triangle mesh for every face of
# every cube
# so that it can be displayed in openGL.
square_box = [[0,0,0], [size + 1, size + 1, size + 1]]

scaled_size    = 5
scene_scale    = [scaled_size/size for i in range(3)]
scene_trans    = [-(square_box[1][i]+square_box[0][i])/2 for i in range(3)]

# Estemate a model using squares algorithm.
def makeQuads(x_ind, y_ind, z_ind):
    x = x_ind * 1
    y = y_ind * 1
    z = z_ind * 1
    tlb = [x, y, z]
    trb = [x + 1, y, z]
    blb = [x, y + 1, z]
    brb = [x + 1, y + 1, z]

    tlf = [x, y, z + 1]
    trf = [x + 1, y, z + 1]
    blf = [x, y + 1, z + 1]
    brf = [x + 1, y + 1, z + 1]

    q1 = [tlf, trf, brf, blf]
    q2 = [trf, trb, brb, brf]
    q3 = [tlb, trb, trf, tlf]
    q4 = [tlb, tlf, blf, blb]
    q5 = [trb, tlb, blb, brb]
    q6 = [brb, blb, blf, brf]
    return [q1, q2, q3, q4, q5, q6]


def Model():
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)

    glBegin(GL_QUADS)
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if(cubes[x, y, z] == 1):
                    quads = makeQuads(x, y, z)
                    for q in quads:
                        for vertex in q:
                            glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()

    glPopMatrix()

def main():
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 1, 500.0)
        glTranslatef(0.0, 0.0, -10)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        glTranslatef(-0.5,0,0)
                    if event.key == pygame.K_RIGHT:
                        glTranslatef(0.5,0,0)
                    if event.key == pygame.K_UP:
                        glTranslatef(0,1,0)
                    if event.key == pygame.K_DOWN:
                        glTranslatef(0,-1,0)

            # glRotatef(1, 5, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            Model()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            pygame.display.flip()
            pygame.time.wait(10)

main()



# Convert to schematic.