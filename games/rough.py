import numpy as np

"""
    ptr is an array of dim 2
    I need a 2*dim*dim array so that ptr can loop through it
    no 
    ptr is just the position of box
    It has nothing to do with validity of move
    I have (x,y) now move in all the directions to check if it is valid or not
"""
dict = {
    0: (0, 1),
    1: (0, -1),
    2: (1, 0),
    3: (-1, 0),
    4: (1, 1),
    5: (-1, -1),
    6: (1, -1),
    7: (-1, 1),
}
n = np.empty(8)
print(n)
