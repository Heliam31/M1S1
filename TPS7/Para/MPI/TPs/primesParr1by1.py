from mpi4py import MPI
import sys
import random
import math
import numpy as np
import matplotlib.image as mpimg
from scipy import misc
import matplotlib.pyplot as plt
import matplotlib.cm as cmdef
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def nb_primes(n):
    result = 0
    for i in range(1, n+1):
        if n%i == 0:
            result += 1
    return result

upper_bound = int(sys.argv[1])

r = rank
current_max = 0

while (r<upper_bound):
    tmp = nb_primes(r)
    current_max = max(current_max, tmp)
    r += size

max = comm.reduce(current_max, op = MPI.MAX)

if rank==0:
    print(max)
