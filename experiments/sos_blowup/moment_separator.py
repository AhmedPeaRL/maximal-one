import numpy as np

def degeneracy_direction_measure(r, sigma):
    """
    Construct truncated moment vector
    approximating concentration near x-axis.
    """
    moments = {}
    for i in range(r+1):
        for j in range(r+1-i):
            if j == 0:
                moments[(i,j)] = sigma**i
            else:
                moments[(i,j)] = 0
    return moments
