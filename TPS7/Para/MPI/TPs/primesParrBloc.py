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


if rank == 0:
    n = math.ceil(upper_bound / size)
    tab = [i for i in range(upper_bound)]
    val = [tab[(n*i)+1:(n*(i+1))+1] for i in range(size-1)]+[tab[n*(size-1):len(tab)]]
else:
    val = None

chunk = comm.scatter(val, root = 0)
current_max = 0

for i in range(0, len(chunk)):
    tmp = nb_primes(chunk[i])
    current_max = max(current_max, tmp)

max = comm.reduce(current_max, op = MPI.MAX)

if rank==0:
    print(max)
