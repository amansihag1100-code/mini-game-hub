import numpy as np

board = np.array([1, 2, 3])
for ptr in range(5):
    print(ptr)

    """
    ptr is an array of dim 2
    I need a 2*dim*dim array so that ptr can loop through it
    no 
    ptr is just the position of box
    It has nothing to do with validity of move
    I have (x,y) now move in all the directions to check if it is valid or not
    """
