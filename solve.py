import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from itertools import product, combinations
import math3d as m3d
import math
from time import sleep, perf_counter as pc
import pickle

from collections import defaultdict
obj_pos = defaultdict(list)
obj_fields = defaultdict(list)

neighborsObj = {}

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

def getNeighborsPos(pos):
    """
        get all neighbors of a position
    """
    global neighborsObj
    
    neighbors = []
    for t in [[0,0,1],[0,1,0],[1,0,0],[0,0,-1],[0,-1,0],[-1,0,0]]:
        test = [pos[0]+t[0],pos[1] + t[1],pos[2]+t[2]]
        if max(test) <= 2 and min(test) >= 0:
            neighbors.append(test)
    neighborsObj[pos] = neighbors
    return neighbors
        
def getZeroNeighbors(field,pos):
    """
        get all neighbors which are 0 (no cube exists)
    """
    neighbors = neighborsObj[tuple(pos)]
    zero_neighbors = []
    for neighbor in neighbors:
        if field[neighbor[0],neighbor[1],neighbor[2]] == 0:
            zero_neighbors.append(neighbor)
    return zero_neighbors
    
def getLongestZeroPath(field, pos):
    """
        get the longest path that a part can use in for a given position
    """
    
    path = []
    pathObj = {}
    neighbors2check = getZeroNeighbors(field,pos)
    for neighbor in neighbors2check:
        path.append(neighbor)
        pathObj[tuple(neighbor)] = 1
        
    c = 0
    while len(neighbors2check) > 0:
        c+=1
        neighbor = neighbors2check.pop(0)
        for n in getZeroNeighbors(field,neighbor):
            if tuple(n) not in pathObj:
                path.append(n)
                pathObj[tuple(n)] = 1
                neighbors2check.append(n)
    return path
            
    
def checkZeroNeighborField(field):
    """
        check whether there is a position in the field where no 
        part is possible (where the longest path without a cube is < 4)
    """
    
    r3 = range(3)
    neighborsMap = np.zeros((3,3,3))
    for pos in product(r3,r3,r3):
        if field[pos[0],pos[1],pos[2]] == 0:
            if neighborsMap[pos[0],pos[1],pos[2]] == 0:
                zeroPath = getLongestZeroPath(field,pos)
                len_zeroPath = len(zeroPath)
                if len_zeroPath < 4:
                    return False
                neighborsMap[pos[0],pos[1],pos[2]] = len_zeroPath
                for point in zeroPath:
                    neighborsMap[point[0],point[1],point[2]] = len_zeroPath            
        else:
            neighborsMap[pos[0],pos[1],pos[2]] = -1
    return True
                        
def checkListOfCubes(combination):
    """
        check whether the combination is possible
        - doesn't use a pos more than once
        - has no holes that have a size < 4
    """
    
    global list_blocks
    global obj_fields
    
    field = np.zeros((3,3,3))
    for p_idx in range(len(combination)):
        p = combination[p_idx]
        field += obj_fields[list_blocks[p_idx]][p] 

    if np.max(field) > 1:
        return False
    return checkZeroNeighborField(field)    

def save_obj(filename, obj):
    with open(filename+'.pickle', 'wb') as handle:
        pickle.dump(obj, handle)

    
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
"""
 get all neighbors of each position once
 saved in neighborsObj
"""
for pos in poss:
    getNeighborsPos(pos)

    
list_blocks = ["a","b","c","d","e","f"]

"""
    add all possible combinations for the first block 
    without mirroring    
"""
cblock = list_blocks[0]
for pos in poss:
    if pos[1] != 2:
        checkCubes(cblock,blocks[cblock],pos,False)

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
for cblock in list_blocks[1:]:
    for rotation in rotations:
        for pos in poss:
            checkCubes(cblock,blocks[cblock],pos,rotation)

"""
    how many positions are possible for each block?
"""
pos_lengths = [range(len(obj_pos[x])) for x in list_blocks]            
print(pos_lengths)
"""
    get all combinations of the two first blocks
    - they might be not possible (it is checked later on)
"""
possibleCombinations = list(product(pos_lengths[0],pos_lengths[1]))

"""
    how many solutions are possible for a given number of blocks?
"""
found = np.zeros(len(list_blocks))
found[0] = len(pos_lengths[0])
p = 0
t1 = pc()
t_check = 0
t_check_Z = 0
solutions = []
while p < len(possibleCombinations):
    combination = possibleCombinations[p]

    """
        check if the current combination is possible and reasonable for the next step
    """
    t2 = pc()
    checkBool = checkListOfCubes(combination)
    t_check += pc()-t2
    if checkBool:
        """
            if reasonable increment in found
            and at all possible combinations of the next block to the current position
        """
        found[len(combination)-1] += 1
        if found[len(combination)-1] == 1:
            print("found: ", found[:len(combination)-1])
            print("time: ", pc()-t1)
        
        block_no = len(combination)
        if block_no < len(list_blocks):
            for q in pos_lengths[block_no]:
                lcombination = list(combination)
                lcombination.append(q)
                possibleCombinations.append(tuple(lcombination))
        """
            if all blocks are used => add to solutions
        """
        if len(combination) == len(list_blocks):
            solutions.append(combination)
    p+=1
for combination in solutions:
    print(combination)

print("found: ",found)
print("checked possibleCombinations: ", p)
print("time for checkListOfCubes", t_check)
print("time for everything", pc()-t1)
    
"""
    save the solution and the positions for drawing
"""
save_obj("solutions",solutions)
save_obj("obj_pos",obj_pos)



