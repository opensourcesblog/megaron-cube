import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from itertools import product, combinations
import math3d as m3d
import math
from time import sleep, perf_counter as pc
import pickle


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

def load_obj(filename):
    with open(filename+'.pickle', 'rb') as handle:
        return pickle.load(handle)    
    
color = {}
color["a"] = "red"
color["b"] = "green"
color["c"] = "blue"
color["d"] = "orange"
color["e"] = "yellow"
color["f"] = "purple"

fig = plt.figure()
fig.suptitle('Megaron-Cube Solution', fontsize=14, fontweight='bold')
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

list_blocks = ["a","b","c","d","e","f"]

solutions = load_obj("solutions")
obj_pos = load_obj("obj_pos")
    
for combination in solutions: 
    ax.clear()
    list_of_cubes = []
    list_of_colors = [] 
    for block_idx in range(len(combination)):
        block = list_blocks[block_idx]
        cubes = obj_pos[block][combination[block_idx]]
        list_of_cubes.append(cubes)
        list_of_colors.append(color[block])

    for cube_idx in range(len(list_of_cubes)):
        cubes = list_of_cubes[cube_idx]
        c = list_of_colors[cube_idx]
        drawCubes(ax,cubes,c)

    ax.set_xlim3d(0, 3)
    ax.set_ylim3d(0, 3)
    ax.set_zlim3d(0, 3)
    plt.pause(5)
        

while True:
    plt.pause(50)
