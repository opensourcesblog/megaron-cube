import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from itertools import product, combinations
import math3d as m3d
import math

from collections import defaultdict
obj_pos = defaultdict(list)
obj_fields = defaultdict(list)

def getCube(cube,pos,rot):
    """
        cube: position
        pos: add this position after rotation
        rot: rotation axis_angle
        rotate a cube and add a position
        return cube
    """
    if rot is not False:
        cube_vec = m3d.Vector(*cube)
        cube = list(rot*cube_vec)
        cube = [ int(round(x)) for x in cube ]
    return tuple([x + y for x, y in zip(cube, pos)])
    
def checkCubes(name,block,pos,rot):
    """
        check if cube is out of the 3x3 field
        save positions of cubes of the block to
        obj_pos and obj_fields
        return True if position is possible for the given block
        else False
    """
    
    global obj_pos
    global obj_fields
    
    cubes = []
    for cube in block: 
        cube = getCube(cube,pos,rot)
        cubes.append(cube)
        for val in cube:
            if val < 0 or val > 2:
                return False, cubes
    cubes.sort()
    if cubes in obj_pos[name]:
        return False, cubes
    obj_pos[name].append(cubes) 
    field = np.zeros((3,3,3))
    for cube in cubes:
        field[cube] = 1
    obj_fields[name].append(field)  
    return True, cubes
    
        
def getCubes(ax,part,pos,rot):    
    """
        get all cubes for a given part using rotation and change of position
    """
    cubes = []
    for cube in part: 
        cube = getCube(cube,pos,rot)
        cubes.append(cube)
        
    return cubes

def drawCubes(ax,cubes,color):
    for cube in cubes: 
        drawCube(ax,cube[0],cube[1],cube[2],color)

def drawCube(ax,x,y,z,color):
    r = [0,1]
    X, Y = np.meshgrid(r, r)
    ax.plot_surface(x+X,y+Y,z+1, alpha=1, color=color) # top
    ax.plot_surface(x+X,y+Y,z+0, alpha=1, color=color) # bottom
    ax.plot_surface(x+X,y+0,z+Y, alpha=1, color=color) # front
    ax.plot_surface(x+X,y+1,z+Y, alpha=1, color=color) # back
    ax.plot_surface(x+0,y+X,z+Y, alpha=1, color=color) # left
    ax.plot_surface(x+1,y+X,z+Y, alpha=1, color=color) # right
    
fig = plt.figure()
fig.suptitle('Megaron-Cube', fontsize=14, fontweight='bold')
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z') 

color = {}
color["a"] = "red"
color["b"] = "green"
color["c"] = "blue"
color["d"] = "orange"
color["e"] = "yellow"
color["f"] = "purple"

"""
    define all blocks
"""
blocks = {}
blocks["a"] = np.array([[0,0,0],[1,0,0],[2,0,0],[1,0,1]])
blocks["b"] = np.array([[0,0,0],[1,0,0],[2,0,0],[1,0,1],[0,1,0]])
blocks["c"] = np.array([[0,0,0],[1,0,0],[1,0,1],[1,1,0],[2,1,0]])
blocks["d"] = np.array([[0,0,0],[0,0,1],[0,1,0],[1,1,0],[1,2,0]])
blocks["e"] = np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]])
blocks["f"] = np.array([[0,0,0],[1,0,0],[0,1,0],[1,0,1]])

r3 = range(3)
poss = list(product(r3,r3,r3))
list_blocks = ["a","b","c","d","e","f"]

"""
    define possible rotations
"""
deg = 90
rad = deg*math.pi/180
rz = m3d.Orientation.new_axis_angle([0,0,1], rad)
ry = m3d.Orientation.new_axis_angle([0,1,0], rad)
rx = m3d.Orientation.new_axis_angle([1,0,0], rad)

protations = [False,rz,ry,rx]
protations = list(product(protations,protations,protations,protations))

rotations = [False]
for r in protations:
    cr = m3d.Orientation.new_axis_angle([1,0,0], 0)
    for t in r:
        if t is not False:
            cr *= t
    if cr not in rotations:
        rotations.append(cr)
        
"""
    add possible positions of each block (not for the first)
    with rotation
    saved in obj_pos and obj_fields
"""
for cblock in list_blocks:
    for rotation in rotations:
        for pos in poss:
            boolCheck, cubes = checkCubes(cblock,blocks[cblock],pos,rotation)
            if boolCheck:    
                ax.clear()
                drawCubes(ax,cubes,color[cblock])

                ax.set_xlim3d(0, 3)
                ax.set_ylim3d(0, 3)
                ax.set_zlim3d(0, 3)
                plt.pause(0.5)

while True:
    plt.pause(50)


